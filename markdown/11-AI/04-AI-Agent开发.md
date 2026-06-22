# AI Agent 开发

## Agent 是什么

AI Agent 是能围绕目标进行多步骤推理、调用工具、观察结果并继续行动的 AI 应用形态。

普通 Chatbot 通常是“用户问，模型答”。Agent 更强调“目标驱动 + 工具调用 + 多步骤执行”。

## Agent 典型流程

```text
用户目标 -> 任务理解 -> 计划 -> 工具调用 -> 观察结果 -> 调整计划 -> 输出结果
```

例如“帮我分析这周线上错误并生成报告”：

1. 查询日志平台。
2. 聚合错误类型。
3. 查询发布记录。
4. 判断可能原因。
5. 生成报告和建议。

## Tool Calling

Tool Calling 是让模型选择并调用外部工具，例如搜索、数据库查询、发邮件、创建工单。

关键点：

1. 工具 schema 要清晰，参数类型要明确。
2. 工具执行必须在后端完成，不能让模型直接拥有权限。
3. 工具返回结果要结构化，避免长文本噪声。
4. 高风险工具要二次确认或人工审批。

## Function Calling

Function Calling 通常是模型输出函数名和参数，由业务服务执行函数。

适合：

1. 查询订单状态。
2. 创建日程。
3. 调用内部 API。
4. 抽取结构化字段。
5. 执行确定性计算。

## Planning

Planning 是让 Agent 把目标拆成步骤。

常见方式：

1. 一次性计划：先生成完整计划再执行。
2. 边执行边计划：每一步根据工具结果调整。
3. 固定流程编排：业务代码定义流程，模型只负责某些节点。

生产环境更推荐固定流程编排和有限自主性，避免 Agent 无限循环或做出不可控动作。

## Memory

Memory 用来保存上下文或长期偏好。

类型：

1. 短期记忆：当前会话上下文。
2. 长期记忆：用户偏好、历史任务、知识沉淀。
3. 工作记忆：Agent 当前任务状态。

注意：

1. 长期记忆需要用户授权和可删除能力。
2. 敏感信息不能随意写入记忆。
3. 记忆需要检索和压缩，否则会污染上下文。

## Reflection

Reflection 是让模型检查自己的中间结果或最终答案。

适合：

1. 代码生成后自检。
2. 多步骤推理后检查遗漏。
3. 输出前检查格式和约束。

注意：Reflection 会增加成本和延迟，不适合所有链路。

## 单 Agent 与多 Agent

单 Agent 简单可控，适合大多数业务。

多 Agent 把角色拆开，例如规划 Agent、检索 Agent、审核 Agent、执行 Agent。

多 Agent 风险：

1. 成本更高。
2. 延迟更高。
3. 调试困难。
4. 错误可能在多个 Agent 间传递。

工程上不要为了概念使用多 Agent，除非角色拆分确实带来可维护性或质量提升。

## 适合 Agent 的场景

1. 多步骤任务。
2. 需要调用多个工具。
3. 目标明确但路径不固定。
4. 对延迟不极端敏感。
5. 可接受人工确认或回滚。

不适合：

1. 支付、转账、删库等高风险动作。
2. 强实时低延迟链路。
3. 规则非常明确的流程。
4. 错误成本极高且不可回滚的场景。

## 常见框架

1. LangChain：生态丰富，适合快速搭建链和 Agent。
2. LangGraph：基于状态图编排 Agent，适合需要可控流程、循环、分支和持久化状态的场景。
3. LangSmith：LangChain 生态的可观测、调试、评估和数据集管理平台。
4. LangServe：把 LangChain Runnable 快速发布成 HTTP API 的服务化工具。
5. Deep Agents：LangChain 生态中面向复杂长任务的 Agent 方案，强调计划、子 Agent、上下文工程和持久化工作区。
6. LlamaIndex：偏数据接入和 RAG。
7. AutoGen：偏多 Agent 协作。
8. CrewAI：用角色组织多 Agent 任务。
9. Semantic Kernel：微软生态，适合和企业系统集成。

面试时不要只说框架，要说清楚框架背后的核心能力：Prompt 编排、工具调用、记忆、检索、评估和监控。

## LangChain 重点实战

LangChain 是一个 LLM 应用开发框架，核心价值不是“让模型更聪明”，而是把 Prompt、模型、工具、检索、记忆、输出解析和执行流程组织成可维护的应用代码。

### LangChain 核心模块

