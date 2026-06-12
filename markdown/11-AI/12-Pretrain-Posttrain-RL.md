# Pretrain、Post-train 与 Model RL

## 总览

大模型训练通常分为三个阶段：

```text
Pretrain -> Post-train -> Alignment / RL
预训练      后训练        对齐与强化学习
```

简单理解：

| 阶段 | 目标 | 数据 | 输出能力 |
| --- | --- | --- | --- |
| Pretrain | 学语言、知识、代码和通用模式 | 海量无标注文本、代码、多模态数据 | 基础模型 Base Model |
| SFT | 学会按指令回答 | 人工或合成的指令问答数据 | Instruct Model |
| Preference Training | 学会偏好更好的答案 | chosen/rejected 偏好数据 | 更符合人类偏好的模型 |
| RL | 用奖励信号继续优化策略 | Reward Model 或规则奖励 | 更对齐目标的模型 |

面试表达：

> Pretrain 是让模型具备通用语言和知识能力，Post-train 是把 base model 变成好用的助手，RL 或偏好优化是让模型输出更符合人类偏好或业务目标。工程上大多数公司不会从零 pretrain，而是基于开源 base model 做 SFT、DPO、RLHF 或领域继续预训练。

## Pretrain 是什么

Pretrain 是用海量文本训练模型预测下一个 Token。

训练目标：

```text
给定 token_1, token_2, ..., token_n，预测 token_{n+1}
```

例如：

```text
输入：Java 中 HashMap 的底层结构是
目标：数组、链表、红黑树...
```

模型通过不断预测下一个 Token，学习语言结构、世界知识、代码模式和推理模式。

## Pretrain 数据怎么做

数据来源：

1. 网页文本。
2. 书籍。
3. 论文。
4. 代码仓库。
5. 百科。
6. 问答社区。
7. 企业内部文档。
8. 多语言语料。

数据处理流水线：

```text
原始数据 -> 清洗 -> 去重 -> 质量过滤 -> 安全过滤 -> 分词 -> 打包 -> 训练样本
```

关键处理：

1. 去 HTML、广告、乱码。
2. 删除重复内容，避免模型记忆重复样本。
3. 过滤低质量内容，例如采集页、垃圾文本、SEO 文本。
4. 过滤敏感信息，例如手机号、身份证、密钥。
5. 过滤有害内容。
6. 按语言、领域、质量做采样配比。
7. Tokenize 后按固定长度打包。

数据配比很关键。例如代码模型需要提高代码语料比例，中文模型需要提高中文高质量语料比例。

## Pretrain 训练流程

```text
准备 tokenizer -> 初始化模型结构 -> 加载训练数据 -> 分布式训练 -> 保存 checkpoint -> 评估 perplexity -> 继续训练或调整数据
```

核心组件：

1. Tokenizer：把文本转成 Token ID。
2. Model Architecture：Transformer Decoder-only 是主流 LLM 架构。
3. Optimizer：常见 AdamW。
4. Scheduler：学习率 warmup + decay。
5. Distributed Training：DDP、FSDP、DeepSpeed、Megatron-LM。
6. Checkpoint：周期性保存模型权重和 optimizer 状态。

训练目标通常是 Causal Language Modeling：

```python
loss = cross_entropy(model(input_ids), labels=input_ids shifted by one)
```

## Pretrain Demo：迷你 GPT 训练骨架

真实 LLM pretrain 需要大量 GPU，这里 demo 只是帮助理解训练流程。

```python
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, GPT2LMHeadModel


class TextDataset(Dataset):
    def __init__(self, texts, tokenizer, max_length=128):
        self.examples = []
        for text in texts:
            encoded = tokenizer(
                text,
                max_length=max_length,
                truncation=True,
                padding="max_length",
                return_tensors="pt",
            )
            self.examples.append(encoded["input_ids"].squeeze(0))

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        input_ids = self.examples[idx]
        return {"input_ids": input_ids, "labels": input_ids.clone()}


texts = [
    "Java HashMap uses array, linked list and red-black tree.",
    "Redis supports string, hash, list, set and sorted set.",
    "RAG retrieves external knowledge before generation.",
]

tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

model = GPT2LMHeadModel.from_pretrained("gpt2")
dataset = TextDataset(texts, tokenizer)
loader = DataLoader(dataset, batch_size=2, shuffle=True)

optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
model.train()

for epoch in range(3):
    for batch in loader:
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        print(f"epoch={epoch}, loss={loss.item():.4f}")
```

