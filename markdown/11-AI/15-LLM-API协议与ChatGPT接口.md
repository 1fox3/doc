# LLM API 协议与 ChatGPT 接口

## LLM API 是否存在共性

主流 LLM Provider 的 API 协议存在明显共性。无论是 OpenAI、Anthropic、Google、AWS Bedrock、Azure OpenAI，还是兼容 OpenAI 协议的本地推理服务，核心都是围绕“输入上下文、模型参数、生成结果、工具调用、流式输出、计费统计”来设计。

常见共性：

1. 基于 HTTP/HTTPS 调用。
2. 使用 JSON 作为请求和响应格式。
3. 使用 API Key 或云厂商 IAM 做鉴权。
4. 请求中指定 `model`。
5. 请求中传入用户输入、系统指令和历史上下文。
6. 支持 `temperature`、`top_p`、`max_tokens` 等推理参数。
7. 支持普通响应和流式响应。
8. 支持多模态输入，例如文本、图片、音频。
9. 支持工具调用或函数调用。
10. 响应中返回生成内容、结束原因和 token 用量。
11. 错误通常通过 HTTP 状态码和结构化错误对象表达。
12. 存在限流、超时、重试、上下文窗口和内容安全限制。

差异主要体现在：

1. 消息格式不同，例如 `system` 是否独立字段、是否支持多段 content。
2. 工具调用字段不同，例如 OpenAI 的 `tools`、Anthropic 的 `tool_use`。
3. 流式事件格式不同。
4. 模型名称、上下文长度、计费口径不同。
5. 结构化输出、JSON Schema、文件上传、批处理等高级能力不同。
6. 安全策略和内容过滤返回方式不同。

工程实践中通常会封装一层模型网关，屏蔽不同 Provider 的协议差异，让业务只依赖内部统一接口。

## ChatGPT API 与 OpenAI API 的关系

日常所说的 ChatGPT API，工程上通常指 OpenAI 提供的模型 API。ChatGPT 是产品形态，OpenAI API 是开发者接入模型能力的接口。

OpenAI 目前推荐使用 `Responses API` 作为统一入口，也可以继续在旧项目中看到 `Chat Completions API`。新项目优先理解 `Responses API`。

## 鉴权方式

HTTP 请求通常通过 `Authorization` 头传入 API Key。

```http
Authorization: Bearer $OPENAI_API_KEY
Content-Type: application/json
```

工程注意：

1. API Key 只能放在服务端，不能暴露给浏览器或移动端客户端。
2. 生产环境建议通过密钥管理系统保存，例如 KMS、Vault、云厂商 Secret Manager。
3. 日志中不能打印完整 API Key、用户隐私内容和敏感上下文。

## Responses API 基本协议

接口地址：

```http
POST https://api.openai.com/v1/responses
```

最小请求示例：

```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1-mini",
    "input": "用三句话解释 RAG 是什么。"
  }'
```

典型响应结构可以理解为：

```json
{
  "id": "resp_xxx",
  "object": "response",
  "created_at": 1710000000,
  "status": "completed",
  "model": "gpt-4.1-mini",
  "output": [
    {
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "RAG 是检索增强生成..."
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 20,
    "output_tokens": 80,
    "total_tokens": 100
  }
}
```

核心字段：

| 字段 | 作用 |
| --- | --- |
| `model` | 指定使用的模型 |
| `input` | 用户输入，可以是字符串，也可以是消息数组 |
| `instructions` | 系统级指令，类似 system prompt |
| `temperature` | 控制随机性，越低越稳定 |
| `top_p` | nucleus sampling 参数，通常不要和 `temperature` 同时大幅调整 |
| `max_output_tokens` | 限制最大输出 token 数 |
| `tools` | 声明模型可调用的工具 |
| `stream` | 是否启用流式输出 |
| `response_format` 或结构化输出配置 | 约束模型输出 JSON 或指定 schema |
| `usage` | token 用量统计 |

## 消息格式

简单任务可以直接用字符串：

```json
{
  "model": "gpt-4.1-mini",
  "input": "把下面一句话翻译成英文：你好，世界。"
}
```

多轮对话通常使用消息数组：

```json
{
  "model": "gpt-4.1-mini",
  "instructions": "你是一个资深 Java 后端面试教练，回答要具体。",
  "input": [
    {
      "role": "user",
      "content": "什么是线程池？"
    },
    {
      "role": "assistant",
      "content": "线程池是复用线程执行任务的机制..."
    },
    {
      "role": "user",
      "content": "那如何设置核心线程数？"
    }
  ]
}
```

常见角色：

1. `system` 或 `instructions`：定义模型行为边界、身份、输出格式和约束。
2. `user`：用户输入。
3. `assistant`：模型历史回复。
4. `tool`：工具执行结果。

面试表达：