| 模块 | 作用 | 面试表达 |
| --- | --- | --- |
| ChatModel | 对接 OpenAI、Claude、本地模型等 | 统一模型调用接口 |
| PromptTemplate | 管理 Prompt 模板 | 把提示词版本化和参数化 |
| OutputParser | 解析模型输出 | JSON、Pydantic、字符串解析 |
| Tool | 封装外部能力 | 数据库、搜索、HTTP API、业务函数 |
| Agent | 让模型选择工具并执行多步骤任务 | 适合路径不固定的任务 |
| Retriever | 检索相关文档 | RAG 核心组件 |
| VectorStore | 向量库抽象 | FAISS、Chroma、Milvus 等 |
| Memory | 保存会话状态 | 多轮对话和用户偏好 |
| LCEL | LangChain Expression Language | 用 `\|` 组合链路 |

### 最小可运行环境

```bash
pip install langchain langchain-ollama langchain-chroma langgraph langsmith langserve fastapi uvicorn deepagents python-dotenv pydantic
```

Ollama 在本地运行，无需 API Key。确保已启动 Ollama 并拉取模型：

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    temperature=0.1,
)
```

## Demo 1：LCEL 基础链

这个 demo 展示 Prompt、Model、Parser 如何组成一条链。

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深 Java 后端面试教练，回答要具体、可落地。"),
    ("user", "请用面试表达方式解释：{topic}"),
])

llm = ChatOllama(model="llama3.2", temperature=0.2)
parser = StrOutputParser()

chain = prompt | llm | parser

result = chain.invoke({"topic": "RAG 如何降低幻觉"})
print(result)
```

这类链适合：

1. 总结。
2. 改写。
3. 分类。
4. 简单问答。
5. 结构化抽取前的轻量处理。

## Demo 2：结构化输出

生产中不要让模型随便输出文本。如果后续程序要消费结果，应该用结构化输出。

```python
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


class TicketAnalysis(BaseModel):
    category: str = Field(description="问题分类，例如 login、payment、order、other")
    priority: str = Field(description="优先级，只能是 low、medium、high")
    summary: str = Field(description="一句话总结")
    need_human: bool = Field(description="是否需要人工介入")


llm = ChatOllama(model="llama3.2", temperature=0)
structured_llm = llm.with_structured_output(TicketAnalysis)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是客服工单分析助手。请按 schema 输出。"),
    ("user", "工单内容：{content}"),
])

chain = prompt | structured_llm

result = chain.invoke({
    "content": "用户反馈支付成功但订单状态还是待支付，已经等待 30 分钟。"
})

print(result)
print(result.category, result.priority, result.need_human)
```

工程要点：

1. Pydantic schema 是服务端约束，不只是 Prompt 约束。
2. 解析失败要重试或降级。
3. 关键枚举值仍建议二次校验。

## Demo 3：自定义 Tool

Tool 是 Agent 能做事的边界。模型只能“请求调用工具”，真正执行工具的是后端代码。

下面模拟两个业务工具：查询订单和创建客服工单。

```python
from langchain_core.tools import tool


ORDERS = {
    "A1001": {"status": "paid", "amount": 199, "delivery": "not_shipped"},
    "A1002": {"status": "refunded", "amount": 88, "delivery": "cancelled"},
}


@tool
def get_order_status(order_id: str) -> dict:
    """根据订单 ID 查询订单状态。"""
    return ORDERS.get(order_id, {"error": "order_not_found"})


@tool
def create_support_ticket(order_id: str, reason: str) -> dict:
    """为指定订单创建客服工单。仅在需要人工处理时调用。"""
    return {
        "ticket_id": f"T-{order_id}",
        "order_id": order_id,
        "reason": reason,
        "status": "created",
    }


tools = [get_order_status, create_support_ticket]
```

Tool 设计原则：

1. 函数名要表达动作。
2. docstring 要说明什么时候调用。
3. 参数尽量少且类型明确。
4. 返回结构化结果。
5. 工具内部做权限、幂等和审计。

## Demo 4：LangChain Agent 调用工具

这个 demo 让模型根据用户问题决定是否调用工具。

