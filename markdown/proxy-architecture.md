# Scallop Gateway — Proxy Architecture

Scallop Gateway 是一个智能本地代理，将 Claude Code 发出的 Anthropic API 请求路由到多个 LLM 后端，并支持自动降级（fallback）。本文档从源码角度深入分析其代理实现原理。

---

## 总体请求流程

```
Claude Code
    │  POST /v1/messages (Bearer token + model 前缀)
    ▼
scallop/proxy.py  ── handle_messages()
    │  按 model 前缀分发
    ├─► anthropic:*    → AnthropicAdapter
    ├─► ebay:*         → EbayAdapter
    ├─► ebay-openai:*  → EbayAdapter (OpenAI 协议)
    ├─► openai-local:* → OpenAILocalAdapter
    ├─► anthropic-local:* → AnthropicLocalAdapter
    ├─► copilot:*      → CopilotAdapter
    └─► router:*       → RouterAdapter（多后端自动 fallback）
            │
            ├─► 按 fallback_chain 顺序逐一尝试
            └─► 每个后端对应上述某一 Adapter
```

所有响应均以 **SSE（Server-Sent Events）流式** 方式透传给 Claude Code，非流式请求直接返回 400。

---

## 核心组件

### 1. 代理入口：`scallop/proxy.py`

**`handle_messages()`**（`proxy.py:110`）是唯一的请求处理器，绑定到 `POST /v1/messages`。

主要职责：

1. **认证校验**：提取 `Authorization: Bearer <token>`，缺失则返回 401。
2. **模型前缀路由**：读取请求体的 `model` 字段，按前缀映射到对应 Adapter：

   | model 前缀 | Adapter | app key |
   |---|---|---|
   | `anthropic:` | AnthropicAdapter | `anthropic_adapter` |
   | `ebay:` | EbayAdapter | `ebay_adapter` |
   | `ebay-openai:` | EbayAdapter (OpenAI 协议) | `ebay_openai_adapter` |
   | `openai-local:` | OpenAILocalAdapter | `openai_local_adapter` |
   | `anthropic-local:` | AnthropicLocalAdapter | `anthropic_local_adapter` |
   | `copilot:` | CopilotAdapter | `copilot_adapter` |
   | `router:` | RouterAdapter | `router_adapter` |

3. **剥离前缀**：路由后将 `model` 字段改写为真实模型名（如 `anthropic:claude-sonnet-4-6` → `claude-sonnet-4-6`）再传给 Adapter。
4. **流式转发**：建立 `aiohttp.StreamResponse`，从 Adapter 异步迭代 SSE chunks 并逐块 `write` + `drain`。
5. **监控埋点**：每个 chunk 触发 `monitor.record_chunk()`，每 10 个 chunk 触发进度快照，完成或出错时触发 `monitor.complete_request()`。

---

### 2. 配置系统：`scallop/config.py`

配置从两个 TOML 文件合并而来：

- **`config/devzone.toml`**（或指定的 `--config`）：代理服务器、后端 URL、认证等运行时配置
- **`router/default.toml`**（或指定的 `--router`）：路由策略（fallback chains）

两文件通过 `Config._deep_merge()` 合并，router 文件只允许包含 `[router.strategies.*]` 段。

**模型字符串解析**（`_parse_model_with_retry()`，`config.py:21`）：

```
"anthropic:claude-sonnet-4-6*3"
 └─ backend: "anthropic"
    model:   "claude-sonnet-4-6"
    retries: 3
```

**Fallback chain 展开**（`_expand_fallback_chain()`，`config.py:70`）：

将 `["anthropic:model*3", "ebay:other*2"]` 展开为有序的尝试列表：

```python
[
  ("anthropic", "model", 1, False),  # is_retry=False
  ("anthropic", "model", 2, True),
  ("anthropic", "model", 3, True),
  ("ebay",      "other", 4, False),
  ("ebay",      "other", 5, True),
]
```

---

### 3. 路由核心：`RouterAdapter`（`scallop/adapters/router.py`）

`router:` 前缀的请求由 `RouterAdapter.forward_request()` 处理（`router.py:92`）。

**执行流程**：

1. 从 `model` 字段提取策略名（`router:default` → `default`）
2. 从配置中取出该策略的 `fallback_chain`
3. 调用 `Config._expand_fallback_chain()` 展开为逐一尝试列表
4. **粘性模型优先**：若 `ModelStickinessTracker` 有有效记录，将该模型的所有尝试移到链首
5. 逐一尝试：
   - 获取对应 Adapter，修改请求体的 `model` 为目标模型名
   - Copilot / OpenAI 类 Adapter 不传 `bearer_token`，其余需要
   - 将 Adapter 的 SSE chunks 直接 `yield` 给上层
   - 成功：更新粘性记录，结束
   - `ClientResponseError`（4xx/5xx）或 `SSEErrorException`：记录错误，继续下一个
6. 所有尝试失败则抛出最后一个异常

**当前路由策略**（`router/default.toml`）：

