# Phoenix LLM 可观测与评估

## 求职者定位

Phoenix 是 Arize AI 开源的 LLM Observability 和 Evaluation 平台，主要用于观察、调试和评估 LLM 应用。面试中不要只把它说成“看日志的工具”，更准确的表达是：

> Phoenix 帮助我把 LLM 应用从黑盒变成可观测系统。它能记录模型调用、Prompt、输入输出、Retriever、Tool、Agent 执行路径、延迟、错误和评估分数，并通过 Dataset + Experiment 做回归评估。

求职者应该重点表达三件事：

1. 我知道 LLM 应用为什么难调试。
2. 我能用 tracing 找到坏 case 的原因。
3. 我能用 dataset 和 experiment 做持续评估，而不是靠主观感觉上线。

## Phoenix 解决什么问题

LLM 应用和传统后端不同，很多问题不是异常栈能直接定位的。

常见问题：

1. Prompt 渲染后到底长什么样不清楚。
2. RAG 检索到了哪些文档不清楚。
3. Agent 为什么选了某个工具不清楚。
4. 模型输出错误，但不知道是 Prompt、检索、工具还是模型本身的问题。
5. 改 Prompt 后效果好坏只靠人工感觉。
6. 线上 bad case 没有沉淀成回归测试集。

Phoenix 对应能力：

| 问题 | Phoenix 能力 |
| --- | --- |
| 看不到执行链路 | Tracing |
| 看不到模型输入输出 | LLM spans |
| 看不到 RAG 检索结果 | Retriever spans |
| 看不到 Agent 工具调用 | Tool spans |
| 不知道改动是否变好 | Dataset + Experiment |
| 无法批量评估 | Evaluators |
| 无法复盘坏样本 | Trace + Annotation |

## 核心概念

### Project

Project 用来隔离不同应用或环境的 traces，例如 `local-agent-demo`、`rag-prod`、`customer-service-agent`。

面试表达：

> 我会按应用或环境拆分 Phoenix project，避免不同业务链路的 trace 混在一起。线上环境还会结合采样和数据保留周期控制成本。

### Trace

Trace 表示一次完整请求的执行链路。

例如一个 RAG 问答请求可能包含：

```text
用户问题 -> Prompt 模板 -> Retriever -> LLM -> Output Parser -> 最终答案
```

Phoenix 会把这条链路拆成多个 span，方便查看每一步输入、输出、耗时和错误。

### Span

Span 是 trace 中的一个步骤，例如：

1. 一次 LLM 调用。
2. 一次向量检索。
3. 一次工具调用。
4. 一个 Chain 节点。
5. 一个 Agent 决策步骤。

面试中可以这样说：

> Trace 让我看到一次请求的全链路，Span 让我定位具体哪一步出了问题，比如检索没召回、Prompt 拼错、工具返回异常或模型输出不符合格式。

### Dataset

Dataset 是评估样本集，用来保存输入、期望输出和元数据。

数据来源可以是：

1. 人工整理的测试样本。
2. 线上 bad case。
3. 高频用户问题。
4. 历史工单。
5. 从 trace 中筛选出的失败样本。

### Experiment

Experiment 是对同一个 Dataset 跑一次系统版本。

它通常用于回答：

1. 新 Prompt 是否比旧 Prompt 更好？
2. 换模型后准确率有没有下降？
3. RAG 的 `top_k` 调整是否提升召回？
4. Agent 工具调用准确率是否稳定？

### Evaluator

Evaluator 是评估函数，可以是代码规则，也可以是 LLM-as-a-judge。

常见 evaluator：

| Evaluator | 作用 |
| --- | --- |
| keyword recall | 检查答案是否覆盖关键词 |
| exact match | 检查分类、枚举、结构化结果是否完全匹配 |
| JSON valid | 检查模型输出是否符合 JSON 格式 |
| tool accuracy | 检查 Agent 是否调用了正确工具 |
| faithfulness | 检查回答是否忠实于检索内容 |
| relevance | 检查回答是否和问题相关 |

## 快速启动

本地开发可以直接启动 Phoenix：

```bash
pip install arize-phoenix
phoenix serve
```

默认访问：

```text
http://localhost:6006
```

Docker 启动：

```bash
docker run -p 6006:6006 -p 4317:4317 -p 4318:4318 arizephoenix/phoenix:latest
```

常用依赖：

```bash
pip install arize-phoenix arize-phoenix-client arize-phoenix-otel openinference-instrumentation-langchain
```

## LangChain Trace 接入

下面示例展示如何把 LangChain 调用上报到 Phoenix。

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from openinference.instrumentation.langchain import LangChainInstrumentor
from phoenix.otel import register


tracer_provider = register(
    project_name="agent-demo",
    endpoint="http://localhost:6006/v1/traces",
)

LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深 AI Agent 工程师，回答要具体。"),
    ("user", "请解释：{question}"),
])

chain = prompt | ChatOllama(model="llama3.2", temperature=0.2) | StrOutputParser()

result = chain.invoke({
    "question": "为什么 LLM 应用需要 tracing？"
})