```python
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama


ORDERS = {
    "A1001": {"status": "paid", "amount": 199, "delivery": "not_shipped"},
    "A1002": {"status": "refunded", "amount": 88, "delivery": "cancelled"},
}


@tool
def get_order_status(order_id: str) -> dict:
    """根据订单 ID 查询订单状态。"""
    return ORDERS.get(order_id, {"error": "order_not_found"})


@tool
def create_support_ticket(order_id: str, reason: str) -> dict:
    """为指定订单创建客服工单。仅在需要人工处理时调用。"""
    return {
        "ticket_id": f"T-{order_id}",
        "order_id": order_id,
        "reason": reason,
        "status": "created",
    }


llm = ChatOllama(model="llama3.2", temperature=0)
tools = [get_order_status, create_support_ticket]

agent = create_agent(
    llm,
    tools,
    system_prompt="你是电商客服助手。需要查询订单时必须调用工具，不要编造订单状态。",
)

result = agent.invoke(
    {"messages": [("user", "帮我查一下订单 A1001 为什么还没发货，如果需要人工处理就创建工单。")]},
    config={"configurable": {"thread_id": "demo-4"}},
)

print(result["messages"][-1].content)
```

执行过程通常是：

1. LLM 判断需要查询订单。
2. Agent 调用 `get_order_status`。
3. LLM 观察到订单已支付但未发货。
4. LLM 判断需要人工处理。
5. Agent 调用 `create_support_ticket`。
6. LLM 汇总结果给用户。

生产配置建议：

1. `max_iterations` 必须设置，避免无限循环。
2. 工具调用要记录审计日志。
3. 高风险工具不要直接执行，先返回确认卡片。
4. Tool 返回不要太长，避免污染上下文。

## Demo 5：带 Memory 的多轮对话 Agent

下面 demo 用 `create_agent` 内置的 checkpointer 管理会话历史，通过 `thread_id` 隔离会话。生产中可以自定义 checkpointer 对接 Redis、数据库。

```python
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama


@tool
def query_user_level(user_id: str) -> dict:
    """查询用户会员等级。"""
    return {"user_id": user_id, "level": "gold", "discount": "90%"}


llm = ChatOllama(model="llama3.2", temperature=0)
tools = [query_user_level]

agent = create_agent(
    llm,
    tools,
    system_prompt="你是会员运营助手。回答要简洁。",
)

config = {"configurable": {"thread_id": "user-001"}}

result1 = agent.invoke(
    {"messages": [("user", "我的用户 ID 是 U888，帮我查下会员等级。")]},
    config=config,
)
print(result1["messages"][-1].content)

result2 = agent.invoke(
    {"messages": [("user", "那我现在有什么折扣？")]},
    config=config,
)
print(result2["messages"][-1].content)
```

Memory 注意点：

1. 不要无限保存全部对话。
2. 敏感信息要脱敏或不入库。
3. 长会话要做摘要压缩。
4. 多租户场景必须隔离 session。

## Demo 6：LangChain RAG Agent

如果 Agent 需要查知识库，可以把 retriever 包装成 tool。

```python
from langchain.agents import create_agent
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_ollama import ChatOllama, OllamaEmbeddings


docs = [
    Document(page_content="退款规则：普通订单支付后 7 天内可申请退款，虚拟商品不支持退款。", metadata={"source": "refund-policy"}),
    Document(page_content="发票规则：企业用户可在订单完成后 30 天内申请电子发票。", metadata={"source": "invoice-policy"}),
]

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})


@tool
def search_policy(question: str) -> str:
    """查询公司订单、退款、发票相关政策。"""
    matched_docs = retriever.invoke(question)
    return "\n\n".join(
        f"来源：{doc.metadata['source']}\n内容：{doc.page_content}"
        for doc in matched_docs
    )


llm = ChatOllama(model="llama3.2", temperature=0)
tools = [search_policy]

agent = create_agent(
    llm,
    tools,
    system_prompt="你是客服知识库助手。涉及政策问题必须调用 search_policy，并基于检索结果回答。",
)

result = agent.invoke(
    {"messages": [("user", "虚拟商品可以退款吗？")]},
    config={"configurable": {"thread_id": "demo-6"}},
)
print(result["messages"][-1].content)
```

真实项目中，`search_policy` 内部还应该做：

1. 用户权限过滤。
2. 租户隔离。
3. metadata filter。
4. rerank。
5. 来源引用返回。

## LangGraph 重点实战

LangGraph 是 LangChain 生态里的 Agent 编排框架，核心不是再封装一个 Prompt Chain，而是把 Agent 执行过程建模成“状态图”。每个节点处理一部分逻辑，边决定下一步走向，状态在节点之间传递。

可以这样理解：

