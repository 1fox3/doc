# Forger Slack Bot Agent 实现原理分析

## 核心设计哲学

**不自己实现 LLM 推理循环**——而是把 `claude` CLI 作为子进程启动，tool use loop 完全委托给 Claude Code CLI 原生处理。

---

## 整体架构

```
Slack 消息
    ↓
slack_bolt (Socket Mode WebSocket)
    ↓
SupportTask 调度
    ↓
生成 run.sh → AppleScript 在 macOS Terminal 新标签页执行
    ↓
claude CLI 进程
    ↓  ↕ MCP Protocol
自定义 MCP Servers (工具集)
    ↓
Slack Web API (回复消息)
```

---

## 目录结构

```
Forger/
├── launcher/                     # 核心业务代码
│   ├── entry/                    # 各组件入口点
│   │   ├── bot.py                # 统一入口：@mention→Yor, 🧠→Anya
│   │   ├── anya.py               # 仅Anya入口
│   │   ├── slack_support.py      # 仅Lily入口
│   │   ├── approval_monitor.py   # Gate2审批监控入口
│   │   ├── task_ui.py            # Jira Task UI入口
│   │   ├── mcp_slack.py          # Slack MCP server入口
│   │   ├── mcp_github.py         # GitHub MCP server入口
│   │   ├── mcp_jenkins.py        # Jenkins MCP server入口
│   │   ├── mcp_cloudconsole.py   # Cloud Console MCP server入口
│   │   ├── mcp_obsidian.py       # Obsidian MCP server入口
│   │   └── mcp_cal.py            # Cal MCP server入口
│   ├── slack_support/            # Slack事件处理核心
│   │   ├── event.py              # EventServer: Socket Mode监听
│   │   ├── hook.py               # HookServer: Flask HTTP服务器(port 7000)
│   │   ├── task.py               # SupportTask: 任务生命周期管理
│   │   └── poller.py             # ThreadPoller: 后台消息轮询
│   ├── mcp_server/               # 自定义MCP服务器实现
│   │   ├── server.py             # McpServer基类(包装FastMCP)
│   │   ├── slack.py              # SlackMcpServer: 核心Slack工具集
│   │   ├── github.py             # GithubMcpServer
│   │   ├── jenkins.py            # JenkinsMcpServer
│   │   ├── cloudconsole.py       # CloudConsoleMcpServer
│   │   ├── obsidian.py           # ObsidianMcpServer
│   │   └── cal.py                # CalMcpServer
│   ├── slack_client/             # Slack SDK封装
│   ├── approval_team/            # Gate2审批委员会
│   ├── claude/                   # Soul加载和模板渲染
│   ├── config/                   # 配置管理（凭证、路径、MCP）
│   ├── souls/                    # Agent人格模板(.md.tpl)
│   ├── task_ui/                  # Flask Web仪表板(port 7788)
│   └── utils/                    # AppleScript Terminal控制等工具
├── plugins/Forger/               # Claude Code插件包
│   ├── .claude-plugin/plugin.json
│   ├── resources/                # 凭证模板、soul资源
│   └── skills/
│       ├── forger_setup/         # 安装向导skill
│       └── forger_run/           # 启动/停止bot skill
├── launch_forger.sh
├── launch_task_ui.sh
├── CLAUDE.md
└── .claude/
    ├── rules/                    # Claude行为规则
    ├── mcp/all.mcp.json          # 运行时生成的MCP配置
    └── settings.json             # Claude Code权限配置
```

---

## 三个核心机制

### 1. 消息接收：两条路径

**路径 A — Socket Mode**（`slack_support/event.py`）

使用 `slack_bolt` 通过 WebSocket 长连接接收 Slack 事件，无需公网 HTTP endpoint。

```python
self.app = App(token=Credential().slack_bot_token)
SocketModeHandler(self.app, Credential().slack_app_token).start()

@self.app.event("app_mention")      # @mention → 触发 Yor
@self.app.event("reaction_added")   # 🧠 emoji → 触发 Anya
```

**路径 B — HTTP Hook**（`slack_support/hook.py`）

Flask 服务监听 `localhost:7000`，供本地脚本或浏览器书签触发：

```
GET http://localhost:7000/?slack=<thread_url>&soul=<soul>
```

也处理 session 生命周期回调：`/session_start`、`/session_end`、`/task_cost`。