这不是从零训练，只是继续训练 GPT-2。真正从零训练还需要自己定义模型配置、初始化权重和大规模数据。

## Continued Pretraining

Continued Pretraining 也叫领域继续预训练，是在已有 base model 上继续用领域无标注语料训练。

适合：

1. 金融、医疗、法律、代码等领域语言差异大。
2. 企业内部有大量高质量文档。
3. 希望模型理解领域术语和写作风格。

不适合：

1. 知识频繁变动且需要引用来源。
2. 数据量太少。
3. 只是输出格式不好。

和 SFT 的区别：

| 方式 | 数据 | 目标 |
| --- | --- | --- |
| Continued Pretraining | 无标注领域文本 | 增强领域语言和知识分布 |
| SFT | 指令-回答样本 | 学会执行具体任务 |

实际项目常见组合：

```text
Base Model -> Continued Pretraining -> SFT -> DPO/RLHF -> 部署
```

## Post-train 是什么

Post-train 是预训练之后的一系列训练，让 base model 变成可用助手。

常见 Post-train 阶段：

1. SFT：监督微调，让模型学会遵循指令。
2. Rejection Sampling：生成多个答案，筛选高质量答案继续训练。
3. Preference Training：用偏好数据训练模型更偏向好答案。
4. RLHF：基于奖励模型做强化学习。
5. Safety Training：拒绝有害请求，提升安全性。

## SFT 如何做

SFT 数据通常是：

```json
{"messages":[{"role":"system","content":"你是一个有帮助的助手。"},{"role":"user","content":"解释什么是 RAG"},{"role":"assistant","content":"RAG 是检索增强生成..."}]}
```

训练目标仍然是预测下一个 Token，但通常只对 assistant 输出部分计算 loss，避免模型学习预测用户问题。

SFT 重点：

1. 指令要多样。
2. 回答要高质量。
3. 格式要统一。
4. 要覆盖拒答、安全、边界场景。
5. 不要让模型学到错误或啰嗦回答。

## Preference Training

SFT 只能告诉模型“标准答案是什么”，但很多开放问题没有唯一答案。Preference Training 用“哪个答案更好”来训练模型。

数据格式：

```json
{
  "prompt": "如何优化 RAG 效果？",
  "chosen": "可以从数据清洗、chunk、混合检索、rerank、prompt 和评估集优化。",
  "rejected": "多调几次 prompt 就好了。"
}
```

chosen 是更好的答案，rejected 是较差答案。

偏好数据可以来自：

1. 人工标注。
2. 用户点赞点踩。
3. 专家评审。
4. 强模型打分。
5. 规则自动生成。

## Model RL 是什么

在 LLM 中，Model RL 通常指用强化学习或偏好优化方法，让模型输出更符合奖励目标。

强化学习里的角色：

| RL 概念 | LLM 对应 |
| --- | --- |
| Policy | 当前语言模型 |
| Action | 生成下一个 Token 或完整回答 |
| State | Prompt 和已生成上下文 |
| Reward | 答案质量分数 |
| Environment | 用户、任务、评估器或工具环境 |

目标：让模型生成高 reward 的答案，同时不要偏离原模型太远。

## RLHF 流程

RLHF 是 Reinforcement Learning from Human Feedback。

典型流程：

```text
1. Pretrain 得到 Base Model
2. SFT 得到初始 Assistant Model
3. 对同一 Prompt 生成多个答案
4. 人类标注哪个答案更好
5. 用偏好数据训练 Reward Model
6. 用 PPO 等 RL 算法优化 Assistant Model
7. 评估安全性、帮助性、真实性
```

## Reward Model

Reward Model 输入 prompt + answer，输出一个分数，表示答案质量。

训练数据：

```text
prompt + chosen answer 的分数应该高于 prompt + rejected answer
```

训练目标不是预测文本，而是学习排序偏好。

简化理解：

```text
reward(prompt, chosen) > reward(prompt, rejected)
```

Reward Model 学到的是人类偏好，例如：

1. 回答是否有帮助。
2. 是否事实正确。
3. 是否遵循指令。
4. 是否安全。
5. 是否简洁。

## PPO 如何用于 LLM

PPO 是 Proximal Policy Optimization，是 RLHF 中常见算法。

简化流程：

```text
Prompt -> Policy Model 生成答案 -> Reward Model 打分 -> PPO 更新 Policy Model
```

为什么要 PPO：