print(result)
```

运行后可以在 Phoenix UI 里查看：

1. Prompt 实际渲染内容。
2. LLM 输入和输出。
3. 调用耗时。
4. 错误信息。
5. 多步骤链路结构。

## Dataset + Experiment 评估

Phoenix 的评估流程适合用来做回归测试。下面示例用关键词召回评估 Agent 面试问答是否覆盖关键点。

```python
import pandas as pd
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from phoenix.client import Client
from phoenix.client.experiments import create_evaluator, run_experiment


client = Client(base_url="http://localhost:6006")

dataset_df = pd.DataFrame([
    {
        "question": "Agent 和普通 Chatbot 有什么区别？",
        "answer_keywords": ["多步骤", "工具调用", "目标驱动"],
    },
    {
        "question": "生产环境如何控制 Agent 风险？",
        "answer_keywords": ["权限", "最大步骤", "审计", "人工确认"],
    },
])

dataset = client.datasets.create_dataset(
    name="agent-interview-qa",
    dataframe=dataset_df,
    input_keys=["question"],
    output_keys=["answer_keywords"],
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是 AI Agent 面试教练，回答要覆盖关键点。"),
    ("user", "{question}"),
])

chain = prompt | ChatOllama(model="llama3.2", temperature=0) | StrOutputParser()


def task(input: dict) -> str:
    return chain.invoke(input)


@create_evaluator(kind="CODE", name="keyword_recall")
def keyword_recall(output: str, expected: dict) -> dict:
    keywords = expected["answer_keywords"]
    hit_count = sum(1 for keyword in keywords if keyword in output)
    score = hit_count / len(keywords)
    return {
        "score": score,
        "explanation": f"hit {hit_count}/{len(keywords)} keywords",
    }


experiment = run_experiment(
    dataset=dataset,
    task=task,
    evaluators=[keyword_recall],
    experiment_name="agent-interview-chain",
    experiment_description="Agent 面试问答关键字召回评估",
)