`bot.py` 同时启动两者——HookServer 在后台线程运行，EventServer 在主线程阻塞。

---

### 2. 调用 Claude：子进程 + CLI

`SupportTask` 生成一个 `run.sh`，在 macOS Terminal 新标签页执行：

```bash
export SOUL_CUSTOM=$(cat /path/to/soul.md)
export TASK_HOME=/path/to/tasks/{channel}/{ts}/{soul}/
cd $TASK_HOME
claude \
  --dangerously-skip-permissions \
  --mcp-config ~/.claude/mcp/all.mcp.json \
  --system-prompt "$SOUL_CUSTOM

Working directory: '$TASK_HOME'
Here is the slack link: '<thread_url>'" \
  --session-id <uuid5(thread_url + soul)> \
  "Read the thread using read_thread again"
```

| 参数 | 作用 |
|---|---|
| `--system-prompt` | 注入 soul（人格）+ 任务上下文 |
| `--mcp-config` | 指向 MCP 配置文件，提供工具集 |
| `--session-id` | uuid5(thread_url + soul)，保证同一 thread 共享同一 session |
| `--resume` | 断点续接已有 session |
| `--permission-mode` / `--dangerously-skip-permissions` | 权限模式，因 soul 而异 |

**Terminal 作为 UI**：通过 AppleScript 控制 macOS Terminal（或 cmux），每个 session 在独立标签页中运行，可直接观察 Claude 的推理过程。

---

### 3. 工具暴露：MCP 服务器

工具通过 **MCP（Model Context Protocol）** 协议暴露给 Claude，基于 `fastmcp` 库实现：

```python
class McpServer:
    def __init__(self, name):
        self.app = FastMCP(name)

class SlackMcpServer(McpServer):
    def _init_tools(self):
        self.app.tool(self.read_thread, description="...")
        self.app.tool(self.reply_thread, description="...")
        # ...
```

**Slack MCP Server 工具集（Claude 可直接调用）：**

| 工具名 | 功能 |
|---|---|
| `read_thread` | 读取 Slack thread 所有消息 |
| `poll_thread` | 轮询新消息（最多10分钟，每15秒） |
| `reply_thread` | 回复 Slack thread（自动PII脱敏） |
| `reply_thread_with_file` | 发送文件附件 |
| `download_file` | 下载 Slack 文件到本地 |
| `react_message` | 添加 emoji reaction |
| `request_approval` | 发Gate2审批请求到审批频道 |
| `poll_approval_channel` | 轮询审批频道（持久审批监控用） |
| `request_approve_from_requester` | 向任务thread发送计划并等待确认 |
| `reply_thread_final` | 发送最终完成消息 |

**其他 MCP Servers：**

| Server | 端口 | 提供工具 |
|---|---|---|
| `GithubMcpServer` | 22202 | `merge_pr`, `get_collaborators` |
| `JenkinsMcpServer` | 22203 | `run_job`, `get_job_log`, `get_build_details` |
| `CloudConsoleMcpServer` | 22204 | 20+ 工具（Pod、部署、Pipeline...） |
| `ObsidianMcpServer` | 22205 | 知识库读写 |
| Jira（外部） | HTTP | Jira ticket CRUD |
| Confluence Wiki（外部） | HTTP | 文档读写 |
| Playwright（外部） | stdio | 浏览器自动化 |
| PII Detection（外部） | stdio | 内容脱敏 |

Slack MCP Server 始终以 **stdio** 模式运行，其他 server 默认以 **HTTP** 模式在本地端口运行。

---

## Soul 系统（Agent 人格）

4 个 agent 人格全部编码在 `.md.tpl` 模板中，通过 `--system-prompt` 注入给 Claude。不同 soul 产生完全不同的 agent 行为。

| Soul | 触发方式 | 权限模式 | MCP配置 | 职责 |
|---|---|---|---|---|
| **Lily** (`slack_support`) | HTTP `localhost:7000` | `acceptEdits` | 全部工具 | DevOps 执行，需 Gate2 审批 |
| **Anya** (`task_analyst`) | 🧠 emoji reaction | `acceptEdits`（工具受限）| 仅 Slack/Jira/PII/Glean/Wiki | 需求澄清 → 创建 Jira ticket |
| **Loid** (`loid_forge`) | Task UI "Run" 按钮 | `acceptEdits` | 全部工具 | 读 spec.md → 执行 Jira 任务 |
| **Yor** (`yor_forger`) | @mention | `dangerously-skip` | 全部工具 | 直接执行命令，无需审批 |