> LLM API 的输入不是单条问题，而是一段上下文。服务端需要把系统指令、用户当前问题、必要的历史消息、RAG 检索结果和工具结果组装成模型请求，同时控制 token 长度和敏感信息。

## Python SDK 调用

安装：

```bash
pip install openai
export OPENAI_API_KEY="你的 API Key"
```

普通调用：

```python
from openai import OpenAI


client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-mini",
    instructions="你是一个资深后端工程师，回答要结构化。",
    input="解释一下 LLM API 为什么需要流式输出。",
)

print(response.output_text)
```

## 流式输出协议

聊天、代码生成、长文档总结通常使用流式输出，降低首 token 延迟。

请求中开启 `stream`：

```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1-mini",
    "input": "写一段 Spring Boot 接入 OpenAI API 的设计说明。",
    "stream": true
  }'
```

Python SDK 示例：

```python
from openai import OpenAI


client = OpenAI()
with client.responses.stream(
    model="gpt-4.1-mini",
    input="用要点说明 SSE 和 WebSocket 在 AI 流式输出中的区别。",
) as stream:
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
```

工程注意：

1. 前端常用 SSE 展示模型增量输出。
2. 后端要支持用户取消请求，并停止继续消费模型输出。
3. 流式输出的错误可能发生在响应中途，需要有前端兜底提示。
4. Markdown 和代码块要做增量渲染兼容。
5. 不建议在流式链路中做过重的同步后处理。

## 工具调用协议

工具调用的核心思想：模型负责判断要不要调用工具以及生成参数，业务服务负责真正执行工具，再把工具结果交回模型总结。

示例工具定义：

```python
from openai import OpenAI


client = OpenAI()
tools = [
    {
        "type": "function",
        "name": "get_order_status",
        "description": "查询订单状态",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "订单号"
                }
            },
            "required": ["order_id"],
            "additionalProperties": False
        }
    }
]

response = client.responses.create(
    model="gpt-4.1-mini",
    input="帮我查一下订单 A1001 的状态。",
    tools=tools,
)

for item in response.output:
    if item.type == "function_call":
        print(item.name, item.arguments)
```

典型执行流程：

1. 应用把用户问题和工具 schema 发给模型。
2. 模型输出 `function_call`，包含工具名和 JSON 参数。
3. 应用校验参数、权限和业务边界。
4. 应用执行真实工具，例如查数据库、调内部 API、检索文档。
5. 应用把工具结果再次发给模型。
6. 模型基于工具结果生成最终自然语言回答。

关键原则：

1. 模型不能直接访问数据库、文件系统或内网 API。
2. 工具参数必须做 schema 校验和权限校验。
3. 高风险动作要加人工确认，例如支付、删除、发邮件。
4. 工具返回结果要控制长度，避免撑爆上下文窗口。

## 结构化输出

很多业务不需要自然语言，而是需要稳定 JSON，例如分类、抽取、打标、路由。

示例：

```python
from openai import OpenAI


client = OpenAI()
response = client.responses.create(
    model="gpt-4.1-mini",
    input="从文本中抽取工单优先级：线上支付接口 500，影响所有用户。",
    text={
        "format": {
            "type": "json_schema",
            "name": "ticket_priority",
            "schema": {
                "type": "object",
                "properties": {
                    "priority": {
                        "type": "string",
                        "enum": ["P0", "P1", "P2", "P3"]
                    },
                    "reason": {
                        "type": "string"
                    }
                },
                "required": ["priority", "reason"],
                "additionalProperties": False
            }
        }
    },
)

print(response.output_text)
```

工程注意：

1. 结构化输出仍然要在服务端做 JSON 解析和 schema 校验。
2. 解析失败可以带着错误信息重试一次，但不能无限重试。
3. 关键业务不能只依赖模型判断，要结合规则、权限和人工审核。

## 多模态输入

多模态模型可以同时处理文本和图片等输入。

示例结构：

```json
{
  "model": "gpt-4.1-mini",
  "input": [
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "请解释这张架构图的主要模块。"
        },
        {
          "type": "input_image",
          "image_url": "https://example.com/architecture.png"
        }
      ]
    }
  ]
}
```

使用场景：

1. 图片理解。
2. 截图问答。
3. 票据、表格、合同初步抽取。
4. UI 走查和代码生成辅助。

## Chat Completions API 旧协议

很多历史项目仍然使用 `/v1/chat/completions`。

接口地址：

```http
POST https://api.openai.com/v1/chat/completions
```

