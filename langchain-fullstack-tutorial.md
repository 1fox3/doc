# LangChain 全家桶教学

本文是一份面向实战的 LangChain 教程，覆盖 LangChain 核心概念、LCEL、Prompt、Model、Output Parser、Memory、RAG、Tool、Agent、LangGraph、评估、部署与工程化建议。

> 适合对象：已经会 Python，想系统掌握 LLM 应用开发的人。

---

## 1. LangChain 是什么

LangChain 是一个用于构建 LLM 应用的开发框架。它本身不是大模型，而是帮助你把大模型、提示词、工具、检索、记忆、工作流和外部系统组合起来。

典型应用包括：

- 智能问答助手
- 企业知识库 RAG
- AI Agent
- 文档分析
- 自动化工作流
- SQL / API / 文件操作助手
- 多步骤推理系统

LangChain 生态主要包含：

- `langchain-core`：核心抽象，如 Prompt、Runnable、Parser
- `langchain`：高级链、Agent、Memory 等能力
- `langchain-community`：社区集成，如向量库、Loader、工具
- `langchain-openai`：OpenAI 模型集成
- `langchain-anthropic`：Anthropic 模型集成
- `langgraph`：可控、多步骤、状态化 Agent 工作流
- `langsmith`：调试、追踪、评估平台

---

## 2. 环境安装

推荐使用 Python 3.10+。

```bash
pip install -U langchain langchain-core langchain-community langchain-openai langgraph langsmith
```

如果使用 OpenAI：

```bash
export OPENAI_API_KEY="你的 API Key"
```

如果使用 `.env`：

```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv

load_dotenv()
```

---

## 3. 第一个 LangChain 程序

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

response = llm.invoke("用一句话解释 LangChain 是什么")
print(response.content)
```

核心点：

- `ChatOpenAI` 是聊天模型封装
- `invoke()` 是同步调用
- 返回值通常是一个 `AIMessage`
- 真实文本在 `response.content` 中

---

## 4. LangChain 核心抽象

LangChain 里最重要的抽象是 `Runnable`。

常见 Runnable：

- PromptTemplate
- ChatPromptTemplate
- ChatModel
- OutputParser
- Retriever
- Tool
- Chain

Runnable 常用方法：

- `invoke(input)`：单次调用
- `batch(inputs)`：批量调用
- `stream(input)`：流式输出
- `ainvoke(input)`：异步调用
- `abatch(inputs)`：异步批量调用

---

## 5. LCEL：LangChain Expression Language

LCEL 是 LangChain 的链式组合语法，核心符号是 `|`。

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("请用中文解释：{topic}")
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({"topic": "RAG"})
print(result)
```

执行流程：

```text
用户输入 -> Prompt -> Model -> OutputParser -> 最终结果
```

LCEL 的优势：

- 组合清晰
- 支持同步、异步、流式、批量
- 容易调试
- 容易替换模型或模块

---

## 6. Prompt 模板

### 6.1 PromptTemplate

适合普通文本补全模型。

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("把下面内容翻译成英文：{text}")

print(prompt.invoke({"text": "你好，世界"}))
```

### 6.2 ChatPromptTemplate

适合 Chat Model。

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个严谨的 Python 老师。"),
    ("human", "请解释这个概念：{concept}"),
])
```

### 6.3 MessagesPlaceholder

用于插入历史对话。

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个 helpful assistant。"),
    MessagesPlaceholder("history"),
    ("human", "{input}"),
])
```

---

## 7. Model 模型调用

### 7.1 Chat Model

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    max_tokens=500,
)
```

常用参数：

- `model`：模型名称
- `temperature`：随机性，越高越发散
- `max_tokens`：最大输出长度
- `timeout`：超时时间
- `max_retries`：重试次数

### 7.2 流式输出

```python
for chunk in model.stream("写一首关于程序员的短诗"):
    print(chunk.content, end="")
```

### 7.3 批量调用

```python
results = model.batch([
    "解释 Python",
    "解释 JavaScript",
    "解释 Rust",
])

for item in results:
    print(item.content)
```

---

## 8. Output Parser 输出解析

### 8.1 字符串解析

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
```

### 8.2 JSON 解析

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()
```

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser

prompt = ChatPromptTemplate.from_template(
    "请把{name}的信息生成为 JSON，字段包括 name、role、skills。"
)

chain = prompt | ChatOpenAI(model="gpt-4o-mini") | JsonOutputParser()

print(chain.invoke({"name": "张三"}))
```

### 8.3 Pydantic 结构化输出

```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

class Person(BaseModel):
    name: str = Field(description="姓名")
    age: int = Field(description="年龄")
    job: str = Field(description="职业")

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_model = model.with_structured_output(Person)

result = structured_model.invoke("生成一个程序员人物信息")
print(result)
```

---

## 9. Memory 记忆

新版本 LangChain 更推荐使用 `RunnableWithMessageHistory` 或 LangGraph 来管理状态。

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的助手。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

chain = prompt | ChatOpenAI(model="gpt-4o-mini")

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "user-1"}}

print(chain_with_history.invoke({"input": "我叫小明"}, config=config).content)
print(chain_with_history.invoke({"input": "我叫什么？"}, config=config).content)
```

---

## 10. RAG：检索增强生成

RAG 是 LangChain 最常用场景之一。

### 10.1 RAG 流程

```text
文档 -> 切分 -> 向量化 -> 存入向量数据库 -> 检索 -> 拼接上下文 -> LLM 回答
```

### 10.2 安装依赖

```bash
pip install chromadb pypdf
```

### 10.3 加载文档

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("example.pdf")
docs = loader.load()
```

### 10.4 文档切分

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
)

chunks = splitter.split_documents(docs)
```

### 10.5 向量化与入库

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db",
)
```

### 10.6 检索器

```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
```

### 10.7 RAG Chain

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

prompt = ChatPromptTemplate.from_template("""
请基于以下上下文回答问题。
如果上下文中没有答案，请说不知道，不要编造。

上下文：
{context}

问题：{question}
""")

rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | ChatOpenAI(model="gpt-4o-mini", temperature=0)
    | StrOutputParser()
)

answer = rag_chain.invoke("这份文档主要讲了什么？")
print(answer)
```

---

## 11. Document Loader 文档加载器

常见 Loader：

- `TextLoader`：加载文本
- `PyPDFLoader`：加载 PDF
- `CSVLoader`：加载 CSV
- `WebBaseLoader`：加载网页
- `DirectoryLoader`：加载目录
- `UnstructuredFileLoader`：加载复杂文件