Anya 使用动态生成的 `settings.json`，在 `.claude/rules/` 中通过 deny 规则阻止调用 Bash/Edit/Write/Playwright 等危险工具。

---

## Gate2 审批系统

对于 Lily 执行高危操作，系统有三层保护：

**第一层 — Lily 发起**（soul.md.tpl 中定义）

```
Step A: request_approval(plan_text, thread_url)
        → 发到审批频道，获取 dm_url
Step B: poll_thread(dm_url)
        → 等待审批委员会意见
Step C: 读取委员会意见 (CLEAR / CONCERNS)
Step D: request_approve_from_requester()
        → 在任务 thread 征得 requester 最终同意
```

**第二层 — 审批委员会**（`PersistentApprovalSession` + `soul_persistent.md`）

一个长期运行的 Claude session（每2小时重启），持续监控审批频道。收到请求后串行启动 3 个 subagent：

```
Agent 1 (Analyst):  逐步分类 READ/WRITE，输出 ANALYST_VOTE: YES/NO
Agent 2 (Advocate): 基于 Analyst 结果为自动批准辩护，输出 ADVOCATE_VOTE: YES/NO
Agent 3 (Opposer):  挑战 Advocate，找隐藏风险，输出 OPPOSER_VOTE: YES/NO

三票全 YES → 发 "Team review: CLEAR"
否则        → 发 "Team review: CONCERNS"
```

**第三层 — 硬性规则**（`.claude/rules/approval-monitor.md`）

任何涉及 `prod` / `general` / `tcop` 环境的写操作，Opposer 必须投 NO，强制需要 owner 手动审批。

---

## 端到端数据流

```
用户在 Slack 发 @mention
    ↓
EventServer (slack_bolt Socket Mode WebSocket)
    ↓  event["app_mention"]
SupportTask.trigger(SlackThreadLink, soul="yor_forger")
    ↓
SupportTask.__init__()
    创建 tasks/{channel}/{ts}/yor_forger/ 目录
    resume = os.path.exists(self.home)  # 已存在则续接
    ↓
SupportTask.prepare()
    生成 session_id = uuid5(thread_url + soul)
    生成 run.sh / resume.sh
    生成 hook_session_start.sh / hook_session_end.sh
    ↓
SupportTask.run()
    ITermUtils.run_command_in_tab("/bin/bash run.sh")
    → osascript AppleScript → macOS Terminal 新标签页
        ↓
        run.sh 执行 claude CLI
            ↓
            Claude CLI 启动（MCP servers 作为子进程/HTTP server 启动）
            Claude 调用: mcp__slack__read_thread(url)
                ↓
            SlackMcpServer 接收 → SlackClient → Slack Web API
            返回 thread 消息列表
                ↓
            Claude 分析消息，执行任务（Bash / GitHub / Jenkins / ...）
            Claude 调用: mcp__slack__reply_thread("完成。")
            Claude 调用: mcp__slack__poll_thread(url)  # 等待下一条命令
                ↓
            poll_thread 每15秒轮询，最多10分钟
            新消息到达 → 返回给 Claude → 继续处理
        ↓
        run.sh 结束 → 执行 hook_session_end.sh
            → curl POST /session_end
            → HookServer 添加 :aaaa: reaction
            → SlackClient 发送 token 消耗信息
```

---

## 设计模式总结

| 模式 | 实现方式 |
|---|---|
| **Agent Runtime** | 直接 fork `claude` CLI，不自己实现推理循环 |
| **Tool Use Loop** | 完全由 Claude Code CLI 原生处理 |
| **工具总线** | MCP Protocol（stdio + HTTP 两种传输模式） |
| **Agent 人格** | System Prompt（`.md.tpl` 模板），Soul 即策略 |
| **上下文隔离** | 每任务独立工作目录 `tasks/{channel}/{ts}/{soul}/` |
| **Session 复用** | `--session-id` = `uuid5(thread_url + soul)` |
| **可观测性** | macOS Terminal 标签页可视化，可直接观察推理过程 |
| **安全控制** | Gate2 三层审批 + `.claude/rules/` 硬性规则 + soul 级别 deny 列表 |