请求示例：

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "system",
      "content": "你是一个资深后端工程师。"
    },
    {
      "role": "user",
      "content": "解释一下限流和熔断的区别。"
    }
  ],
  "temperature": 0.2,
  "max_tokens": 800
}
```

响应示例：

```json
{
  "id": "chatcmpl_xxx",
  "object": "chat.completion",
  "created": 1710000000,
  "model": "gpt-4o-mini",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "限流是控制进入系统的请求量..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 120,
    "total_tokens": 170
  }
}
```

Chat Completions 和 Responses 的主要区别：

| 对比项 | Chat Completions | Responses |
| --- | --- | --- |
| 接口定位 | 传统聊天补全接口 | 新一代统一生成接口 |
| 输入字段 | `messages` | `input`、`instructions` |
| 输出字段 | `choices[].message` | `output`、`output_text` |
| 多模态 | 支持但表达较旧 | 更统一 |
| 工具调用 | `tools`、`tool_calls` | 统一在 output item 中表达 |
| 新项目建议 | 可维护旧项目 | 优先使用 |

## 错误与限流

常见 HTTP 状态码：

| 状态码 | 含义 | 处理建议 |
| --- | --- | --- |
| `400` | 请求参数错误 | 修正请求格式、schema、模型名 |
| `401` | 鉴权失败 | 检查 API Key |
| `403` | 无权限 | 检查账号权限、模型权限、组织配置 |
| `404` | 资源不存在 | 检查 endpoint、文件 ID、模型名 |
| `408` | 请求超时 | 缩短输入、调整超时、考虑异步任务 |
| `429` | 限流或额度不足 | 指数退避、降级、排队、检查配额 |
| `500` | 服务端错误 | 短暂重试、故障降级 |
| `503` | 服务不可用 | 重试、切换备用模型 |

重试原则：

1. 网络错误、`429`、`500`、`503` 可以有限重试。
2. `400`、`401`、`403` 通常不应重试。
3. 重试要使用指数退避和最大次数限制。
4. 非幂等工具调用不能直接重试，例如扣款、下单、发消息。

## 生产接入建议

生产系统不要让业务代码到处直接调用 OpenAI API，建议封装模型网关。

模型网关需要处理：

1. Provider 适配。
2. API Key 管理。
3. 模型路由。
4. 超时、重试和熔断。
5. 用户级、租户级和模型级限流。
6. Token 统计和成本统计。
7. Prompt 模板版本管理。
8. 请求和响应脱敏日志。
9. 内容安全审核。
10. 结构化输出校验。
11. 流式输出转发。
12. 灰度发布和 A/B Test。

简化架构：

```text
业务服务 -> 模型网关 -> OpenAI API
              |
              +-> 鉴权和限流
              +-> Prompt 模板
              +-> RAG 上下文
              +-> 工具调用编排
              +-> 日志、监控、评估
```

## 面试高频问答

### LLM API 协议有什么共性

回答模板：

> 共性主要是 HTTP + JSON + API Key 鉴权，请求里指定模型、输入上下文和推理参数，响应里返回生成内容、结束原因和 token 用量。多数 Provider 都支持流式输出、工具调用、结构化输出和多模态输入。差异主要在消息格式、工具调用格式、流式事件格式、模型命名和安全策略，所以工程上通常会封装模型网关来做适配。

### 为什么不在前端直接调用 ChatGPT API

回答模板：

> 因为 API Key 会泄露，用户可以绕过业务限流和权限控制，也无法统一做审计、脱敏、成本控制和内容安全。正确做法是前端调用自己的后端，后端通过模型网关调用 OpenAI API。

### 流式输出为什么重要

回答模板：

> LLM 生成长文本时整体耗时较长，流式输出可以降低首 token 延迟，让用户尽快看到内容。工程上一般用 SSE 或 WebSocket 转发模型增量输出，同时要支持取消、错误兜底、Markdown 增量渲染和日志脱敏。

### Function Calling 和普通 Prompt 有什么区别

回答模板：

> 普通 Prompt 只是让模型生成文本，Function Calling 是让模型按 schema 生成工具调用意图和参数。真正的工具执行仍然由业务系统完成，因此可以做权限校验、参数校验、审计和人工确认，适合订单查询、知识库检索、代码执行等场景。

### 如何控制成本

回答模板：

> 成本主要由输入 token、输出 token、模型单价和调用次数决定。常见手段包括选择合适模型、限制最大输出、压缩历史上下文、RAG 只放必要片段、缓存高频结果、对高成本接口限流、异步批处理和监控 token 用量。

## 记忆要点

1. ChatGPT API 工程上通常指 OpenAI API。
2. 新项目优先理解 `Responses API`，旧项目常见 `Chat Completions API`。
3. LLM API 的核心输入是上下文，不只是用户当前问题。
4. 流式输出是 AI 应用体验的关键能力。
5. 工具调用必须由业务系统执行，模型只生成调用意图和参数。
6. 结构化输出要配合服务端 schema 校验。
7. 生产系统建议通过模型网关统一封装 Provider 差异、安全、限流、成本和监控。