示例：

```python
from langchain_community.document_loaders import DirectoryLoader, TextLoader

loader = DirectoryLoader(
    "./docs",
    glob="**/*.md",
    loader_cls=TextLoader,
)

docs = loader.load()
```

---

## 12. Text Splitter 文本切分

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    separators=["\n\n", "\n", "。", " ", ""],
)
```

切分建议：

- 普通中文文档：`chunk_size` 500 到 1000
- 技术文档：`chunk_size` 800 到 1500
- 法律合同：保留章节结构，适当增加 overlap
- FAQ：按问答对切分，不要机械切块

---

## 13. Embedding 向量模型

Embedding 把文本转换为向量，用于相似度检索。

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector = embeddings.embed_query("LangChain 是什么？")
print(len(vector))
```

常见选择：

- OpenAI Embeddings
- Cohere Embeddings
- HuggingFace Embeddings
- BGE / M3E 等中文向量模型

---

## 14. Vector Store 向量数据库

常见向量库：

- Chroma：本地开发简单
- FAISS：本地高性能
- Milvus：适合大规模部署
- Qdrant：易用、生产友好
- Pinecone：云服务
- Weaviate：功能丰富

Chroma 示例：

```python
from langchain_community.vectorstores import Chroma

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db",
)

docs = vectorstore.similarity_search("怎么使用 LangChain？", k=3)
```

---

## 15. Retriever 检索器

### 15.1 相似度检索

```python
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4},
)
```

### 15.2 MMR 检索

MMR 会兼顾相关性和多样性。

```python
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "fetch_k": 20},
)
```

### 15.3 带分数检索

```python
docs_and_scores = vectorstore.similarity_search_with_score("问题", k=4)
```

---

## 16. Tool 工具

Tool 是 Agent 调用外部能力的方式。

```python
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """计算两个整数之和。"""
    return a + b

print(add.name)
print(add.description)
print(add.invoke({"a": 1, "b": 2}))
```

工具设计原则：

- 名称清晰
- 描述明确
- 参数类型准确
- 返回内容简洁
- 不要让一个工具承担太多职责

---

## 17. Agent 智能体

Agent 可以根据目标自主选择工具。

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

@tool
def get_weather(city: str) -> str:
    """查询城市天气。"""
    return f"{city} 今天晴，25 摄氏度。"

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent = create_react_agent(model, tools=[get_weather])

result = agent.invoke({
    "messages": [("user", "北京今天天气怎么样？")]
})

print(result["messages"][-1].content)
```

Agent 的典型循环：

```text
用户目标 -> 模型思考 -> 选择工具 -> 执行工具 -> 观察结果 -> 继续推理 -> 最终回答
```

---

## 18. LangGraph 入门

LangGraph 用来构建可控、状态化、多节点的 Agent 工作流。相比传统 Agent，LangGraph 更适合生产环境。

### 18.1 安装

```bash
pip install langgraph
```

### 18.2 基础图

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END

class State(TypedDict):
    input: str
    output: str

def node_a(state: State):
    return {"output": f"处理结果：{state['input']}"}

graph = StateGraph(State)
graph.add_node("node_a", node_a)
graph.set_entry_point("node_a")
graph.add_edge("node_a", END)

app = graph.compile()

result = app.invoke({"input": "hello", "output": ""})
print(result)
```

### 18.3 条件分支

```python
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END

class State(TypedDict):
    question: str
    route: str
    answer: str

def router(state: State):
    if "价格" in state["question"]:
        return {"route": "sales"}
    return {"route": "support"}

def sales_node(state: State):
    return {"answer": "这是销售问题。"}

def support_node(state: State):
    return {"answer": "这是支持问题。"}

def choose_route(state: State) -> Literal["sales", "support"]:
    return state["route"]

graph = StateGraph(State)
graph.add_node("router", router)
graph.add_node("sales", sales_node)
graph.add_node("support", support_node)

graph.set_entry_point("router")
graph.add_conditional_edges("router", choose_route)
graph.add_edge("sales", END)
graph.add_edge("support", END)

app = graph.compile()
```

LangGraph 适合：

- 多步骤任务
- 需要状态管理的对话
- 人工审核节点
- 工具调用可控的 Agent
- 复杂业务流程编排

---

## 19. LangSmith 调试与评估

LangSmith 用于追踪调用链、调试 Prompt、评估模型效果。

### 19.1 开启追踪

```bash
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_API_KEY="你的 LangSmith Key"
export LANGCHAIN_PROJECT="langchain-demo"
```

### 19.2 追踪价值

LangSmith 可以看到：

- 每一步输入输出
- Token 消耗
- 模型延迟
- Prompt 内容
- Retriever 返回了哪些文档
- Agent 调用了哪些工具
- 哪一步出错

### 19.3 评估维度

常见评估指标：

- 正确性
- 相关性
- 忠实度
- 幻觉率
- 延迟
- 成本
- 工具调用准确率

---

## 20. 完整 RAG 项目示例

目录结构：

```text
rag_demo/
  app.py
  ingest.py
  docs/
    example.txt
  chroma_db/
  requirements.txt
```

### 20.1 requirements.txt

```text
langchain
langchain-core
langchain-community
langchain-openai
langchain-text-splitters
chromadb
python-dotenv
```

### 20.2 ingest.py

```python
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

loader = DirectoryLoader(
    "./docs",
    glob="**/*.txt",
    loader_cls=TextLoader,
)

docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
chunks = splitter.split_documents(docs)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

Chroma.from_documents(
    chunks,
    embedding=embeddings,
    persist_directory="./chroma_db",
)

print(f"已导入 {len(chunks)} 个文档块")
```

### 20.3 app.py

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

prompt = ChatPromptTemplate.from_template("""
你是一个企业知识库助手。
请只基于上下文回答问题。
如果上下文没有答案，请回答：我不知道。

上下文：
{context}

问题：
{question}
""")

chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | ChatOpenAI(model="gpt-4o-mini", temperature=0)
    | StrOutputParser()
)

while True:
    question = input("请输入问题，输入 q 退出：")
    if question.lower() == "q":
        break
    print(chain.invoke(question))
