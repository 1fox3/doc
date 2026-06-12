# 模型开发与 Fine-tuning 实战

## 先纠正一个面试误区

大多数业务开发者不会从零训练一个大模型，而是在已有基础模型上做应用开发、RAG、Prompt、工具调用或 Fine-tuning。

从零训练大模型需要海量语料、GPU 集群、分布式训练框架和大量工程经验。面试中如果被问“如何开发一个 model”，更合理的回答是：

> 我会先明确任务目标和数据形态，再选择基础模型。如果只是补充外部知识，优先 RAG；如果是固定输出风格、领域术语、分类抽取或指令遵循能力不足，可以做 SFT。工程上一般不会从零训练，而是基于 Llama、Qwen、DeepSeek 等开源模型做 LoRA 或 QLoRA 微调，然后用业务评估集验证效果，最后通过 vLLM 或 TGI 部署。

## 模型开发的完整流程

```text
定义任务 -> 准备数据 -> 选择基础模型 -> 选择微调方式 -> 训练 -> 评估 -> 导出模型 -> 部署推理 -> 线上监控
```

每一步要回答的问题：

| 阶段 | 要解决的问题 |
| --- | --- |
| 定义任务 | 是问答、分类、抽取、总结、代码还是对话？ |
| 准备数据 | 输入输出格式是什么？质量是否稳定？是否有敏感信息？ |
| 选择模型 | 中文、代码、长上下文、推理能力是否匹配？ |
| 微调方式 | 全量微调、LoRA、QLoRA 还是只做 Prompt/RAG？ |
| 训练 | 显存是否够？batch size、学习率、epoch 如何设置？ |
| 评估 | 有没有业务评估集？和原模型相比是否真的提升？ |
| 部署 | 用 API、vLLM、TGI、Ollama 还是业务内嵌？ |
| 监控 | 延迟、成本、幻觉、失败率、用户反馈如何收集？ |

## 什么时候需要 Fine-tuning

适合 Fine-tuning：

1. 固定格式输出，例如把客服对话抽取成结构化 JSON。
2. 固定业务话术，例如客服回复风格、销售话术。
3. 领域术语适配，例如金融、医疗、法律、运维。
4. 小模型能力增强，例如让 7B 模型学会某类内部任务。
5. 分类、意图识别、标签生成等稳定任务。

不优先 Fine-tuning：

1. 知识频繁更新，例如企业制度、产品文档、接口说明。
2. 需要引用来源的知识问答。
3. 权限敏感的实时数据查询。
4. 数据量很少且质量不稳定。
5. 只是 Prompt 写得不清楚导致效果不好。

判断规则：

> 知识问题优先 RAG，行为风格问题考虑 Fine-tuning，实时动作问题用 Tool Calling。

## 常见微调方式

### Full Fine-tuning

全量微调会更新模型全部参数。

优点：效果上限高。

缺点：显存和训练成本高，容易过拟合，部署和版本管理成本高。

适合大团队、有充足 GPU 和大量高质量数据的场景。

### LoRA

LoRA 是 Low-Rank Adaptation，只训练少量低秩矩阵，不更新原模型主体参数。

优点：

1. 显存占用低。
2. 训练速度快。
3. 可为不同任务保存不同 adapter。
4. 适合业务团队做轻量微调。

缺点：

1. 效果上限通常低于全量微调。
2. 对模型基础能力依赖较大。

### QLoRA

QLoRA 是在量化基础上做 LoRA，常见是把基础模型以 4bit 加载，再训练 LoRA adapter。

优点：显存需求更低，单卡也可以微调较大的模型。

缺点：训练速度和效果需要评估，复杂任务可能受量化影响。

## 数据准备

Fine-tuning 的效果上限主要由数据质量决定。

### 指令微调数据格式

常见 JSONL 格式：

```json
{"instruction":"请从下面文本中抽取合同甲方、乙方、金额和日期","input":"甲方：北京某某科技有限公司，乙方：上海某某信息有限公司，合同金额为 120 万元，签署日期为 2025-03-01。","output":"{\"甲方\":\"北京某某科技有限公司\",\"乙方\":\"上海某某信息有限公司\",\"金额\":\"120万元\",\"日期\":\"2025-03-01\"}"}
```

也可以用 chat 格式：