| 对比项 | LangChain AgentExecutor | LangGraph |
| --- | --- | --- |
| 核心抽象 | Agent 执行器 | StateGraph 状态图 |
| 流程控制 | 主要由 Agent 自主决定 | 代码显式定义节点、边、条件分支 |
| 适合场景 | 简单工具调用、多步骤问答 | 复杂 Agent、循环、自检、人工确认、多阶段工作流 |
| 可控性 | 中等 | 更高 |
| 状态管理 | 依赖 Memory 或外部封装 | 状态是一等公民 |
| 调试方式 | 看 Agent scratchpad 和 callbacks | 看图上的节点输入输出和状态变化 |

LangGraph 适合：

1. 需要明确流程边界的 Agent。
2. 需要循环执行直到满足条件的任务。
3. 需要人工审批或人工介入的任务。
4. 需要在多个节点之间保存结构化状态。
5. 需要把 RAG、工具调用、反思、自检、总结拆成多个可观测节点。

不建议使用 LangGraph 的场景：

1. 一次 Prompt 就能完成的简单任务。
2. 只有一个工具调用的轻量 Agent。
3. 团队还没有 tracing、测试和状态设计能力时，不要过早引入复杂图。

## Demo 7：LangGraph 固定状态图

这个 demo 用 LangGraph 实现一个可控的客服流程：先查订单，再根据订单状态决定是否创建工单，最后生成回复。

```python
from langgraph.graph import END, StateGraph
from pydantic import BaseModel


ORDERS = {
    "A1001": {"status": "paid", "amount": 199, "delivery": "not_shipped"},
    "A1002": {"status": "refunded", "amount": 88, "delivery": "cancelled"},
}


class CustomerServiceState(BaseModel):
    order_id: str = ""
    order: dict = {}
    ticket: dict | None = None
    answer: str = ""


def query_order(state: CustomerServiceState) -> dict:
    order = ORDERS.get(state.order_id, {"error": "order_not_found"})
    return {"order": order}


def need_ticket(state: CustomerServiceState) -> str:
    if state.order.get("status") == "paid" and state.order.get("delivery") == "not_shipped":
        return "create_ticket"
    return "generate_answer"


def create_ticket(state: CustomerServiceState) -> dict:
    ticket = {
        "ticket_id": f"T-{state.order_id}",
        "order_id": state.order_id,
        "reason": "订单已支付但未发货，需要人工跟进",
        "status": "created",
    }
    return {"ticket": ticket}


def generate_answer(state: CustomerServiceState) -> dict:
    if state.order.get("error") == "order_not_found":
        answer = f"没有查询到订单 {state.order_id}。"
    elif state.ticket:
        answer = (
            f"订单 {state.order_id} 已支付但还未发货，"
            f"已创建工单 {state.ticket['ticket_id']}，客服会继续跟进。"
        )
    else:
        answer = f"订单 {state.order_id} 当前状态：{state.order}。"
    return {"answer": answer}


workflow = StateGraph(CustomerServiceState)
workflow.add_node("query_order", query_order)
workflow.add_node("create_ticket", create_ticket)
workflow.add_node("generate_answer", generate_answer)

workflow.set_entry_point("query_order")
workflow.add_conditional_edges(
    "query_order",
    need_ticket,
    {
        "create_ticket": "create_ticket",
        "generate_answer": "generate_answer",
    },
)
workflow.add_edge("create_ticket", "generate_answer")
workflow.add_edge("generate_answer", END)

app = workflow.compile()

result = app.invoke(CustomerServiceState(order_id="A1001"))

print(result["answer"])
```

这个例子的关键点：

1. `CustomerServiceState` 是整个图共享的状态。
2. `query_order`、`create_ticket`、`generate_answer` 是图上的节点。
3. `need_ticket` 是条件路由函数，决定下一步走哪条边。
4. 业务流程由代码控制，不完全交给模型自由发挥。
5. 每个节点输入输出都可测试、可观测、可审计。

## Demo 8：手写 LangGraph ReAct Agent

`create_agent` 内部实际上是一个 StateGraph：LLM 节点调用模型，工具节点执行工具调用，条件边决定是否继续循环。这个 demo 手动拆开这个结构，让执行过程完全可控、可观测。