```

运行：

```bash
python ingest.py
python app.py
```

---

## 21. 常见架构模式

### 21.1 普通问答

```text
User -> Prompt -> LLM -> Answer
```

适合：

- 翻译
- 改写
- 摘要
- 简单问答

### 21.2 RAG 知识库

```text
User -> Retriever -> Context -> LLM -> Answer
```

适合：

- 企业文档问答
- 产品手册问答
- 法律文档检索
- 论文问答

### 21.3 Agent 工具调用

```text
User -> Agent -> Tool -> Observation -> Agent -> Answer
```

适合：

- 查数据库
- 调 API
- 自动化任务
- 多工具助手

### 21.4 LangGraph 工作流

```text
User -> Router -> Node A / Node B -> Tool -> Human Review -> Final
```

适合：

- 多步骤业务流程
- 可控 Agent
- 审批流
- 长任务

---

## 22. Prompt 工程技巧

好 Prompt 通常包含：

- 角色：你是谁
- 任务：要做什么
- 约束：不能做什么
- 输入：用户数据
- 输出格式：需要怎样返回
- 示例：必要时给 few-shot 示例

模板：

```text
你是一个{role}。

你的任务是：{task}

要求：
1. {constraint_1}
2. {constraint_2}
3. {constraint_3}

输入：
{input}

请按以下格式输出：
{format}
```

RAG Prompt 建议：

- 明确要求只基于上下文回答
- 明确不知道就说不知道
- 要求引用来源时，需要在上下文里保留 metadata
- 不要把无关上下文塞太多

---

## 23. 工程化最佳实践

### 23.1 把 Prompt 当代码管理

Prompt 应该版本化、可测试、可追踪，不要散落在业务代码里。

### 23.2 给链路加日志

至少记录：

- 请求 ID
- 用户输入
- 检索结果 ID
- 模型名称
- 耗时
- 错误信息

### 23.3 做降级策略

例如：

- 模型失败时重试
- 大模型不可用时切小模型
- RAG 无结果时返回固定话术
- 工具调用失败时给用户可理解的提示

### 23.4 控制成本

方法：

- 减少上下文长度
- 使用更便宜的模型处理简单任务
- 对 Embedding 结果缓存
- 对高频问题做结果缓存
- 批量处理离线任务

### 23.5 防止幻觉

方法：

- 使用 RAG
- 强约束 Prompt
- 结构化输出
- 引用来源
- 后处理校验
- 人工审核高风险结果

---

## 24. 常见坑

### 24.1 Prompt 写得太宽泛

坏例子：

```text
帮我回答问题。
```

好例子：

```text
你是客服助手，请只基于给定知识库回答。如果没有答案，请说不知道。
```

### 24.2 RAG 检索不到正确内容

可能原因：

- 文档切分太大或太小
- Embedding 模型不适合中文
- query 表达和文档表达差异大
- metadata 没有利用
- `k` 太小
- 没有 rerank

### 24.3 Agent 工具描述不清楚

工具描述会直接影响模型是否正确调用工具。

### 24.4 过度依赖 Agent

不是所有问题都需要 Agent。确定流程的问题，优先用普通 Chain 或 LangGraph。

---

## 25. 学习路线

推荐顺序：

1. 先掌握 ChatModel、Prompt、Parser
2. 学 LCEL，把简单链串起来
3. 学 Loader、Splitter、Embedding、VectorStore、Retriever
4. 做一个完整 RAG 项目
5. 学 Tool 和 Agent
6. 学 LangGraph，把 Agent 做可控
7. 学 LangSmith，做调试和评估
8. 学部署、缓存、监控、权限和成本控制

---

## 26. 最小可用模板

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业助手。"),
    ("human", "{input}"),
])

chain = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0) | StrOutputParser()

print(chain.invoke({"input": "解释 LangChain 的核心价值"}))
```

---

## 27. 总结

LangChain 的核心不是“调用大模型”，而是把大模型接入真实业务系统。

你需要重点掌握：

- Prompt：控制模型行为
- Model：调用不同 LLM
- Parser：约束输出格式
- LCEL：组合调用链
- RAG：连接私有知识
- Tool：连接外部能力
- Agent：让模型决定下一步
- LangGraph：让复杂流程可控
- LangSmith：调试、追踪、评估

如果是生产项目，建议优先使用：

- LCEL 处理简单链路
- RAG 处理知识库问答
- LangGraph 处理复杂 Agent 工作流
- LangSmith 做调试与评估

---

## 28. 覆盖确认清单

这份教程已经覆盖 LangChain 开发中最常见的完整链路。

| 模块 | 是否覆盖 | 说明 |
| --- | --- | --- |
| ChatModel | 已覆盖 | OpenAI Chat Model、流式、批量 |
| Prompt | 已覆盖 | 普通模板、聊天模板、历史占位符 |
| Output Parser | 已覆盖 | 字符串、JSON、Pydantic 结构化输出 |
| LCEL | 已覆盖 | `prompt | model | parser` 基础链 |
| Runnable | 已覆盖 | invoke、batch、stream、async |
| Memory | 已覆盖 | `RunnableWithMessageHistory` |
| Document Loader | 已覆盖 | PDF、目录、文本等 |
| Text Splitter | 已覆盖 | 递归切分与参数建议 |
| Embedding | 已覆盖 | OpenAI Embeddings |
| VectorStore | 已覆盖 | Chroma 示例与常见向量库 |
| Retriever | 已覆盖 | similarity、MMR、带分数检索 |
| RAG | 已覆盖 | 基础 RAG 与完整项目 |
| Tool | 已覆盖 | `@tool` 定义方式 |
| Agent | 已覆盖 | `create_react_agent` |
| LangGraph | 已覆盖 | 基础图、条件分支 |
| LangSmith | 已覆盖 | 追踪、调试、评估方向 |
| 工程化 | 已覆盖 | 日志、降级、成本、幻觉控制 |

下面继续补充更细的可运行 Demo，包括并行链、路由链、Few-shot、RAG 引用来源、Rerank、Agent 记忆、LangGraph checkpoint、FastAPI 部署等。

---

## 29. Demo 运行准备

建议新建虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
```

基础依赖：

```bash
pip install -U langchain langchain-core langchain-community langchain-openai langchain-text-splitters python-dotenv pydantic-settings
```

RAG 依赖：

```bash
pip install -U chromadb pypdf beautifulsoup4
```

LangGraph 与服务化依赖：

```bash
pip install -U langgraph fastapi uvicorn
```

可选依赖：

```bash
pip install -U langserve langchain-anthropic langchain-ollama sse-starlette
```

`.env` 示例：

```text
OPENAI_API_KEY=你的 API Key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=你的 LangSmith Key
LANGCHAIN_PROJECT=langchain-fullstack-demo
```

---

## 30. Demo：基础聊天助手

文件名：`demo_01_chat.py`

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

while True:
    user_input = input("你：")
    if user_input.lower() in {"q", "quit", "exit"}:
        break

    response = model.invoke(user_input)
    print("AI：", response.content)
```

