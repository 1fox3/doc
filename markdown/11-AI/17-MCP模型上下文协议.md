# MCP 模型上下文协议

## 核心定位

MCP，全称 Model Context Protocol，中文常译为模型上下文协议。它是一套让 AI 应用、安全地、标准化地连接外部工具和数据源的协议。

可以把 MCP 理解成 AI 应用领域的“USB-C”：模型或 Agent 不需要为每个系统单独写一套接入逻辑，而是通过统一协议连接文件系统、数据库、Git、浏览器、内部 API、监控平台等外部能力。

MCP 解决的核心问题是：

- 大模型本身只会基于上下文生成文本，不能天然访问外部系统。
- 不同工具的接入方式不统一，工程集成成本高。
- 工具调用需要权限控制、上下文隔离、审计和安全边界。
- Agent 需要稳定获取资源、调用工具、执行多步骤任务。

## 基本架构

MCP 通常包含三个角色：

| 角色 | 说明 |
| --- | --- |
| MCP Host | 用户直接使用的 AI 应用，例如 Claude Desktop、IDE 插件、代码助手、Agent 平台 |
| MCP Client | Host 内部用于连接 MCP Server 的客户端组件 |
| MCP Server | 对外暴露工具、资源和提示模板的服务端，例如文件系统 Server、Git Server、数据库 Server |

调用链路可以简化为：

```text
用户 -> MCP Host -> MCP Client -> MCP Server -> 外部系统
```

例如用户让代码助手“读取项目 README 并总结”，实际过程可能是：

```text
代码助手 Host
  -> 通过 MCP Client 调用 filesystem MCP Server
  -> filesystem MCP Server 读取本地文件
  -> 返回文件内容给模型
  -> 模型基于内容生成总结
```

## MCP Server 暴露什么

MCP Server 主要暴露三类能力：

| 能力 | 含义 | 示例 |
| --- | --- | --- |
| Resources | 可读取的上下文资源 | 文件内容、数据库表结构、日志片段、Git diff |
| Tools | 可执行的动作 | 查询数据库、创建 issue、调用内部 API、运行搜索 |
| Prompts | 可复用的提示模板 | 代码审查模板、排障模板、SQL 优化模板 |

其中最常被问到的是 `Tools`。Tool 是模型可以请求调用的外部动作，但最终是否允许执行，通常由 Host、权限配置或用户确认决定。

## 和 Function Calling 的区别

MCP 和 Function Calling 都和工具调用有关，但层次不同。

| 对比项 | Function Calling | MCP |
| --- | --- | --- |
| 关注点 | 模型如何表达“我要调用哪个函数” | AI 应用如何标准化接入外部工具和数据源 |
| 层次 | 模型 API 能力 | 应用集成协议 |
| 工具定义位置 | 通常由业务代码在请求中传给模型 | 由 MCP Server 对外暴露 |
| 复用性 | 每个应用通常各自定义工具 | 同一个 MCP Server 可被多个 Host 复用 |
| 典型例子 | OpenAI tools、Claude tool use | filesystem MCP、GitHub MCP、Postgres MCP |

简单理解：Function Calling 更像“模型决定调用函数的格式”，MCP 更像“工具生态和外部系统接入协议”。

## 和 Agent 的关系

Agent 是一种应用形态，MCP 是一种工具和上下文接入协议。

Agent 负责规划、推理、选择工具、执行多步骤任务；MCP 负责把外部工具和数据源以标准方式提供给 Agent。

它们的关系可以理解为：

```text
Agent 负责思考和决策
MCP 负责提供可调用的工具和上下文
```

例如一个代码修复 Agent 可以通过 MCP 获得这些能力：

- 读取仓库文件。
- 搜索代码符号。
- 查看 Git diff。
- 查询 issue 或 PR。
- 运行测试或调用 CI 系统。

## 典型使用场景

### 本地开发助手

IDE 或桌面 AI 助手通过 MCP 访问本地文件、Git 仓库、终端命令、包管理器和测试工具，从而完成代码解释、代码修改、测试验证和提交说明生成。

### 企业知识库

企业可以实现内部文档、Wiki、工单、监控、数据库的 MCP Server，让 AI 助手在权限范围内读取上下文，辅助问答、排障和信息检索。

### 数据分析助手

MCP Server 可以暴露数据库 schema 查询、只读 SQL 执行、报表系统查询等工具。模型负责生成查询意图，Server 负责执行受控访问并返回结果。

### 运维排障助手

MCP 可以接入日志平台、指标系统、链路追踪和发布系统。Agent 可以按步骤拉取错误日志、查询指标、定位异常版本，并生成排障建议。

## 安全边界

MCP 的工程价值不仅是“能调用工具”，还包括可控地调用工具。设计 MCP Server 时要重点关注：

- 最小权限：只暴露任务需要的资源和工具。
- 只读优先：数据库、文件、生产系统优先提供只读能力。
- 用户确认：高风险操作需要用户显式确认。
- 参数校验：不要直接信任模型生成的参数。
- 审计日志：记录谁在什么时候通过什么工具访问了什么资源。
- 上下文隔离：不同用户、项目、租户的数据不能混用。
- Prompt Injection 防护：外部文档中的恶意指令不能越权控制工具调用。

## 面试表达

可以这样回答：

```text
MCP 是 Model Context Protocol，它不是一个模型，而是 AI 应用连接外部工具和数据源的标准协议。
它把文件、数据库、Git、内部 API 等能力封装成 MCP Server 暴露的 Resources、Tools 和 Prompts，AI Host 通过 MCP Client 统一调用。
Function Calling 更偏模型 API 层的工具调用格式，MCP 更偏应用工程层的工具接入和生态复用。
在 Agent 系统里，Agent 负责规划和决策，MCP 负责提供标准化、可权限控制、可审计的外部能力。
落地时要重点关注最小权限、只读优先、用户确认、参数校验、审计和 Prompt Injection 防护。
```

## 常见误区

- MCP 不是大模型本身，也不是 RAG 框架。
- MCP 不等于 Function Calling，它可以和 Function Calling 配合使用。
- MCP Server 不应该无边界暴露系统能力，尤其不能默认开放生产写操作。
- MCP 不能替代业务权限系统，工具调用仍然要经过权限校验。
- MCP 让工具接入更标准，但不会自动保证 Agent 的规划一定正确。