```json
{"messages":[{"role":"system","content":"你是一个合同信息抽取助手，只输出 JSON。"},{"role":"user","content":"从文本抽取甲方、乙方、金额和日期：甲方A，乙方B，金额10万元，日期2025-01-01。"},{"role":"assistant","content":"{\"甲方\":\"甲方A\",\"乙方\":\"乙方B\",\"金额\":\"10万元\",\"日期\":\"2025-01-01\"}"}]}
```

### 数据质量要求

1. 输入输出格式一致。
2. 标签准确，不要混入错误样本。
3. 覆盖真实业务表达，不只写理想样例。
4. 包含困难样本，例如缺字段、字段别名、噪声文本、多实体。
5. 训练集、验证集、测试集隔离。
6. 删除手机号、身份证、密钥等敏感信息。

### 数据量经验

粗略经验：

1. 几十条：更适合 few-shot 或 Prompt 优化。
2. 几百条：可以尝试 LoRA，但效果不一定稳定。
3. 几千条：适合做轻量 SFT。
4. 几万条以上：可以系统性微调和评估。

数据质量比数量更重要。1000 条高质量业务样本通常比 10000 条噪声样本更有价值。

## Demo：用 QLoRA 微调 Qwen 模型

下面 demo 用 Hugging Face `transformers`、`datasets`、`peft`、`trl` 做 SFT。适合学习流程，真实训练要根据显卡和模型大小调整参数。

### 目录结构

```text
finetune-demo/
├── data/
│   ├── train.jsonl
│   └── eval.jsonl
├── train_qlora.py
├── infer_lora.py
└── requirements.txt
```

### requirements.txt

```text
torch
transformers
datasets
accelerate
peft
trl
bitsandbytes
sentencepiece
```

Mac 本地通常不适合跑 `bitsandbytes` 训练，建议在 Linux + NVIDIA GPU 环境运行。

### train.jsonl

```json
{"instruction":"从文本中抽取合同字段，只输出 JSON。","input":"甲方：北京星河科技有限公司；乙方：上海云杉信息有限公司；合同金额：88万元；签署日期：2025年5月20日。","output":"{\"甲方\":\"北京星河科技有限公司\",\"乙方\":\"上海云杉信息有限公司\",\"金额\":\"88万元\",\"签署日期\":\"2025年5月20日\"}"}
{"instruction":"从文本中抽取合同字段，只输出 JSON。","input":"本协议由杭州青石网络有限公司与深圳远帆数据有限公司签订，费用总计 35.6 万元，日期为 2024-12-01。","output":"{\"甲方\":\"杭州青石网络有限公司\",\"乙方\":\"深圳远帆数据有限公司\",\"金额\":\"35.6万元\",\"签署日期\":\"2024-12-01\"}"}
```

### train_qlora.py

```python
import torch
from datasets import load_dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTConfig, SFTTrainer


MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
OUTPUT_DIR = "./outputs/qwen-contract-lora"


def format_example(example):
    prompt = (
        "<|im_start|>system\n"
        "你是一个严谨的信息抽取助手。只输出 JSON，不要输出解释。\n"
        "<|im_end|>\n"
        "<|im_start|>user\n"
        f"{example['instruction']}\n\n文本：{example['input']}\n"
        "<|im_end|>\n"
        "<|im_start|>assistant\n"
        f"{example['output']}"
        "<|im_end|>"
    )
    return prompt


def main():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token

    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=quant_config,
        device_map="auto",
        trust_remote_code=True,
    )

    dataset = load_dataset(
        "json",
        data_files={
            "train": "data/train.jsonl",
            "eval": "data/eval.jsonl",
        },
    )

    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )

    training_args = SFTConfig(
        output_dir=OUTPUT_DIR,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        learning_rate=2e-4,
        num_train_epochs=3,
        logging_steps=10,
        eval_strategy="steps",
        eval_steps=100,
        save_steps=100,
        max_seq_length=1024,
        bf16=True,
        packing=False,
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset["train"],
        eval_dataset=dataset["eval"],
        peft_config=lora_config,
        formatting_func=format_example,
        args=training_args,
    )

    trainer.train()
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)


if __name__ == "__main__":
    main()
```

### infer_lora.py

```python
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


BASE_MODEL = "Qwen/Qwen2.5-7B-Instruct"
LORA_DIR = "./outputs/qwen-contract-lora"


def main():
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    model = PeftModel.from_pretrained(model, LORA_DIR)
    model.eval()

    messages = [
        {"role": "system", "content": "你是一个严谨的信息抽取助手。只输出 JSON，不要输出解释。"},
        {"role": "user", "content": "从文本中抽取合同字段：甲方广州明川科技有限公司和乙方南京北辰软件有限公司签订合同，总金额 52 万元，签署日期 2025-06-16。"},
    ]

    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.1,
            do_sample=False,
        )

    generated = outputs[0][inputs["input_ids"].shape[-1]:]
    print(tokenizer.decode(generated, skip_special_tokens=True))


if __name__ == "__main__":
    main()
```