运行：

```bash
python demo_01_chat.py
```

---

## 31. Demo：LCEL 基础链

文件名：`demo_02_lcel_chain.py`

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个技术写作助手，回答要简洁准确。"),
    ("human", "请解释：{topic}"),
])

chain = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0) | StrOutputParser()

print(chain.invoke({"topic": "LangChain LCEL"}))
```

重点：

- `ChatPromptTemplate` 负责构造消息
- `ChatOpenAI` 负责生成
- `StrOutputParser` 把 `AIMessage` 转成字符串

---

## 32. Demo：流式输出

文件名：`demo_03_stream.py`

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = ChatPromptTemplate.from_template("请写一段 200 字以内的介绍：{topic}")
chain = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0.7) | StrOutputParser()

for chunk in chain.stream({"topic": "RAG 的工作原理"}):
    print(chunk, end="", flush=True)
```

适合：

- 聊天 UI
- 长文本生成
- 用户需要即时反馈的场景

---

## 33. Demo：异步批量调用

文件名：`demo_04_async_batch.py`

```python
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = ChatPromptTemplate.from_template("用一句话解释：{topic}")
chain = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0) | StrOutputParser()

async def main():
    inputs = [
        {"topic": "Prompt"},
        {"topic": "Embedding"},
        {"topic": "VectorStore"},
        {"topic": "Agent"},
    ]
    results = await chain.abatch(inputs)
    for result in results:
        print(result)

asyncio.run(main())
```

适合：

- 离线批处理
- 多问题并发
- 批量摘要、批量分类、批量抽取

---

## 34. Demo：Few-shot Prompt

文件名：`demo_05_few_shot.py`

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

examples = [
    {"input": "订单一直没发货", "output": "物流问题"},
    {"input": "怎么申请退款", "output": "退款问题"},
    {"input": "发票抬头怎么改", "output": "发票问题"},
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}"),
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是客服工单分类器，只输出分类名称。"),
    few_shot_prompt,
    ("human", "{input}"),
])

chain = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0) | StrOutputParser()

print(chain.invoke({"input": "我的包裹三天没动了"}))
```

适合：

- 分类
- 风格模仿
- 信息抽取
- 输出格式约束

---

## 35. Demo：结构化抽取

文件名：`demo_06_structured_extract.py`

```python
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

load_dotenv()

class Invoice(BaseModel):
    company: str = Field(description="公司名称")
    amount: float = Field(description="发票金额")
    date: str = Field(description="发票日期")
    items: List[str] = Field(description="商品或服务项目")

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
extractor = model.with_structured_output(Invoice)

text = "2026 年 6 月 1 日，上海某某科技有限公司购买云服务，金额 1288.50 元，项目包括云服务器和对象存储。"

result = extractor.invoke(text)
print(result.model_dump())
```

适合：

- 合同字段抽取
- 发票识别后结构化
- 简历解析
- 工单字段提取

---

## 36. Demo：RunnableParallel 并行链

文件名：`demo_07_parallel.py`

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

summary_chain = ChatPromptTemplate.from_template("总结这段文本：{text}") | model | parser
keywords_chain = ChatPromptTemplate.from_template("提取 5 个关键词：{text}") | model | parser
sentiment_chain = ChatPromptTemplate.from_template("判断情绪倾向：{text}") | model | parser

chain = RunnableParallel(
    summary=summary_chain,
    keywords=keywords_chain,
    sentiment=sentiment_chain,
)

text = "这款产品界面漂亮，速度也很快，但客服响应太慢，希望后续改进。"
result = chain.invoke({"text": text})

print(result)
```

适合：

- 同一输入做多个分析
- 并行摘要、分类、抽取
- 多模型投票

---

## 37. Demo：RunnableBranch 路由链

文件名：`demo_08_router.py`

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

tech_chain = ChatPromptTemplate.from_template("你是技术支持，请回答：{question}") | model | parser
sales_chain = ChatPromptTemplate.from_template("你是销售顾问，请回答：{question}") | model | parser
default_chain = ChatPromptTemplate.from_template("你是通用客服，请回答：{question}") | model | parser

router = RunnableBranch(
    (lambda x: "报错" in x["question"] or "接口" in x["question"], tech_chain),
    (lambda x: "价格" in x["question"] or "购买" in x["question"], sales_chain),
    default_chain,
)

print(router.invoke({"question": "你们企业版价格是多少？"}))
```

适合：

- 客服问题分流
- 多业务线助手
- 不同问题走不同 Prompt 或模型

---

## 38. Demo：对话记忆

文件名：`demo_09_memory.py`

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

histories = {}

def get_history(session_id: str):
    if session_id not in histories:
        histories[session_id] = InMemoryChatMessageHistory()
    return histories[session_id]

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个能记住上下文的助手。"),
    MessagesPlaceholder("history"),
    ("human", "{input}"),
])

chain = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0) | StrOutputParser()

chat = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "user-001"}}

print(chat.invoke({"input": "我叫李雷，喜欢 Python。"}, config=config))
print(chat.invoke({"input": "我喜欢什么语言？"}, config=config))
```

注意：

- `InMemoryChatMessageHistory` 只适合 Demo
- 生产环境应存 Redis、PostgreSQL 或其他持久化存储

---

## 39. Demo：本地文本 RAG

文件名：`demo_10_rag_text.py`

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

raw_docs = [
    Document(page_content="LangChain 是一个 LLM 应用开发框架，支持 Prompt、Chain、Agent、RAG。", metadata={"source": "intro"}),
    Document(page_content="LangGraph 用于构建有状态、多节点、可控的 Agent 工作流。", metadata={"source": "langgraph"}),
    Document(page_content="LangSmith 用于调试、追踪和评估 LangChain 应用。", metadata={"source": "langsmith"}),
]

splitter = RecursiveCharacterTextSplitter(chunk_size=120, chunk_overlap=20)
docs = splitter.split_documents(raw_docs)