print(experiment)
```

面试表达：

> 我会把线上 bad case 和核心场景整理成 Phoenix Dataset。每次改 Prompt、换模型或调整 RAG 参数时，用同一批样本跑 Experiment，再用 evaluator 对准确性、相关性、忠实度和格式合规性打分。这样能把 LLM 应用优化从主观判断变成可复现的实验。

## 在 Agent 项目中的落地方式

Agent 项目最难调的是“中间过程”。Phoenix 的价值在于把 Agent 的决策过程展开。

应该重点记录：

1. 用户原始输入。
2. 系统 Prompt。
3. Agent 每一步 reasoning 之后的 action。
4. Tool name 和 tool arguments。
5. Tool 返回结果。
6. LLM 最终输出。
7. 每一步耗时和错误。

Agent 调试时重点看：

1. 是否选错工具。
2. 是否漏掉必须调用的工具。
3. 是否重复调用工具。
4. 是否因为工具返回太长污染上下文。
5. 是否因为 Prompt 没限制导致输出不稳定。
6. 是否在失败时没有降级路径。

面试表达：

> 对 Agent 来说，我不会只看最终答案，而是会看完整 trace。比如客服 Agent 回答错误，我会先看它有没有调用订单查询工具，再看工具参数是否正确，再看工具返回后模型是否正确理解结果。这样能把错误定位到 Prompt、工具、检索、模型或编排逻辑中的某一层。

## 在 RAG 项目中的落地方式

RAG 的问题通常不只是模型回答错，而是检索和生成链路共同导致。

Phoenix 中应该重点观察：

1. 查询改写后的 query。
2. Retriever 返回的文档。
3. 文档 score。
4. 文档 metadata。
5. 拼进 Prompt 的 context。
6. 最终回答是否基于 context。

RAG 常用评估维度：

| 维度 | 说明 |
| --- | --- |
| retrieval relevance | 检索文档是否相关 |
| faithfulness | 回答是否忠实于上下文 |
| answer relevance | 回答是否真正回答了问题 |
| citation accuracy | 引用来源是否正确 |
| context precision | 检索内容是否噪声过多 |

面试表达：

> RAG 出错时，我会先用 Phoenix 看检索结果。如果没召回正确文档，优先调整 embedding、chunk、metadata filter 或 rerank；如果召回正确但回答错，说明是 Prompt、上下文组织或模型生成的问题。

## Phoenix 与 LangSmith 对比

| 对比项 | Phoenix | LangSmith |
| --- | --- | --- |
| 定位 | 开源 LLM observability 和 evaluation | LangChain 生态官方观测和评估平台 |
| 自托管 | 开源可自托管 | self-hosted 通常需要企业授权 |
| LangChain 集成 | 支持 OpenInference instrumentation | 原生支持 LangChain/LangGraph |
| Tracing | 支持 | 支持 |
| Dataset/Experiment | 支持 | 支持 |
| Prompt 管理 | 支持 | 支持 |
| 适合场景 | 自建、PoC、本地调试、团队观测 | 深度使用 LangChain 生态的团队 |

面试中不要贬低任何一个工具。更好的说法是：

> 如果团队已经深度使用 LangChain，并且有 LangSmith 预算，我会优先用 LangSmith；如果需要开源自托管、快速本地调试或搭建内部 LLM observability 平台，我会考虑 Phoenix。

## 生产落地注意点

### 敏感信息

Trace 里可能包含用户隐私、业务数据、Prompt 和模型输出。生产环境必须做脱敏和权限控制。

建议：

1. 对手机号、邮箱、身份证、地址等字段脱敏。
2. 高敏业务不要完整记录输入输出。
3. 对不同团队设置访问边界。
4. 配置数据保留周期。

### 采样

线上全量记录成本可能很高。

常见做法：

1. 开发和测试环境全量记录。
2. 生产环境按比例采样。
3. 错误请求全量保留。
4. 高价值链路保留更多 trace。

### 异步上报

观测系统不能影响主业务链路。

面试表达：

> Phoenix 上报失败不能导致用户请求失败。生产中我会把 tracing 当成旁路能力，设置超时、异步上报和降级策略。

### Trace ID 串联

Phoenix trace 最好和业务日志、网关日志、订单 ID 或 session ID 串起来。

这样排查问题时可以从业务系统定位到 LLM trace，也可以从 Phoenix 反查业务请求。

## 简历写法

可以写成：

```text
引入 Arize Phoenix 搭建 LLM 应用可观测与评估体系，对 LangChain Agent/RAG 链路进行 tracing，记录模型调用、工具调用、检索结果、延迟和错误；沉淀线上 bad case 为评估数据集，通过 Dataset + Experiment 对 Prompt、模型和 RAG 参数变更做回归评估。
```

更项目化的写法：

```text
在智能客服 Agent 项目中接入 Phoenix，追踪用户请求、Agent 工具调用、订单查询结果和最终回复；基于历史工单构建评估数据集，使用代码 evaluator 检查分类准确率、工具调用准确率和关键词覆盖率，降低 Prompt 调整带来的回归风险。
```

## 面试高频问答

### Phoenix 是什么？

Phoenix 是一个开源的 LLM Observability 和 Evaluation 平台，用于记录和分析 LLM 应用的执行过程。它可以追踪模型调用、Prompt、工具调用、检索结果、延迟、错误，并支持 Dataset + Experiment 做批量评估。

### 为什么 LLM 应用需要 Phoenix 这类工具？

因为 LLM 应用很多错误不是普通异常，而是链路质量问题。例如 Prompt 拼错、检索没召回、工具参数错误、模型没有遵循格式。Phoenix 能把一次请求拆成 trace 和 span，让我们定位问题发生在哪一步。

### Phoenix 如何帮助调试 Agent？

它能记录 Agent 的每一步执行，包括模型判断、工具选择、工具参数、工具返回和最终回答。这样可以判断 Agent 是选错工具、漏调用工具、误解工具结果，还是 Prompt 约束不够。

### Phoenix 如何帮助调试 RAG？

它可以展示检索 query、召回文档、metadata、score、拼接上下文和最终回答。RAG 出错时可以区分是检索阶段失败，还是生成阶段没有忠实使用上下文。

### Dataset 和 Experiment 有什么用？

Dataset 是测试样本集，Experiment 是用某个版本的系统跑这批样本并记录结果。它们用于回归评估，避免每次改 Prompt、模型或检索参数时只靠人工感觉判断效果。

### Evaluator 怎么设计？

确定性任务用代码 evaluator，例如分类准确率、JSON 格式、关键词覆盖、工具调用是否正确。开放式问答可以用 LLM-as-a-judge 评估相关性、忠实度和完整性。生产中最好混合使用规则、人工和 LLM 评估。

### Phoenix 和普通日志有什么区别？

普通日志通常是平铺文本，难以表达 LLM 链路结构。Phoenix 用 trace 和 span 表示层级调用关系，能直接看到 Prompt、模型、Retriever、Tool 和输出之间的关系，也能和评估结果关联。

### 生产接入 Phoenix 要注意什么？

重点是脱敏、采样、权限、异步上报和数据保留周期。Phoenix 是观测系统，不能影响主业务链路；trace 里可能有敏感信息，不能无脑全量记录。

## 面试回答模板

可以这样回答 Phoenix 相关问题：

> 我在 LLM 应用里会引入 Phoenix 做 tracing 和 evaluation。Tracing 主要解决调试问题，把一次请求拆成 prompt、retriever、tool、model call 等 span，定位错误发生在哪一步。Evaluation 主要解决回归问题，把线上 bad case 和核心场景沉淀成 dataset，每次改 Prompt、模型或 RAG 参数都跑 experiment，用 evaluator 比较效果。生产落地时我会注意敏感信息脱敏、采样、权限隔离、异步上报和 trace ID 与业务日志打通。

## 一句话总结

Phoenix 的面试价值不是“我会用一个工具”，而是体现你有 LLM 工程化意识：能观测、能评估、能复盘、能回归，而不是只会写 Prompt 和调用模型 API。
