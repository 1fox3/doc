# AI 开发与应用面试复习

本目录面向后端、全栈、平台工程师的 AI 开发与应用面试复习，重点覆盖大模型应用工程、LLM API 协议、RAG、Agent、LangChain、模型选择、Fine-tuning、Pretrain、Post-train、RL、部署和安全可靠性。

## 学习路径

1. 先理解大模型基础概念：Token、Embedding、Transformer、推理参数、幻觉。
2. 再掌握 Prompt Engineering：如何稳定控制模型输入输出。
3. 重点掌握 RAG：企业知识库、智能客服、文档问答最常见。
4. 理解 Agent：重点掌握 LangChain 的 Chain、Tool、AgentExecutor、Memory 和 RAG Agent。
5. 学习模型开发与 Fine-tuning：掌握数据准备、LoRA、QLoRA、训练、评估和部署。
6. 理解模型训练路线：Pretrain、Continued Pretraining、SFT、DPO、RLHF、PPO、GRPO。
7. 理解从 0 构建模型：tokenizer、dataset、Transformer、loss、训练循环、推理生成。
8. 了解 Claude、Codex 和代码智能体：Tool Use、MCP、代码助手架构、测试验证闭环。
9. 掌握 LLM API 协议共性和 ChatGPT/OpenAI API：鉴权、消息、流式输出、工具调用、结构化输出。
10. 从工程角度补齐架构、成本、监控、安全、评估与部署。

## 文件说明

| 文件 | 重点 |
| --- | --- |
| [01-AI基础与大模型.md](./01-AI基础与大模型.md) | LLM 基础概念、Transformer、推理参数、幻觉 |
| [02-Prompt-Engineering.md](./02-Prompt-Engineering.md) | Prompt 设计、结构化输出、常见优化方法 |
| [03-RAG检索增强生成.md](./03-RAG检索增强生成.md) | RAG 架构、切分、召回、重排、评估 |
| [04-AI-Agent开发.md](./04-AI-Agent开发.md) | Agent、Tool Calling、LangChain、Memory、RAG Agent demo |
| [05-AI应用工程架构.md](./05-AI应用工程架构.md) | 前后端集成、流式输出、会话、限流、成本 |
| [06-模型选择与部署.md](./06-模型选择与部署.md) | 闭源/开源模型、本地部署、vLLM、Ollama、量化 |
| [07-AI安全与可靠性.md](./07-AI安全与可靠性.md) | Prompt Injection、权限、输出校验、Guardrails |
| [08-AI项目实战案例.md](./08-AI项目实战案例.md) | 智能客服、知识库、代码助手、文档抽取等案例 |
| [09-AI面试高频问答.md](./09-AI面试高频问答.md) | 高频问题与回答模板 |
| [10-AI术语中英对照.md](./10-AI术语中英对照.md) | 常用术语中英对照 |
| [11-模型开发与Fine-tuning实战.md](./11-模型开发与Fine-tuning实战.md) | SFT、LoRA、QLoRA、训练代码、评估、部署 |
| [12-Pretrain-Posttrain-RL.md](./12-Pretrain-Posttrain-RL.md) | Pretrain、Post-train、SFT、DPO、RLHF、PPO、GRPO |
| [13-从0构建一个模型.md](./13-从0构建一个模型.md) | PyTorch 从零实现小型 Transformer LM、工业级模型构建流程 |
| [14-Claude与Codex代码智能体.md](./14-Claude与Codex代码智能体.md) | Claude API、Tool Use、MCP、Codex、代码智能体架构和 demo |
| [15-LLM-API协议与ChatGPT接口.md](./15-LLM-API协议与ChatGPT接口.md) | LLM API 协议共性、ChatGPT/OpenAI Responses API、流式输出、工具调用 |

## 面试表达原则

1. 不要只说“调了大模型 API”，要讲清楚业务问题、架构设计、稳定性和效果评估。
2. 遇到 RAG 问题，要从数据处理、检索、重排、Prompt、评估五层回答。
3. 遇到 Agent 问题，要强调边界：Agent 适合多步骤、工具调用、目标不完全固定的场景，不适合强确定性、高风险、低延迟链路。
4. 遇到安全问题，要回答权限隔离、上下文隔离、输入输出校验、审计日志和人工兜底。
5. 遇到成本问题，要回答模型分层、缓存、批处理、限流、上下文压缩和监控。
6. 遇到 Fine-tuning 问题，要先判断是否真的需要微调，再讲数据、训练、评估、部署和风险。
7. 遇到 LangChain 问题，要讲清楚 LCEL、Tool、AgentExecutor、Memory、Retriever，而不是只说“用过框架”。
8. 遇到模型训练问题，要区分 Pretrain、Continued Pretraining、SFT、DPO 和 RLHF，不要把所有训练都叫微调。
9. 遇到从 0 构建模型问题，要先区分教学级从零实现和工业级从零训练，再讲 tokenizer、模型结构、loss、训练、评估和部署。
10. 遇到 Claude、Codex 或代码助手问题，要重点讲上下文工程、工具调用、权限边界、测试验证和审计，而不是只比较模型名字。
11. 遇到 LLM API 协议问题，要先讲清楚 HTTP、JSON、鉴权、上下文、推理参数、流式输出、工具调用和 token 用量这些共性，再说明不同 Provider 的字段差异需要通过模型网关适配。