vectorstore = Chroma.from_documents(
    docs,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    collection_name="demo_rag_text",
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

def format_docs(items):
    return "\n\n".join(f"来源：{doc.metadata['source']}\n内容：{doc.page_content}" for doc in items)

prompt = ChatPromptTemplate.from_template("""
请只基于上下文回答问题。若上下文没有答案，请回答不知道。

{context}

问题：{question}
""")

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | ChatOpenAI(model="gpt-4o-mini", temperature=0)
    | StrOutputParser()
)

print(chain.invoke("LangGraph 是做什么的？"))
```

---

## 40. Demo：带引用来源的 RAG

文件名：`demo_11_rag_with_sources.py`

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

docs = [
    Document(page_content="退款申请需要在订单完成后 7 天内提交。", metadata={"source": "refund_policy.md"}),
    Document(page_content="企业版支持 SSO、审计日志和专属 SLA。", metadata={"source": "enterprise.md"}),
]

vectorstore = Chroma.from_documents(
    docs,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    collection_name="demo_rag_sources",
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

def format_docs(items):
    return "\n\n".join(
        f"[{index}] source={doc.metadata['source']}\n{doc.page_content}"
        for index, doc in enumerate(items, start=1)
    )

prompt = ChatPromptTemplate.from_template("""
请基于上下文回答，并在答案末尾列出引用来源。
如果上下文没有答案，请说不知道。

上下文：
{context}

问题：{question}
""")

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | ChatOpenAI(model="gpt-4o-mini", temperature=0)
    | StrOutputParser()
)

print(chain.invoke("企业版有什么能力？"))
```

生产建议：

- metadata 中保留 `source`、`page`、`url`、`title`
- Prompt 要求引用来源
- 前端展示引用卡片，而不是只展示模型文字

---

## 41. Demo：RAG 检索结果调试

文件名：`demo_12_retriever_debug.py`

```python
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

load_dotenv()

docs = [
    Document(page_content="重置密码请进入账号安全页面。", metadata={"source": "account.md"}),
    Document(page_content="企业版价格按席位数和功能模块计费。", metadata={"source": "pricing.md"}),
    Document(page_content="API 限流默认每分钟 600 次请求。", metadata={"source": "api.md"}),
]

vectorstore = Chroma.from_documents(
    docs,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    collection_name="demo_retriever_debug",
)

query = "接口每分钟能请求多少次？"
results = vectorstore.similarity_search_with_score(query, k=3)

for doc, score in results:
    print("score:", score)
    print("source:", doc.metadata["source"])
    print("content:", doc.page_content)
    print("---")
```

调试重点：

- 正确文档是否排在前面
- 分数差距是否明显
- query 是否需要改写
- chunk 是否切得太碎或太大

---

## 42. Demo：RAG Query 改写

文件名：`demo_13_query_rewrite.py`

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = ChatPromptTemplate.from_template("""
你是搜索查询改写器。请把用户问题改写成适合知识库检索的简短查询。
只输出改写后的查询，不要解释。

用户问题：{question}
""")

chain = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0) | StrOutputParser()

print(chain.invoke({"question": "我想知道你们接口一分钟最多能调几次，会不会被限制？"}))
```

用途：

- 用户问题口语化时改写成检索关键词
- 多轮对话中把省略问题改写为完整问题
- 提升 RAG 召回率

---

## 43. Demo：简单 Rerank 重排

文件名：`demo_14_simple_rerank.py`

```python
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

load_dotenv()

class RankResult(BaseModel):
    best_index: int = Field(description="最相关文档的序号，从 0 开始")
    reason: str = Field(description="选择原因")

docs = [
    "账号安全页面可以修改密码和绑定手机。",
    "API 默认限流为每分钟 600 次请求。",
    "企业版支持单点登录和审计日志。",
]

question = "接口调用频率限制是多少？"

model = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(RankResult)

prompt = f"""
问题：{question}

候选文档：
0. {docs[0]}
1. {docs[1]}
2. {docs[2]}

请选择最相关的文档。
"""

result = model.invoke(prompt)
print(result.model_dump())
print("best doc:", docs[result.best_index])
```

说明：

- 这是教学版 Rerank，适合小规模候选
- 生产环境建议使用专门 reranker，如 Cohere Rerank、bge-reranker、Jina Reranker

---

## 44. Demo：自定义 Tool

文件名：`demo_15_custom_tool.py`

```python
from langchain_core.tools import tool

@tool
def calculate_discount(price: float, discount: float) -> float:
    """根据原价和折扣计算最终价格。discount 是 0 到 1 之间的小数。"""
    return round(price * (1 - discount), 2)

print(calculate_discount.invoke({"price": 199.0, "discount": 0.15}))
```

工具函数的 docstring 非常重要，Agent 会根据它判断什么时候调用工具。

---

## 45. Demo：Agent 调用多个工具

文件名：`demo_16_agent_tools.py`

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

@tool
def get_order_status(order_id: str) -> str:
    """根据订单号查询订单状态。"""
    return f"订单 {order_id} 当前状态：已发货，预计明天送达。"

@tool
def calculate_refund(order_amount: float) -> str:
    """根据订单金额估算可退款金额。"""
    return f"预计可退款金额为 {order_amount:.2f} 元。"

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent = create_react_agent(model, tools=[get_order_status, calculate_refund])

result = agent.invoke({
    "messages": [("user", "帮我查一下订单 A10086 的状态")]
})

print(result["messages"][-1].content)
```

---

## 46. Demo：Agent 加系统提示词

文件名：`demo_17_agent_prompt.py`

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

@tool
def get_weather(city: str) -> str:
    """查询指定城市天气。"""
    return f"{city} 今天多云，气温 22 到 28 摄氏度。"

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent = create_react_agent(
    model,
    tools=[get_weather],
    prompt=SystemMessage(content="你是一个谨慎的助手。需要使用工具时必须调用工具，不要编造。"),
)

result = agent.invoke({"messages": [("user", "上海天气如何？")]})
print(result["messages"][-1].content)
```

---

## 47. Demo：LangGraph 带记忆 Checkpoint

文件名：`demo_18_langgraph_memory.py`

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
checkpointer = MemorySaver()

agent = create_react_agent(model, tools=[], checkpointer=checkpointer)

config = {"configurable": {"thread_id": "thread-001"}}

result1 = agent.invoke(
    {"messages": [("user", "我叫王强，正在学习 LangChain。")]},
    config=config,
)
print(result1["messages"][-1].content)

result2 = agent.invoke(
    {"messages": [("user", "我正在学习什么？")]},
    config=config,
)
print(result2["messages"][-1].content)
```