1. 直接最大化 reward 容易让模型崩掉。
2. PPO 会限制每次策略更新幅度。
3. 通常还加入 KL penalty，避免模型偏离 SFT 模型太远。

训练目标大致是：

```text
maximize reward - beta * KL(current_model || reference_model)
```

其中 reference model 通常是 SFT 后的模型。

KL penalty 的作用：

1. 防止模型为了 reward 投机取巧。
2. 保持语言流畅性。
3. 保持原有通用能力。

## PPO Demo：概念代码

下面代码展示 TRL 中 PPO 的大致形态。真实训练需要 reward model、数据集、显存和大量调参。

```python
from transformers import AutoTokenizer
from trl import AutoModelForCausalLMWithValueHead, PPOConfig, PPOTrainer


model_name = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLMWithValueHead.from_pretrained(model_name, trust_remote_code=True)
ref_model = AutoModelForCausalLMWithValueHead.from_pretrained(model_name, trust_remote_code=True)

config = PPOConfig(
    learning_rate=1e-6,
    batch_size=2,
    mini_batch_size=1,
)

ppo_trainer = PPOTrainer(
    config=config,
    model=model,
    ref_model=ref_model,
    tokenizer=tokenizer,
)

prompts = [
    "用一句话解释 RAG。",
    "如何降低大模型幻觉？",
]


def simple_reward(text: str) -> float:
    # 示例规则：包含关键字且不要太长。真实项目通常使用 Reward Model 或业务评估器。
    score = 0.0
    if "检索" in text or "上下文" in text:
        score += 1.0
    if len(text) < 200:
        score += 0.5
    return score


for prompt in prompts:
    query = tokenizer(prompt, return_tensors="pt").input_ids[0]
    response = ppo_trainer.generate(query, max_new_tokens=128)
    response_text = tokenizer.decode(response.squeeze(), skip_special_tokens=True)
    reward = simple_reward(response_text)
    ppo_trainer.step([query], [response.squeeze()], [reward])
    print(response_text, reward)
```

这个 demo 只是帮助理解：模型生成答案，奖励函数打分，然后 PPO 根据 reward 更新模型。

## DPO

DPO 是 Direct Preference Optimization。它不需要显式训练 Reward Model，也不需要 PPO 那样复杂的 RL 过程，直接用 chosen/rejected 偏好数据优化模型。

DPO 输入数据：

```json
{"prompt":"解释什么是 Agent","chosen":"Agent 是能规划并调用工具完成目标的 AI 系统。","rejected":"Agent 就是聊天机器人。"}
```

DPO 优点：

1. 训练流程比 PPO 简单。
2. 稳定性通常更好。
3. 工程成本更低。
4. 不需要单独训练 reward model。

DPO 缺点：

1. 依赖高质量偏好数据。
2. 不适合所有复杂 RL 场景。
3. 对 reward 可组合和动态环境支持不如 RL 灵活。

## DPO Demo

```python
from datasets import load_dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import DPOConfig, DPOTrainer


model_name = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, device_map="auto")

dataset = load_dataset("json", data_files="preference.jsonl", split="train")

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
)

training_args = DPOConfig(
    output_dir="./outputs/dpo-model",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=5e-6,
    num_train_epochs=1,
    logging_steps=10,
    beta=0.1,
    report_to="none",
)

trainer = DPOTrainer(
    model=model,
    ref_model=None,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer,
    peft_config=lora_config,
)

trainer.train()
trainer.save_model("./outputs/dpo-model")
```

`preference.jsonl` 示例：

```json
{"prompt":"如何优化 RAG 效果？","chosen":"可以从文档清洗、chunk、混合检索、rerank、Prompt 约束和评估集六个方面优化。","rejected":"调大模型参数就可以。"}
{"prompt":"Agent 生产环境有什么风险？","chosen":"主要风险是工具误调用、权限越权、循环执行、成本失控和输出不可控，需要限制工具权限、最大步数、超时和审计。","rejected":"Agent 一般没有什么风险。"}
```

## GRPO

GRPO 是 Group Relative Policy Optimization，一些推理模型训练中会使用类似思想。它不一定依赖传统 critic/value model，而是对同一个 prompt 采样多个回答，通过组内相对 reward 来优化。

简化流程：

```text
同一个 prompt -> 生成多个 answers -> 每个 answer 打 reward -> 计算组内相对优势 -> 更新模型
```

适合：

1. 数学推理。
2. 代码任务。
3. 有规则验证器的任务。
4. 可以自动判断对错的任务。