```python
from typing import Literal

from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode


ORDERS = {
    "A1001": {"status": "paid", "amount": 199, "delivery": "not_shipped"},
    "A1002": {"status": "refunded", "amount": 88, "delivery": "cancelled"},
}


@tool
def get_order_status(order_id: str) -> dict:
    """根据订单 ID 查询订单状态。"""
    return ORDERS.get(order_id, {"error": "order_not_found"})


@tool
def create_support_ticket(order_id: str, reason: str) -> dict:
    """为指定订单创建客服工单。仅在需要人工处理时调用。"""
    return {
        "ticket_id": f"T-{order_id}",
        "order_id": order_id,
        "reason": reason,
        "status": "created",
    }


tools = [get_order_status, create_support_ticket]
llm = ChatOllama(model="llama3.2", temperature=0)
llm_with_tools = llm.bind_tools(tools)


def call_llm(state: MessagesState) -> dict:
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    if state["messages"][-1].tool_calls:
        return "tools"
    return END


tool_node = ToolNode(tools)

workflow = StateGraph(MessagesState)
workflow.add_node("llm", call_llm)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("llm")
workflow.add_conditional_edges("llm", should_continue)
workflow.add_edge("tools", "llm")

app = workflow.compile()

result = app.invoke({
    "messages": [("user", "帮我查一下订单 A1001 为什么还没发货，如果需要人工处理就创建工单。")]
})

print(result["messages"][-1].content)
```

图的结构：

```text
用户输入 → llm → 有 tool_calls？
                   ├─ 是 → tools → llm（循环）
                   └─ 否 → END
```

和 `create_agent` 的区别：

1. `llm.bind_tools(tools)` 显式把工具 schema 注入模型，这一步 `create_agent` 内部也在做。
2. `should_continue` 是条件边，控制循环退出，可以在这里插入步骤计数、风险检查、人工确认等逻辑。
3. `ToolNode` 负责解析 `tool_calls` 并执行，结果作为 `ToolMessage` 追加到消息列表。
4. 整个执行路径在图上可见，每个节点可以单独测试和替换。

生产建议：

1. 在 `should_continue` 里加最大步骤计数，防止无限循环。
2. 高风险工具在 `tools` 节点前插入人工确认节点。
3. 需要持久化会话时在 `compile()` 传入 checkpointer。
4. 每个节点单独写单元测试，不要只测最终输出。

## LangGraph 面试讲法

可以这样回答：

> LangGraph 是 LangChain 生态里更偏工程化的 Agent 编排框架。LangChain AgentExecutor 更像一个黑盒执行器，而 LangGraph 把 Agent 拆成状态、节点和边，可以显式控制分支、循环、人工确认和失败恢复。生产里我会把确定性流程写成 StateGraph，把模型能力放在某些节点里，把工具调用、RAG、自检和总结拆开，这样可观测、可测试，也更容易控制风险。

## LangSmith 重点实战

LangSmith 是 LangChain 生态里的可观测、调试和评估平台。它解决的不是“怎么调用模型”，而是“调用之后如何知道链路对不对、慢在哪里、贵在哪里、坏 case 为什么坏”。

LangSmith 常用于：

1. 记录每次 LLM 调用、Prompt、输入、输出、token、延迟和错误。
2. 查看 Chain、Agent、Tool、Retriever 的完整执行轨迹。
3. 建立测试数据集，对 Prompt、模型、RAG 策略做回归评估。
4. 对线上 bad case 做标注、复盘和优化。
5. 对不同模型或 Prompt 版本做对比实验。

生产中尤其要关注：

1. 是否记录敏感信息。
2. 是否做脱敏和采样。
3. Trace ID 是否能和业务日志串起来。
4. 是否有离线评估集，而不是只靠人工感觉。

### LangSmith 环境变量

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY="你的 LangSmith API Key"
export LANGSMITH_PROJECT="agent-demo"
```

如果团队使用自建观测系统，也可以借鉴 LangSmith 的思想：记录 trace、run、span、输入输出、工具调用、检索结果和评估指标。

## Demo 9：LangSmith 追踪 LCEL Chain

开启环境变量后，LangChain 的 Runnable 调用会自动上报 trace。

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深 AI 应用架构师，回答要具体。"),
    ("user", "请解释：{question}"),
])

llm = ChatOllama(model="llama3.2", temperature=0.2)
chain = prompt | llm | StrOutputParser()

result = chain.invoke(
    {"question": "为什么 Agent 需要设置最大迭代次数？"},
    config={
        "run_name": "agent_question_chain",
        "tags": ["demo", "agent", "interview"],
        "metadata": {"biz": "ai-interview-doc"},
    },
)

print(result)
```

这个 demo 在 LangSmith 中可以看到：

1. `prompt` 的实际渲染内容。
2. `llm` 的输入和输出。
3. token 用量和延迟。
4. 调用链路的层级结构。
5. 自定义 `tags` 和 `metadata`。

## Demo 10：LangSmith 数据集评估

下面示例演示如何对一个 Chain 做批量评估。真实项目中可以把历史 bad case、人工标注样本、线上高频问题沉淀成数据集。

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langsmith import Client
from langsmith.evaluation import evaluate