生产环境：

- `MemorySaver` 只适合本地 Demo
- 生产应使用持久化 checkpoint，例如 SQLite、Postgres 或 Redis 方案

---

## 48. Demo：LangGraph 多节点工作流

文件名：`demo_19_langgraph_workflow.py`

```python
from typing import TypedDict, Literal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

load_dotenv()

class State(TypedDict):
    question: str
    category: str
    answer: str

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

classify_chain = (
    ChatPromptTemplate.from_template("问题分类，只输出 tech 或 sales：{question}")
    | model
    | parser
)

tech_chain = ChatPromptTemplate.from_template("你是技术支持，请回答：{question}") | model | parser
sales_chain = ChatPromptTemplate.from_template("你是销售顾问，请回答：{question}") | model | parser

def classify(state: State):
    category = classify_chain.invoke({"question": state["question"]}).strip().lower()
    if category not in {"tech", "sales"}:
        category = "tech"
    return {"category": category}

def route(state: State) -> Literal["tech", "sales"]:
    return state["category"]

def tech(state: State):
    return {"answer": tech_chain.invoke({"question": state["question"]})}

def sales(state: State):
    return {"answer": sales_chain.invoke({"question": state["question"]})}

graph = StateGraph(State)
graph.add_node("classify", classify)
graph.add_node("tech", tech)
graph.add_node("sales", sales)
graph.set_entry_point("classify")
graph.add_conditional_edges("classify", route)
graph.add_edge("tech", END)
graph.add_edge("sales", END)

app = graph.compile()

print(app.invoke({"question": "API 报 401 怎么处理？", "category": "", "answer": ""}))
```

---

## 49. Demo：LangGraph 人工审核节点

文件名：`demo_20_langgraph_review.py`

```python
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END

class State(TypedDict):
    amount: float
    approved: bool
    message: str

def check_amount(state: State):
    return state

def route(state: State) -> Literal["auto_approve", "manual_review"]:
    if state["amount"] <= 1000:
        return "auto_approve"
    return "manual_review"

def auto_approve(state: State):
    return {"approved": True, "message": "金额较小，自动通过。"}

def manual_review(state: State):
    approved = input(f"退款金额 {state['amount']} 元，是否通过？y/n：") == "y"
    return {"approved": approved, "message": "人工审核完成。"}

graph = StateGraph(State)
graph.add_node("check_amount", check_amount)
graph.add_node("auto_approve", auto_approve)
graph.add_node("manual_review", manual_review)
graph.set_entry_point("check_amount")
graph.add_conditional_edges("check_amount", route)
graph.add_edge("auto_approve", END)
graph.add_edge("manual_review", END)

app = graph.compile()

print(app.invoke({"amount": 1888.0, "approved": False, "message": ""}))
```

说明：

- 这个 Demo 用 `input()` 模拟人工审核
- 真实生产中通常会把状态挂起，等待前端或审批系统回调

---

## 50. Demo：Web 页面加载 RAG

文件名：`demo_21_web_rag.py`

```python
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

loader = WebBaseLoader("https://python.langchain.com/docs/introduction/")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
chunks = splitter.split_documents(docs)

vectorstore = Chroma.from_documents(
    chunks,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    collection_name="demo_web_rag",
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

def format_docs(items):
    return "\n\n".join(doc.page_content for doc in items)

prompt = ChatPromptTemplate.from_template("""
基于上下文回答问题。

上下文：
{context}

问题：{question}
""")

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | ChatOpenAI(model="gpt-4o-mini", temperature=0)
    | StrOutputParser()
)

print(chain.invoke("LangChain 主要解决什么问题？"))
```

---

## 51. Demo：PDF RAG

文件名：`demo_22_pdf_rag.py`

```python
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

pdf_path = "example.pdf"
loader = PyPDFLoader(pdf_path)
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
chunks = splitter.split_documents(docs)

vectorstore = Chroma.from_documents(
    chunks,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    persist_directory="./pdf_chroma_db",
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

def format_docs(items):
    return "\n\n".join(
        f"page={doc.metadata.get('page')}\n{doc.page_content}"
        for doc in items
    )

prompt = ChatPromptTemplate.from_template("""
请基于 PDF 内容回答，并尽量指出页码。

上下文：
{context}

问题：{question}
""")

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | ChatOpenAI(model="gpt-4o-mini", temperature=0)
    | StrOutputParser()
)

print(chain.invoke("这份 PDF 的核心结论是什么？"))
```

---

## 52. Demo：FastAPI 封装 LangChain 服务

文件名：`demo_23_fastapi.py`

```python
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

app = FastAPI(title="LangChain Demo API")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个简洁的中文助手。"),
    ("human", "{message}"),
])

chain = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0) | StrOutputParser()

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = chain.invoke({"message": request.message})
    return ChatResponse(answer=answer)
```

运行：

```bash
uvicorn demo_23_fastapi:app --reload
```

测试：

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"解释一下 RAG"}'
```

---

## 53. Demo：FastAPI 流式输出

文件名：`demo_24_fastapi_stream.py`

```python
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

app = FastAPI(title="LangChain Streaming API")

class ChatRequest(BaseModel):
    message: str

prompt = ChatPromptTemplate.from_template("请用中文回答：{message}")
chain = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0.7) | StrOutputParser()

@app.post("/chat/stream")
def chat_stream(request: ChatRequest):
    def generate():
        for chunk in chain.stream({"message": request.message}):
            yield chunk

    return StreamingResponse(generate(), media_type="text/plain; charset=utf-8")
```

运行：

```bash
uvicorn demo_24_fastapi_stream:app --reload
```

---

## 54. Demo：SQLite SQL 问答

文件名：`demo_25_sqlite_qa.py`

```python
import sqlite3
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain

load_dotenv()

conn = sqlite3.connect("demo.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
cursor.execute("DELETE FROM users")
cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [("Alice", 30), ("Bob", 24)])
conn.commit()
conn.close()

db = SQLDatabase.from_uri("sqlite:///demo.db")
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
chain = create_sql_query_chain(model, db)