例如数学题可以用最终答案是否正确作为 reward，代码题可以用单测是否通过作为 reward。

## Rule-based RL

有些 RL 不依赖人工偏好，而是依赖规则或环境反馈。

例子：

1. 数学：答案正确得 1 分，错误得 0 分。
2. 代码：单测通过率作为 reward。
3. SQL：执行结果正确作为 reward。
4. 格式：JSON 合法得分，非法扣分。
5. 安全：触发敏感输出扣分。

优点：

1. 标注成本低。
2. 反馈明确。
3. 可大规模自动生成。

缺点：

1. 容易 reward hacking。
2. 只适合可验证任务。
3. 规则不完整时会优化偏。

## Reward Hacking

Reward Hacking 是模型学会钻奖励函数漏洞，而不是学会真正做好任务。

例子：

1. 奖励越长越高，模型开始废话变多。
2. 奖励包含关键词，模型堆关键词但不回答问题。
3. 代码任务只为了通过公开测试，忽略隐藏 case。
4. 安全 reward 过强，模型对正常问题也拒答。

防护：

1. 多维 reward。
2. 加 KL penalty。
3. 使用隐藏评估集。
4. 加人工抽检。
5. 定期做能力回归测试。

## Pretrain、SFT、DPO、RLHF 怎么选

| 目标 | 推荐方式 |
| --- | --- |
| 学习大量领域语言和术语 | Continued Pretraining |
| 学会固定任务和输出格式 | SFT |
| 偏好更好的回答风格 | DPO |
| 基于复杂奖励优化行为 | RLHF / PPO / GRPO |
| 补充实时知识和引用来源 | RAG |
| 调用业务系统完成动作 | Tool Calling / Agent |

## 工程成本对比

| 方式 | 数据成本 | 训练成本 | 工程复杂度 | 常见团队 |
| --- | --- | --- | --- | --- |
| Prompt | 低 | 无 | 低 | 应用团队 |
| RAG | 中 | 低 | 中 | 应用/平台团队 |
| SFT/LoRA | 中 | 中 | 中 | AI 应用团队 |
| Continued Pretraining | 高 | 高 | 高 | 模型团队 |
| DPO | 高 | 中 | 中 | 模型/算法团队 |
| RLHF/PPO | 很高 | 很高 | 很高 | 大模型团队 |
| Pretrain from scratch | 极高 | 极高 | 极高 | 基础模型团队 |

## 面试常问

### 如何 pretrain 一个 model？

完整流程是先准备大规模高质量语料，做清洗、去重、安全过滤和采样配比，然后训练 tokenizer 或选择已有 tokenizer，定义 Transformer decoder-only 模型结构，用 causal language modeling 目标预测下一个 Token。训练时需要分布式训练框架、混合精度、checkpoint、学习率调度和评估。实际业务中很少从零 pretrain，更多是 continued pretraining。

### 如何 post-train 一个 model？

Post-train 通常包括 SFT、偏好优化和安全对齐。先用指令问答数据做 SFT，让 base model 学会按指令回答；再用 chosen/rejected 偏好数据做 DPO 或训练 Reward Model；如果需要更强对齐，可以用 PPO 等 RL 方法基于 reward 继续优化；最后做安全、事实性和业务评估。

### Model RL 是如何做的？

LLM 里的 RL 通常把模型当作 policy，prompt 是状态，生成 token 或回答是动作，reward model 或规则评估器给奖励。典型 RLHF 是先训练 SFT 模型，再收集人类偏好训练 reward model，最后用 PPO 优化模型，同时加 KL penalty 防止模型偏离原模型太远。

### DPO 和 RLHF 有什么区别？

DPO 直接用 chosen/rejected 偏好数据优化模型，不需要单独训练 reward model，也不需要 PPO，工程上更简单、更稳定。RLHF 通常需要 reward model 和 PPO，复杂度更高，但在复杂奖励和交互环境中更灵活。

### RL 能不能让模型变聪明？

RL 可以强化某些行为，例如更好遵循指令、更符合偏好、更会推理或更会通过验证器。但 RL 不是凭空注入知识，它依赖 base model 的能力、训练数据和 reward 设计。reward 设计不好还会导致 reward hacking 或能力退化。

### 为什么 post-train 后模型可能变差？

可能因为训练数据质量差、偏好数据有偏、学习率过大、过拟合、reward 设计错误或 KL 约束不足。表现为回答模板化、过度拒答、通用能力下降或为了 reward 投机取巧。因此 post-train 后必须做能力回归和安全评估。