client = Client()
dataset_name = "agent-interview-qa"

if not client.has_dataset(dataset_name=dataset_name):
    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="Agent 面试问答回归测试集",
    )
    client.create_examples(
        dataset_id=dataset.id,
        examples=[
            {
                "inputs": {"question": "Agent 和普通 Chatbot 有什么区别？"},
                "outputs": {"answer_keywords": ["多步骤", "工具调用", "目标驱动"]},
            },
            {
                "inputs": {"question": "生产环境如何控制 Agent 风险？"},
                "outputs": {"answer_keywords": ["权限", "最大步骤", "审计", "人工确认"]},
            },
        ],
    )

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是 AI Agent 面试教练，回答要覆盖关键点。"),
    ("user", "{question}"),
])

chain = prompt | ChatOllama(model="llama3.2", temperature=0) | StrOutputParser()


def target(inputs: dict) -> dict:
    return {"answer": chain.invoke(inputs)}


def keyword_score(outputs: dict, reference_outputs: dict) -> dict:
    answer = outputs["answer"]
    keywords = reference_outputs["answer_keywords"]
    hit_count = sum(1 for keyword in keywords if keyword in answer)
    return {
        "key": "keyword_recall",
        "score": hit_count / len(keywords),
        "comment": f"hit {hit_count}/{len(keywords)} keywords",
    }


results = evaluate(
    target,
    data=dataset_name,
    evaluators=[keyword_score],
    experiment_prefix="agent-interview-chain",
)

print(results)
```

评估要点：

1. 评估集要来自真实业务问题和 bad case。
2. 评估指标可以是规则、人工、LLM-as-judge 或混合方式。
3. Prompt、模型、检索参数变更后要跑回归评估。
4. 不要只看平均分，还要看失败样本和错误类型。

## LangSmith 面试讲法

可以这样回答：

> LangSmith 主要解决 LLM 应用的可观测和评估问题。做 Agent 时我会记录每一步模型调用、工具调用、检索结果、token、延迟和错误，并把线上 bad case 沉淀成评估集。每次改 Prompt、换模型或调整 RAG 参数，都用评估集做回归测试，避免只凭主观感觉上线。

## LangServe 重点实战

LangServe 用来把 LangChain Runnable 发布成 HTTP API。它基于 FastAPI，可以快速给 Chain、Agent、RAG 应用生成标准接口，方便前后端或其他服务调用。

LangServe 适合：

1. 快速把内部 Chain 暴露成服务。
2. 给前端、后端、测试工具提供统一 HTTP 接口。
3. 在 demo、PoC、内部平台中快速验证 LLM 应用。
4. 配合模型网关、鉴权、限流、日志和监控做服务化。

LangServe 不等于完整生产网关。生产环境仍然需要额外处理鉴权、租户隔离、限流、审计、超时、降级和敏感信息脱敏。

## Demo 11：LangServe 发布 LCEL Chain

创建 `server.py`：

```python
from fastapi import FastAPI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langserve import add_routes


prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深 Java 后端面试教练，回答要结构化。"),
    ("user", "请解释：{topic}"),
])

chain = prompt | ChatOllama(model="llama3.2", temperature=0.2) | StrOutputParser()

app = FastAPI(title="AI Agent Demo API")

add_routes(
    app,
    chain,
    path="/interview",
)
```

启动服务：

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

调用接口：

```bash
curl http://localhost:8000/interview/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "topic": "LangGraph 和 AgentExecutor 的区别"
    }
  }'
```

LangServe 常见接口：

| 接口 | 作用 |
| --- | --- |
| `/invoke` | 普通同步调用 |
| `/batch` | 批量调用 |
| `/stream` | 流式返回最终输出片段 |
| `/stream_log` | 流式返回中间步骤和日志 |
| `/playground` | 浏览器调试页面 |

## Demo 12：LangServe 发布 Agent

下面示例把前面的工具调用 Agent 发布成 HTTP API。

```python
from fastapi import FastAPI
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langserve import add_routes


ORDERS = {
    "A1001": {"status": "paid", "amount": 199, "delivery": "not_shipped"},
    "A1002": {"status": "refunded", "amount": 88, "delivery": "cancelled"},
}


@tool
def get_order_status(order_id: str) -> dict:
    """根据订单 ID 查询订单状态。"""
    return ORDERS.get(order_id, {"error": "order_not_found"})