sql = chain.invoke({"question": "年龄最大的用户是谁？"})
print(sql)
```

注意：

- 这个 Demo 只生成 SQL，不执行 SQL
- 生产环境执行 SQL 前必须做权限控制、只读限制和 SQL 审核

---

## 55. Demo：回调与日志

文件名：`demo_26_callbacks.py`

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler

load_dotenv()

class SimpleLogger(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print("LLM start")
        for prompt in prompts:
            print(prompt[:200])

    def on_llm_end(self, response, **kwargs):
        print("LLM end")

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    callbacks=[SimpleLogger()],
)

response = model.invoke("解释一下 LangSmith 的作用")
print(response.content)
```

生产中建议优先使用 LangSmith 做完整追踪，自定义 callback 适合记录业务侧日志。

---

## 56. Demo：缓存模型结果

文件名：`demo_27_cache.py`

```python
from dotenv import load_dotenv
from langchain.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
from langchain_openai import ChatOpenAI

load_dotenv()

set_llm_cache(SQLiteCache(database_path=".langchain_cache.db"))

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

print(model.invoke("用一句话解释 LangChain").content)
print(model.invoke("用一句话解释 LangChain").content)
```

说明：

- 第二次相同请求会命中缓存
- 适合高频固定问题、开发调试、离线任务
- 不适合强实时、强个性化回答

---

## 57. Demo：错误重试与超时

文件名：`demo_28_retry_timeout.py`

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    timeout=20,
    max_retries=3,
)

response = model.invoke("解释一下 LLM 应用里的降级策略")
print(response.content)
```

生产建议：

- 设置合理超时
- 设置有限重试
- 捕获异常后返回用户可理解的信息
- 对可恢复错误重试，对参数错误不要盲目重试

---

## 58. Demo：多轮 RAG 的问题改写

文件名：`demo_29_contextualize_question.py`

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "根据历史对话，把用户最新问题改写成独立完整的问题。只输出改写后的问题。"),
    MessagesPlaceholder("history"),
    ("human", "{input}"),
])

chain = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0) | StrOutputParser()

history = [
    HumanMessage(content="LangGraph 是什么？"),
    AIMessage(content="LangGraph 是用于构建状态化 Agent 工作流的框架。"),
]

standalone_question = chain.invoke({
    "history": history,
    "input": "它和普通 Agent 有什么区别？",
})

print(standalone_question)
```

这是多轮 RAG 的关键步骤。否则用户问“它”“这个”“刚才那个”时，Retriever 很可能检索不到正确文档。

---

## 59. Demo：配置模型可替换

文件名：`demo_30_configurable_model.py`

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.runnables.utils import ConfigurableField

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini", temperature=0).configurable_fields(
    temperature=ConfigurableField(id="temperature"),
)

default_response = model.invoke("写一句产品标语")
creative_response = model.with_config(configurable={"temperature": 0.9}).invoke("写一句产品标语")

print("default:", default_response.content)
print("creative:", creative_response.content)
```

适合：

- A/B 测试
- 不同租户使用不同参数
- 后台动态调整模型行为

---

## 60. Demo：小型项目模板

推荐目录：

```text
my_langchain_app/
  app/
    __init__.py
    main.py
    chains.py
    prompts.py
    retrievers.py
    tools.py
    settings.py
  scripts/
    ingest.py
  data/
  tests/
  .env
  requirements.txt
```

`app/settings.py`：

```python
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    model_name: str = "gpt-4o-mini"
    temperature: float = 0

    class Config:
        env_file = ".env"

settings = Settings()
```

`app/prompts.py`：

```python
from langchain_core.prompts import ChatPromptTemplate

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是企业知识库助手。只基于上下文回答，不知道就说不知道。"),
    ("human", "上下文：\n{context}\n\n问题：{question}"),
])
```

`app/chains.py`：

```python
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from app.prompts import qa_prompt
from app.settings import settings

def create_qa_chain():
    model = ChatOpenAI(model=settings.model_name, temperature=settings.temperature)
    return qa_prompt | model | StrOutputParser()
```

`app/main.py`：

```python
from fastapi import FastAPI
from pydantic import BaseModel
from app.chains import create_qa_chain

app = FastAPI()
chain = create_qa_chain()

class AskRequest(BaseModel):
    context: str
    question: str

@app.post("/ask")
def ask(request: AskRequest):
    answer = chain.invoke({"context": request.context, "question": request.question})
    return {"answer": answer}
