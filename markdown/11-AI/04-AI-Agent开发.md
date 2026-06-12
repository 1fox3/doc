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
2. LlamaIndex：偏数据接入和 RAG。
3. AutoGen：偏多 Agent 协作。
4. CrewAI：用角色组织多 Agent 任务。
5. Semantic Kernel：微软生态，适合和企业系统集成。

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
| LCEL | LangChain Expression Language | 用 `|` 组合链路 |

### 最小可运行环境

```bash
pip install langchain langchain-openai langchain-community python-dotenv pydantic
```

环境变量：

```bash
export OPENAI_API_KEY="你的 API Key"
```

如果使用兼容 OpenAI API 的模型网关，可以配置 `base_url`。

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,
    base_url="https://your-model-gateway/v1",  # 可选
)
```

## Demo 1：LCEL 基础链

这个 demo 展示 Prompt、Model、Parser 如何组成一条链。

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深 Java 后端面试教练，回答要具体、可落地。"),
    ("user", "请用面试表达方式解释：{topic}"),
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
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
from langchain_openai import ChatOpenAI


class TicketAnalysis(BaseModel):
    category: str = Field(description="问题分类，例如 login、payment、order、other")
    priority: str = Field(description="优先级，只能是 low、medium、high")
    summary: str = Field(description="一句话总结")
    need_human: bool = Field(description="是否需要人工介入")


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
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
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


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


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [get_order_status, create_support_ticket]

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是电商客服助手。需要查询订单时必须调用工具，不要编造订单状态。"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True,
)

result = executor.invoke({
    "input": "帮我查一下订单 A1001 为什么还没发货，如果需要人工处理就创建工单。"
})

print(result["output"])
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

下面 demo 用 `RunnableWithMessageHistory` 管理会话历史。生产中可以把历史存到 Redis 或数据库。

```python
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


@tool
def query_user_level(user_id: str) -> dict:
    """查询用户会员等级。"""
    return {"user_id": user_id, "level": "gold", "discount": "90%"}


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [query_user_level]

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是会员运营助手。回答要简洁。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=3)

agent_with_history = RunnableWithMessageHistory(
    executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

config = {"configurable": {"session_id": "user-001"}}

print(agent_with_history.invoke({"input": "我的用户 ID 是 U888，帮我查下会员等级。"}, config=config)["output"])
print(agent_with_history.invoke({"input": "那我现在有什么折扣？"}, config=config)["output"])
```

Memory 注意点：

1. 不要无限保存全部对话。
2. 敏感信息要脱敏或不入库。
3. 长会话要做摘要压缩。
4. 多租户场景必须隔离 session。

## Demo 6：LangChain RAG Agent

如果 Agent 需要查知识库，可以把 retriever 包装成 tool。

```python
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


docs = [
    Document(page_content="退款规则：普通订单支付后 7 天内可申请退款，虚拟商品不支持退款。", metadata={"source": "refund-policy"}),
    Document(page_content="发票规则：企业用户可在订单完成后 30 天内申请电子发票。", metadata={"source": "invoice-policy"}),
]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})


@tool
def search_policy(question: str) -> str:
    """查询公司订单、退款、发票相关政策。"""
    matched_docs = retriever.invoke(question)
    return "\n\n".join(
        f"来源：{doc.metadata['source']}\n内容：{doc.page_content}"
        for doc in matched_docs
    )


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [search_policy]

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是客服知识库助手。涉及政策问题必须调用 search_policy，并基于检索结果回答。"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=3)

result = executor.invoke({"input": "虚拟商品可以退款吗？"})
print(result["output"])
```

真实项目中，`search_policy` 内部还应该做：

1. 用户权限过滤。
2. 租户隔离。
3. metadata filter。
4. rerank。
5. 来源引用返回。

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