llm = ChatOllama(model="llama3.2", temperature=0)
agent = create_agent(
    llm,
    [get_order_status],
    system_prompt="你是电商客服助手。涉及订单状态时必须调用工具。",
)

app = FastAPI(title="Customer Service Agent API")
add_routes(app, agent, path="/agent")
```

调用接口：

```bash
curl http://localhost:8000/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [
        ["user", "帮我查一下订单 A1001 的状态。"]
      ]
    }
  }'
```

生产建议：

1. 不要裸露 LangServe 到公网。
2. 在外层加 API 网关、鉴权、限流和审计。
3. 对输入输出做脱敏和长度限制。
4. 对工具调用加权限校验和幂等控制。
5. 对慢请求配置超时和异步任务化。

## LangServe 面试讲法

可以这样回答：

> LangServe 是把 LangChain Runnable 服务化的工具，可以快速把 Chain、Agent 或 RAG 应用发布成 HTTP API，支持 invoke、batch、stream 和 playground。它适合内部平台和快速服务化，但生产环境还需要配合 API 网关做鉴权、限流、审计、脱敏、超时和降级，不能直接把模型能力裸露出去。

## Deep Agents 重点实战

Deep Agents 是 LangChain 生态中面向复杂长任务的 Agent 方案。它关注的不是单轮工具调用，而是更接近“长任务助手”：能规划任务、拆分子任务、调用子 Agent、维护上下文，并在一个工作区里持续产出结果。

可以把 Deep Agents 理解为：

1. 比普通 ReAct Agent 更适合复杂任务。
2. 比手写所有 LangGraph 节点更快搭建复杂 Agent。
3. 适合研究、代码分析、文档生成、竞品分析、报告生成等长任务。
4. 核心仍然要控制工具权限、上下文、步骤数和输出质量。

Deep Agents 常见能力：

| 能力 | 说明 |
| --- | --- |
| Planning | 先规划任务，再分步执行 |
| Sub Agents | 把研究、写作、审核等角色拆给子 Agent |
| File System | 使用虚拟工作区保存中间文件和最终产物 |
| Context Engineering | 控制哪些上下文进入模型，避免上下文污染 |
| Long-running Tasks | 支持更长链路的任务执行和状态保留 |

适合场景：

1. “分析一个主题并生成报告”。
2. “阅读多份文档并产出对比结论”。
3. “规划一个功能实现方案并生成任务清单”。
4. “调用多个工具完成一段较长研究任务”。

不适合场景：

1. 强确定性业务流程。
2. 低延迟在线请求。
3. 高风险自动执行动作。
4. 简单分类、抽取、改写任务。

## Demo 13：Deep Agents 研究助手

下面示例构建一个简单研究助手，用工具查询资料，再输出 Markdown 报告。

```python
from deepagents import create_deep_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama


@tool
def search_internal_docs(query: str) -> str:
    """查询内部 AI 应用文档。"""
    docs = {
        "agent": "Agent 适合多步骤、工具调用、路径不固定的任务。生产中要限制权限、步骤数和工具范围。",
        "rag": "RAG 通过检索外部知识补充上下文，降低幻觉，但需要关注召回、重排和引用来源。",
        "langgraph": "LangGraph 用状态图编排 Agent，适合分支、循环、人工确认和复杂工作流。",
    }
    matched = [content for key, content in docs.items() if key in query.lower()]
    return "\n".join(matched) or "没有找到相关文档。"


instructions = """
你是 AI 应用研究助手。
工作方式：
1. 先理解用户目标并制定简短计划。
2. 必要时调用 search_internal_docs 查询资料。
3. 最终输出 Markdown 报告，包含结论、关键点和工程建议。
4. 不要编造工具没有返回的信息。
"""

agent = create_deep_agent(
    model=ChatOllama(model="llama3.2", temperature=0.2),
    tools=[search_internal_docs],
    instructions=instructions,
)

result = agent.invoke({
    "messages": [
        ("user", "请分析 Agent、RAG、LangGraph 在企业知识库问答系统中的分工，并给出建议。")
    ]
})

print(result["messages"][-1].content)
```

这个 demo 的重点：

1. `instructions` 定义长任务的工作方式。
2. `tools` 提供外部资料入口。
3. Deep Agent 负责规划、调用工具和组织最终报告。
4. 真实项目中工具可以替换为搜索、RAG、数据库、代码仓库分析等能力。

## Demo 14：Deep Agents 子 Agent 分工

复杂任务可以拆给不同子 Agent，例如研究员、写作者、审稿人。

```python
from deepagents import create_deep_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama


@tool
def search_policy_docs(query: str) -> str:
    """查询产品政策文档。"""
    return "退款政策：普通订单 7 天内可退，虚拟商品不支持退款。发票政策：订单完成后 30 天内可申请电子发票。"


subagents = [
    {
        "name": "researcher",
        "description": "负责查询资料、提炼事实，不负责最终写作。",
        "prompt": "你是资料研究员。只基于工具结果总结事实，避免扩展猜测。",
    },
    {
        "name": "reviewer",
        "description": "负责检查最终答案是否遗漏约束、是否有编造。",
        "prompt": "你是审核员。检查回答是否基于事实、是否包含风险提示。",
    },
]

agent = create_deep_agent(
    model=ChatOllama(model="llama3.2", temperature=0),
    tools=[search_policy_docs],
    instructions="你是客服知识库分析助手。先研究资料，再生成给客服团队使用的 SOP。",
    subagents=subagents,
)

result = agent.invoke({
    "messages": [
        ("user", "请根据政策文档生成一份退款和发票问题的客服 SOP。")
    ]
})

print(result["messages"][-1].content)
```

设计子 Agent 时要注意：

1. 子 Agent 角色要少而清晰。
2. 不要为了概念拆太多角色。
3. 每个子 Agent 的输入、输出和权限要明确。
4. 审核 Agent 不能代替服务端规则校验。
5. 成本和延迟会随着子 Agent 数量上升。

## Deep Agents 面试讲法

可以这样回答：

> Deep Agents 更适合复杂长任务，比如研究报告、代码分析、文档生成这类需要规划、工具调用、子任务分工和中间状态管理的场景。它不是替代工作流引擎，也不适合低延迟、高风险的在线链路。生产使用时我会限制工具权限和最大步骤，把关键中间产物落盘或持久化，并用 LangSmith 观察 trace 和评估效果。

## LangChain 工程分层

推荐目录结构：

```text
ai-app/
├── app.py
├── chains/
│   ├── ticket_chain.py
│   └── summary_chain.py
├── agents/
│   └── customer_service_agent.py
├── tools/
│   ├── order_tool.py
│   └── ticket_tool.py
├── retrievers/
│   └── policy_retriever.py
├── prompts/
│   └── customer_service.md
├── schemas/
│   └── ticket.py
└── observability/
    └── callbacks.py
```

分层原则：

1. Prompt 单独管理，便于版本化。
2. Tool 是业务边界，内部做鉴权和审计。
3. Chain 负责稳定流程。
4. Agent 只用于路径不固定的任务。
5. Retriever 独立封装，便于替换向量库和 rerank。
6. Schema 独立定义，便于输出校验。

## LangChain 生产风险

### 版本变化快

LangChain API 变化较快，生产项目要锁定版本，并对关键链路写回归测试。

### Agent 不可控

Agent 可能选错工具、重复调用、漏调用或循环。必须设置最大步数、超时、工具权限和审计。

### 抽象过重

简单任务不要强行 Agent 化。普通 Prompt Chain 能解决的问题，不要引入复杂 Agent。

### 调试困难

建议打开 tracing 或接入 LangSmith，至少记录 prompt、tool call、retrieval result、latency 和 token usage。

## LangChain 面试讲法

可以这样回答：

> 我用 LangChain 主要是做 LLM 应用编排，不是依赖它提升模型本身能力。简单任务用 LCEL 把 Prompt、Model、Parser 串起来；需要结构化结果时用 Pydantic schema；需要外部系统能力时把业务 API 封装成 Tool；路径不固定的任务才用 AgentExecutor，并设置 max iterations、权限校验和审计日志。知识库场景会把 Retriever 包装成工具，结合 RAG 和 Agent 完成问答或多步骤任务。

## 面试常问

### Agent 和普通 Chatbot 有什么区别？

Chatbot 主要是问答，Agent 是围绕目标做多步骤执行，可以规划任务、调用工具、观察结果并继续调整。Agent 能力更强，但成本、延迟和不可控风险也更高。

### 生产环境如何控制 Agent 风险？

我会限制工具权限，给工具加 schema 和参数校验，对高风险动作加人工确认，设置最大步骤数和超时，记录完整审计日志，并对输出结果做校验和降级处理。

### Agent 会不会替代工作流引擎？

不会完全替代。规则明确、状态严格、合规要求高的流程更适合传统工作流。Agent 适合处理非结构化输入、多工具探索和路径不固定的任务。实际系统中常见做法是工作流控制主流程，Agent 处理智能节点。