### 训练命令

```bash
accelerate launch train_qlora.py
```

### 预期输出

```json
{"甲方":"广州明川科技有限公司","乙方":"南京北辰软件有限公司","金额":"52万元","签署日期":"2025-06-16"}
```

## 关键参数怎么理解

### learning_rate

LoRA 常见范围是 `1e-4` 到 `3e-4`。太大容易破坏原模型能力，太小收敛慢。

### epoch

常见 1 到 5。数据少时 epoch 太高容易过拟合，表现为训练集很好、真实输入变差。

### batch size

显存不够时用小 batch size + gradient accumulation 模拟大 batch。

### max_seq_length

要覆盖样本输入输出长度。太小会截断训练样本，太大增加显存占用。

### LoRA r

`r` 表示低秩矩阵大小。常见 8、16、32、64。越大可训练参数越多，成本越高，也更容易过拟合。

## 如何评估微调效果

不要只看 loss，也不要只看几个 demo。

### 离线评估

准备独立测试集，和 base model 对比：

1. JSON 合法率。
2. 字段准确率。
3. 缺字段识别能力。
4. 幻觉率。
5. 对噪声输入的鲁棒性。
6. 输出格式稳定性。

### 人工评估

让业务人员或标注人员按维度打分：

1. 是否正确。
2. 是否完整。
3. 是否有无依据内容。
4. 是否符合业务口径。

### A/B Test

线上灰度对比：

1. 用户采纳率。
2. 人工修正率。
3. 投诉率。
4. 平均处理时长。
5. 单次请求成本。

## 模型导出与部署

### 方式一：加载 base model + LoRA adapter

优点：多个任务可以共用一个 base model。

缺点：推理时需要加载 adapter，部署复杂一点。

### 方式二：Merge LoRA 到基础模型

示例：

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base_model = "Qwen/Qwen2.5-7B-Instruct"
lora_dir = "./outputs/qwen-contract-lora"
merged_dir = "./outputs/qwen-contract-merged"

tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(base_model, device_map="auto", trust_remote_code=True)
model = PeftModel.from_pretrained(model, lora_dir)
model = model.merge_and_unload()

model.save_pretrained(merged_dir)
tokenizer.save_pretrained(merged_dir)
```

部署时可以用 vLLM：

```bash
vllm serve ./outputs/qwen-contract-merged --host 0.0.0.0 --port 8000
```

## 常见坑

1. 数据格式不一致，导致模型输出混乱。
2. 训练样本太少，微调后只会背答案。
3. 把知识问答拿去微调，结果知识更新困难且无法引用来源。
4. 只看训练 loss，不看业务评估集。
5. 训练数据混入测试集，评估结果虚高。
6. 没有脱敏，训练数据泄露敏感信息。
7. 微调后通用能力下降，没有做回归评估。
8. JSON 输出只靠模型，不做服务端 schema 校验。

## 面试常问

### 如何 Fine-tune 一个模型？

我会先判断是否真的需要 Fine-tuning。如果是知识更新优先 RAG，如果是固定任务和输出风格才考虑 SFT。流程上先准备高质量指令数据，选择 Qwen、Llama 等基础模型，用 LoRA 或 QLoRA 低成本训练，然后用独立业务评估集对比 base model，最后合并 adapter 或单独加载 adapter 部署到 vLLM，并监控线上效果。

### LoRA 和 QLoRA 区别是什么？

LoRA 是冻结基础模型，只训练少量低秩 adapter。QLoRA 是把基础模型量化成 4bit 后再训练 LoRA，显存更省，适合资源有限的场景，但需要评估量化对效果的影响。

### Fine-tuning 能不能解决幻觉？

不能彻底解决。Fine-tuning 可以让模型更懂任务格式和领域表达，但不能保证事实正确。需要实时知识、引用来源和权限控制时，仍然要用 RAG 或工具调用。

### 你如何证明微调有效？

我会用独立测试集和 base model 做对比，指标包括字段准确率、JSON 合法率、幻觉率、拒答准确率、延迟和成本。线上再通过灰度观察用户采纳率和人工修正率。