```

依赖：

```text
fastapi
uvicorn
langchain
langchain-core
langchain-openai
pydantic-settings
python-dotenv
```

运行：

```bash
uvicorn app.main:app --reload
```

---

## 61. 生产落地检查表

上线前建议逐项确认：

| 项目 | 检查点 |
| --- | --- |
| Prompt | 是否版本化，是否有测试样例 |
| Model | 是否设置超时、重试、温度、最大输出 |
| RAG | 是否评估召回率，是否保留来源 |
| Tool | 是否有权限控制，是否避免危险操作 |
| Agent | 是否限制最大步数，是否有失败兜底 |
| Memory | 是否区分用户会话，是否可清除 |
| 日志 | 是否记录 request_id、耗时、错误 |
| 安全 | 是否过滤 Prompt Injection、敏感信息 |
| 成本 | 是否有 token 预算、缓存和限流 |
| 评估 | 是否有基准问题集和回归测试 |
| 部署 | 是否有健康检查、监控和报警 |

---

## 62. 如何判断该用 Chain、Agent 还是 LangGraph

优先级建议：

| 场景 | 推荐方案 |
| --- | --- |
| 固定输入输出 | LCEL Chain |
| 文档问答 | RAG Chain |
| 简单工具调用 | Agent |
| 多步骤且流程明确 | LangGraph |
| 多步骤且需要人工审核 | LangGraph |
| 需要强可控生产 Agent | LangGraph + Tool |

不要一上来就用 Agent。能用确定性 Chain 解决的问题，优先用 Chain。Agent 适合“模型需要自己判断下一步”的场景。

---

## 63. Demo 索引表

| Demo | 文件名 | 主题 |
| --- | --- | --- |
| 1 | `demo_01_chat.py` | 基础聊天 |
| 2 | `demo_02_lcel_chain.py` | LCEL 基础链 |
| 3 | `demo_03_stream.py` | 流式输出 |
| 4 | `demo_04_async_batch.py` | 异步批量 |
| 5 | `demo_05_few_shot.py` | Few-shot Prompt |
| 6 | `demo_06_structured_extract.py` | 结构化抽取 |
| 7 | `demo_07_parallel.py` | 并行链 |
| 8 | `demo_08_router.py` | 路由链 |
| 9 | `demo_09_memory.py` | 对话记忆 |
| 10 | `demo_10_rag_text.py` | 本地文本 RAG |
| 11 | `demo_11_rag_with_sources.py` | 带来源 RAG |
| 12 | `demo_12_retriever_debug.py` | 检索调试 |
| 13 | `demo_13_query_rewrite.py` | Query 改写 |
| 14 | `demo_14_simple_rerank.py` | 简单 Rerank |
| 15 | `demo_15_custom_tool.py` | 自定义 Tool |
| 16 | `demo_16_agent_tools.py` | Agent 多工具 |
| 17 | `demo_17_agent_prompt.py` | Agent 系统提示词 |
| 18 | `demo_18_langgraph_memory.py` | LangGraph 记忆 |
| 19 | `demo_19_langgraph_workflow.py` | LangGraph 多节点 |
| 20 | `demo_20_langgraph_review.py` | 人工审核节点 |
| 21 | `demo_21_web_rag.py` | Web RAG |
| 22 | `demo_22_pdf_rag.py` | PDF RAG |
| 23 | `demo_23_fastapi.py` | FastAPI 服务 |
| 24 | `demo_24_fastapi_stream.py` | FastAPI 流式 |
| 25 | `demo_25_sqlite_qa.py` | SQLite SQL 问答 |
| 26 | `demo_26_callbacks.py` | Callback 日志 |
| 27 | `demo_27_cache.py` | 模型缓存 |
| 28 | `demo_28_retry_timeout.py` | 超时重试 |
| 29 | `demo_29_contextualize_question.py` | 多轮问题改写 |
| 30 | `demo_30_configurable_model.py` | 可配置模型 |
| 31 | `demo_31_langserve.py` | LangServe 服务 |
| 32 | `demo_32_ollama.py` | Ollama 本地模型 |
| 33 | `demo_33_anthropic.py` | Anthropic 模型 |
| 34 | `demo_34_hub_prompt.py` | LangChain Hub Prompt |

---

## 64. Demo：LangServe 暴露 Chain

LangServe 是 LangChain 官方服务化方案之一，可以快速把 Runnable 暴露成 HTTP API。

文件名：`demo_31_langserve.py`

```python
from dotenv import load_dotenv
from fastapi import FastAPI
from langserve import add_routes
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个简洁的中文助手。"),
    ("human", "{input}"),
])

chain = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0) | StrOutputParser()

app = FastAPI(title="LangServe Demo")
add_routes(app, chain, path="/chain")
```

运行：

```bash
uvicorn demo_31_langserve:app --reload
```

调用：

```bash
curl -X POST http://127.0.0.1:8000/chain/invoke \
  -H 'Content-Type: application/json' \
  -d '{"input":{"input":"解释 LangServe 是什么"}}'
```

说明：

- `/chain/invoke`：单次调用
- `/chain/batch`：批量调用
- `/chain/stream`：流式调用
- `/chain/playground`：浏览器调试界面

---

## 65. Demo：Ollama 本地模型

如果你希望本地运行模型，可以使用 Ollama。

安装模型：

```bash
ollama pull llama3.1
```

文件名：`demo_32_ollama.py`

```python
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("请用中文解释：{topic}")
model = ChatOllama(model="llama3.1", temperature=0)
chain = prompt | model | StrOutputParser()

print(chain.invoke({"topic": "本地大模型的优缺点"}))
```

适合：

- 本地开发
- 数据不能出内网的实验场景
- 低成本原型验证

注意：

- 本地模型质量取决于模型大小和机器性能
- RAG 场景中也要选择合适的本地 embedding 模型

---

## 66. Demo：Anthropic Claude 模型

文件名：`demo_33_anthropic.py`

```python
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = ChatPromptTemplate.from_template("请用中文总结：{text}")
model = ChatAnthropic(model="claude-3-5-sonnet-latest", temperature=0)
chain = prompt | model | StrOutputParser()

print(chain.invoke({"text": "LangChain 可以组合模型、提示词、工具、检索器和工作流。"}))
```

环境变量：

```bash
export ANTHROPIC_API_KEY="你的 Anthropic API Key"
```

模型切换建议：

- 简单分类、改写、摘要：用便宜快速模型
- 复杂推理、代码、长上下文：用更强模型
- 生产系统中把模型名称放到配置，不要写死在业务代码里

---

## 67. Demo：LangChain Hub Prompt

LangChain Hub 可以拉取社区或团队共享的 Prompt。是否使用取决于团队流程；生产中更推荐把核心 Prompt 放在自己的版本管理里。

文件名：`demo_34_hub_prompt.py`

```python
from dotenv import load_dotenv
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = hub.pull("rlm/rag-prompt")
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
chain = prompt | model | StrOutputParser()

result = chain.invoke({
    "context": "LangChain 是用于开发 LLM 应用的框架。",
    "question": "LangChain 是什么？",
})

print(result)
```

注意：

- Hub Prompt 可能随版本变化，关键业务不要无审查直接依赖远程 Prompt
- 团队内应固定 Prompt 版本或复制到代码仓库中管理

---

## 68. 最终覆盖说明

严格来说，LangChain 集成生态非常大，不可能在一份教程里逐个覆盖每个第三方数据库、每个模型供应商、每个 Loader 和每个 Tool。

但这份教程已经覆盖“全家桶主干”：

- `langchain-core`：Prompt、Runnable、Parser、Tool、Message
- `langchain`：Chain、Hub、缓存、SQL Chain
- `langchain-community`：Loader、VectorStore、SQLDatabase、Cache
- `langchain-openai`：ChatModel、Embedding
- `langchain-anthropic`：Claude 调用
- `langchain-ollama`：本地模型调用
- `langgraph`：Agent、状态图、条件分支、checkpoint、人审节点
- `langserve`：Runnable 服务化
- `langsmith`：追踪、调试、评估思路
- RAG：加载、切分、向量化、检索、引用、调试、改写、重排
- 工程化：FastAPI、流式、异步、缓存、日志、超时、重试、配置、项目结构

如果你要继续深化，下一步建议单独拆成 3 份进阶文档：

1. `langchain-rag-production.md`：专讲生产级 RAG，包括混合检索、rerank、权限、评估。
2. `langgraph-agent-production.md`：专讲可控 Agent，包括 checkpoint、人审、工具权限、失败恢复。
3. `langchain-deployment-observability.md`：专讲部署、LangServe、FastAPI、LangSmith、监控和成本控制。