| 策略 | 用途 | 链顺序（摘要）|
|---|---|---|
| `default` | 主策略 | Sonnet 4.6 → Sonnet 4.5 → Sonnet 4 → GLM → Sonnet 3.7 → ... → Copilot |
| `subagent` | 子 Agent | Copilot → Sonnet 4.6 → Sonnet 4.5 → 自托管 |
| `haiku` | 低延迟 | Copilot mini → 本地 Qwen → GLM → Sonnet |
| `opus` | 旗舰模型 | Opus 4.7 → Opus 4.6 |
| `sonnet` | Sonnet 优先 | Sonnet 4.6 → 4.5 → 自托管降级 |
| `sonnet-only` | 仅 Sonnet | Sonnet 4.6 → 4.5 → HubGPT |
| `self-hosted` | 仅自托管 | GLM → Qwen → HubGPT |

---

### 4. 各后端 Adapter

#### AnthropicAdapter（`scallop/adapters/anthropic.py`）
- 转发到 HubGPT `/anthropic/v1/messages`，携带用户 Bearer token
- 请求前执行两个 **thinking 变换**：
  - `normalize_adaptive_thinking()`：将 Claude Code 发出的 `thinking.type="adaptive"` 转换为 `"enabled"` 并补全 `budget_tokens`
  - `normalize_claude_thinking_blocks()`：清理历史消息中来自自托管模型（GLM/MiniMax）的无效 thinking 签名
- 记录 `last_response_headers` 和 `last_error_body` 供 RouterAdapter 读取

#### EbayAdapter（`scallop/adapters/ebay.py`）
- 支持 Anthropic 协议和 OpenAI 协议两种变体
- 转发到 HubGPT `/ebay/v1/messages`

#### CopilotAdapter（`scallop/adapters/copilot.py`）
- 通过 GitHub OAuth Device Flow 认证，获取 GitHub 短期 Copilot token
- 将 Anthropic 格式请求转换为 OpenAI Chat Completions 或 Responses API 格式
- 后台任务持续刷新 Copilot token（`_token_refresh_loop()`）
- 支持模型映射（`copilot.model_mapping`：Anthropic 名 → Copilot 名）
- 将 OpenAI SSE 响应转换回 Anthropic SSE 格式

#### OpenAILocalAdapter / AnthropicLocalAdapter
- 转发到本地运行的 OpenAI 兼容或 Anthropic 兼容端点（如本地 vLLM/MLX）
- 支持模型别名映射

---

### 5. Thinking 块规范化：`scallop/transforms/thinking.py`

当路由在 Anthropic 与自托管模型（GLM、MiniMax）之间切换时，历史消息中可能含有非 Claude 的 thinking 块（签名不以 `E` 开头或长度 ≤ 100），Claude API 会拒绝这些内容。

**规范化规则**（`normalize_claude_thinking_blocks()`，`thinking.py:219`）：

| 情况 | 处理 |
|---|---|
| 无效 thinking 签名 | 转为 `<assistant_thinking>...</assistant_thinking>` 文本 |
| reasoning 块 | 转为 `<assistant_reasoning>...</assistant_reasoning>` 文本 |
| tool call/result ID 含特殊字符 | 替换为 `_` |
| 空 thinking 块 | 过滤掉 |
| 最后一条 assistant 消息无有效 thinking/tool（thinking 已启用时）| 整条删除，让 Claude 重新生成 |

---

### 6. 模型粘性：`ModelStickinessTracker`（`scallop/model_stickiness.py`）

在 fallback 发生后（主模型不可用，切换到次选模型成功），将成功的模型记录在 `_sticky_models` 字典中。

后续同一策略的请求在粘性窗口（`router.stickiness_window_seconds`，默认 0 即禁用）内，将该模型的所有重试次数移到 fallback chain 最前面，避免每次都先尝试已知失败的主模型。

若主模型恢复（第一个尝试即成功），粘性记录自动清除。

---

### 7. 实时监控：`scallop/monitoring/`

- **`RequestMonitor`**：在请求生命周期各阶段（开始、每次后端尝试、每个 chunk、完成）记录事件
- **`EventBuffer`**：环形缓冲区，存储最近 N 条事件及汇总指标（成功率、P50/P99 延迟）
- **WebSocket**（`/ws`）：将实时事件推送给 Dashboard
- **`/monitor`**：基于 React/TypeScript 构建的可视化 Dashboard，展示实时请求流、fallback 情况、各后端响应时间

---

## 关键设计决策

| 决策 | 原因 |
|---|---|
| **仅支持流式响应** | Claude Code 始终使用流式；非流式会返回 400，避免实现复杂的非流式 fallback 逻辑 |
| **前缀路由而非配置映射** | 每个请求明确声明目标后端，避免歧义；Router 策略统一通过 `router:` 前缀进入 |
| **SSE 透传** | Adapter 直接 yield bytes，proxy 层不解析响应体，最大化传输效率和兼容性 |
| **两个配置文件分离** | runtime config（证书、端口）与 router 策略（fallback chain）分离，便于运营时只调整路由而不重启服务 |
| **Thinking 规范化** | 自托管模型不理解 Claude 的 thinking 协议，gateway 层透明处理，Claude Code 无感知 |
