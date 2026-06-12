# Claude 与 Codex 代码智能体

## 为什么需要单独了解 Claude 和 Codex

Claude 和 Codex 都经常出现在 AI 开发、代码助手、Agent、自动化研发工具相关面试中。

Claude 更偏通用高质量对话、长上下文、工具使用和安全对齐。Codex 最早是 OpenAI 面向代码生成的模型系列，现在 Codex 这个词在很多语境里也泛指代码生成模型、代码智能体或 OpenAI 的代码能力。

面试表达：

> Claude 和 Codex 不是同一类产品。Claude 是 Anthropic 的通用大模型系列，长上下文、推理、安全和工具调用能力比较突出。Codex 最初是 OpenAI 的代码生成模型，后来代码能力融合到 GPT 系列和代码助手产品中。做代码智能体时，核心不是只选模型，而是如何给模型提供仓库上下文、工具能力、权限边界、测试验证和审计。

## Claude 概览

Claude 是 Anthropic 的大模型系列，常用于：

1. 长文档理解。
2. 代码生成和代码审查。
3. 企业知识库问答。
4. Agent 工具调用。
5. 复杂推理和写作。
6. 安全要求较高的企业场景。

Claude 常被关注的能力：

1. 长上下文处理。
2. 指令遵循。
3. 复杂文本理解。
4. Tool Use。
5. Computer Use。
6. 安全对齐。
7. 代码理解与重构。

## Claude API 基本调用

Python SDK 示例：

```bash
pip install anthropic
export ANTHROPIC_API_KEY="你的 API Key"
```

```python
import anthropic


client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-latest",
    max_tokens=1024,
    temperature=0.2,
    system="你是一个资深 Java 后端面试教练，回答要具体。",
    messages=[
        {"role": "user", "content": "请解释 RAG 如何降低幻觉，并给出面试回答。"}
    ],
)

print(message.content[0].text)
```

Claude API 的核心结构：

1. `system`：系统指令。
2. `messages`：用户和助手消息。
3. `model`：模型名称。
4. `max_tokens`：最大输出长度。
5. `temperature`：随机性。
6. `tools`：工具定义。

## Claude 流式输出

聊天产品和代码助手通常需要流式输出。

```python
import anthropic


client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-3-5-sonnet-latest",
    max_tokens=1024,
    messages=[{"role": "user", "content": "写一个 Spring Boot 限流方案的设计说明。"}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

工程注意：

1. 前端可以用 SSE 或 WebSocket 展示 token 流。
2. 后端要支持用户取消生成。
3. 日志记录时要注意脱敏。
4. 长回答需要处理 Markdown 渲染和代码块。

## Claude Tool Use

Claude Tool Use 类似 Function Calling。模型不会直接执行工具，而是输出工具调用请求，由业务服务执行。

示例：查询订单状态。

```python
import anthropic


client = anthropic.Anthropic()


def get_order_status(order_id: str):
    orders = {
        "A1001": {"status": "paid", "delivery": "not_shipped"},
        "A1002": {"status": "refunded", "delivery": "cancelled"},
    }
    return orders.get(order_id, {"error": "order_not_found"})


tools = [
    {
        "name": "get_order_status",
        "description": "根据订单 ID 查询订单状态。",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "订单 ID，例如 A1001。",
                }
            },
            "required": ["order_id"],
        },
    }
]

messages = [
    {"role": "user", "content": "帮我查一下订单 A1001 为什么还没发货。"}
]

response = client.messages.create(
    model="claude-3-5-sonnet-latest",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)

tool_results = []
for block in response.content:
    if block.type == "tool_use" and block.name == "get_order_status":
        result = get_order_status(**block.input)
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": str(result),
        })

messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user", "content": tool_results})

final_response = client.messages.create(
    model="claude-3-5-sonnet-latest",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)

print(final_response.content[0].text)
```

Tool Use 工程原则：

1. 工具 schema 要清楚。
2. 工具执行在服务端。
3. 服务端必须鉴权。
4. 高风险工具需要用户确认。
5. 工具返回结构化结果。
6. 记录工具调用审计日志。

## Claude 与 MCP

MCP 是 Model Context Protocol，用来把外部工具、数据源和上下文以标准协议暴露给模型应用。

可以理解为：

```text
Claude / AI Client -> MCP Client -> MCP Server -> 本地文件、数据库、Git、HTTP API、业务系统
```

MCP 解决的问题：

1. 工具接入标准化。
2. 数据源上下文标准化。
3. 不同 AI 客户端复用同一套工具。
4. 本地开发工具和企业系统更容易接入模型。

常见 MCP Server：

1. 文件系统。
2. Git。
3. GitHub。
4. 数据库。
5. Slack、Notion、Jira。
6. 自定义业务 API。

面试表达：

> MCP 可以看作模型应用和外部工具之间的标准协议。以前每个 Agent 框架都要自己适配工具，现在可以通过 MCP Server 暴露资源和工具，AI Client 通过统一协议访问。生产中仍然要做权限控制、审计和工具边界限制。

## Claude Computer Use

Computer Use 是让模型通过工具操作电脑界面，例如看截图、移动鼠标、点击按钮、输入文本。

适合：

1. UI 自动化。
2. 跨系统操作。
3. 无 API 的旧系统自动化。
4. 测试和浏览器任务。

风险：

1. 操作不可控。
2. 误点击。
3. 敏感信息暴露。
4. 成本和延迟高。
5. 难以稳定复现。

工程建议：

1. 优先 API 自动化，不要优先 UI 自动化。
2. 限制可访问应用和页面。
3. 高风险动作人工确认。
4. 记录截图和操作轨迹。
5. 使用沙箱环境。

## Claude Artifacts

Artifacts 是 Claude 产品里的交互式内容区域，常用于生成和迭代代码、文档、网页、图表等。

面试中不需要强调产品 UI，而要讲背后的应用形态：

1. 模型生成结构化可编辑内容。
2. 用户可以持续迭代同一个产物。
3. 前端需要把对话和产物状态分离。
4. 后端需要管理版本、diff、保存和回滚。

类似能力可以用于：

1. 在线代码生成器。
2. 文档协作。
3. SQL 报表生成。
4. 页面原型生成。
5. 配置文件生成。

## Codex 是什么

Codex 最早是 OpenAI 面向代码生成和理解的模型系列，支撑过自然语言转代码、代码补全、代码解释等场景。

现在很多代码能力已经融合进 GPT 系列和各类代码助手产品中。面试中提 Codex 时，可以泛指代码模型和代码智能体能力。

Codex 典型能力：

1. 代码补全。
2. 根据自然语言生成代码。
3. 解释代码。
4. 生成单元测试。
5. 修复报错。
6. 代码重构。
7. 多文件代码修改。

## Codex / 代码模型的输入输出

代码模型不是只看用户一句话，效果取决于上下文。

常见上下文：

1. 当前文件。
2. 相关文件。
3. 函数签名。
4. 调用关系。
5. 错误堆栈。
6. 测试用例。
7. README 和开发规范。
8. 依赖版本。

输出不应该直接信任，需要：

1. 编译。
2. 单测。
3. 静态检查。
4. 安全扫描。
5. 人工 review。

## 代码智能体架构

一个代码助手或 Codex-like Agent 通常这样设计：

```text
用户需求 -> 仓库索引 -> 相关代码检索 -> 计划 -> 代码修改 -> 测试 -> 总结
```

核心模块：

1. Repository Indexer：索引文件、符号、依赖、调用关系。
2. Context Builder：选择相关上下文，控制 token 预算。
3. Planner：拆分修改步骤。
4. Code Editor：生成 patch，而不是整文件重写。
5. Tool Runner：运行测试、lint、build。
6. Reviewer：检查潜在问题。
7. Audit Logger：记录修改、命令和结果。

面试表达：

> 代码智能体的核心是上下文工程和验证闭环。模型必须先理解仓库结构和相关调用链，再生成最小 patch，最后通过测试、lint 和 review 验证。不能让模型凭空写代码，也不能让它随意改无关文件。

## Demo：简单代码修复 Agent 思路

下面是一个简化版代码智能体流程，不直接操作真实仓库，只展示架构。

```python
from dataclasses import dataclass
from typing import List


@dataclass
class FileContext:
    path: str
    content: str


def retrieve_related_files(issue: str) -> List[FileContext]:
    # 真实项目中这里会用 grep、AST、向量检索、调用图等方式找相关文件。
    return [
        FileContext(
            path="order_service.py",
            content="""
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total
""",
        ),
        FileContext(
            path="test_order_service.py",
            content="""
def test_calculate_total_with_quantity():
    items = [Item(price=10, quantity=2)]
    assert calculate_total(items) == 20
""",
        ),
    ]


def build_prompt(issue: str, files: List[FileContext]) -> str:
    context = "\n\n".join(
        f"文件：{file.path}\n```python\n{file.content}\n```"
        for file in files
    )
    return f"""
你是一个代码修复助手。
要求：
1. 只修改必要代码。
2. 输出 unified diff。
3. 不要重写无关文件。

问题：{issue}

相关上下文：
{context}
"""


def call_code_model(prompt: str) -> str:
    # 真实项目中这里调用 Claude、GPT、代码模型或内部模型网关。
    return """
--- a/order_service.py
+++ b/order_service.py
@@
 def calculate_total(items):
     total = 0
     for item in items:
-        total += item.price
+        total += item.price * item.quantity
     return total
"""


def run_tests() -> bool:
    # 真实项目中执行 pytest、mvn test、npm test 等命令。
    return True


def main():
    issue = "calculate_total 没有处理商品 quantity，导致总价计算错误。"
    files = retrieve_related_files(issue)
    prompt = build_prompt(issue, files)
    patch = call_code_model(prompt)
    print(patch)

    if run_tests():
        print("tests passed")
    else:
        print("tests failed, ask model to fix based on test output")


if __name__ == "__main__":
    main()
```

真实代码 Agent 需要补充：

1. 安全沙箱。
2. 文件读写权限控制。
3. patch apply 校验。
4. 测试命令白名单。
5. 失败重试策略。
6. 人工 review。

## Claude vs Codex / GPT Code 能力对比

| 维度 | Claude | Codex / GPT Code |
| --- | --- | --- |
| 主要定位 | 通用助手、长上下文、Agent、安全 | 代码生成、代码补全、代码智能体 |
| 长文档理解 | 强 | 取决于具体模型 |
| 代码生成 | 强 | 强 |
| 代码补全 | 可做，但不是唯一定位 | 经典优势场景 |
| 工具调用 | Tool Use、MCP、Computer Use | Function Calling、工具调用、代码执行环境 |
| 企业安全 | 强调安全对齐 | 依赖产品和部署策略 |
| 典型场景 | 文档、Agent、代码审查、长上下文 | IDE Copilot、代码生成、自动修复 |

注意：不同版本模型能力变化很快，面试中不要死背某个版本强弱，更应该讲如何评估模型。

## 如何评估 Claude 或 Codex 是否适合代码助手

评估维度：

1. 单文件补全准确率。
2. 多文件修改能力。
3. 是否能遵循项目风格。
4. 是否会编造不存在的 API。
5. 测试通过率。
6. 修复 bug 的成功率。
7. 生成代码安全性。
8. 延迟和成本。
9. 长上下文下的稳定性。
10. 工具调用准确率。

评估方法：

1. 从真实 issue 中抽样。
2. 准备标准测试集。
3. 让模型生成 patch。
4. 自动运行测试。
5. 人工 review patch 质量。
6. 统计一次成功率和平均修复轮数。

## 代码智能体的风险

1. 修改范围过大。
2. 编造不存在的函数或配置。
3. 只修测试不修逻辑。
4. 删除安全校验。
5. 引入性能问题。
6. 泄露代码和密钥。
7. 执行危险命令。
8. 破坏用户未提交改动。

防护：

1. 最小权限。
2. 沙箱运行。
3. 禁止危险命令。
4. patch 级修改。
5. 测试和 lint 必须通过。
6. 敏感文件保护。
7. 人工 review。
8. 完整审计日志。

## 面试常问

### Claude 有什么特点？

Claude 是 Anthropic 的通用大模型系列，特点是长上下文、指令遵循、复杂文本理解、安全对齐和工具使用能力较强，适合企业知识库、文档处理、Agent 和代码审查等场景。

### Claude Tool Use 怎么理解？

Tool Use 是模型根据用户目标选择工具并生成参数，真正执行工具的是后端服务。服务端执行后把结果返回给模型，模型再基于结果生成最终回答。权限、幂等、审计和高风险确认都必须在服务端做。

### MCP 是什么？

MCP 是 Model Context Protocol，用统一协议把外部工具和数据源暴露给 AI 应用。它让文件系统、GitHub、数据库、企业 API 等能力可以通过标准方式接入 Claude 或其他 AI 客户端，但安全边界仍然要靠权限控制和审计。

### Codex 是什么？

Codex 最早是 OpenAI 的代码生成模型，擅长自然语言转代码、代码补全、解释和修复。现在代码能力更多融合在 GPT 系列和代码助手产品中，面试中可以把 Codex 理解为代码模型或代码智能体能力的代表。

### 如何设计一个 Codex-like 代码助手？

我会先做仓库索引，包括文件、符号和调用关系；然后根据用户问题检索相关上下文；模型生成修改计划和 patch；系统应用 patch 后运行测试、lint 和 build；失败时把错误反馈给模型迭代；最终由人工 review 合入。关键是上下文准确、修改最小、验证闭环和权限控制。

### Claude 和 Codex 怎么选？

如果任务偏长文档理解、复杂推理、Agent 和安全对齐，可以优先考虑 Claude。如果任务偏 IDE 补全、代码生成和自动修复，可以评估 Codex/GPT Code 类模型。但最终要用真实代码任务、测试通过率、延迟和成本来评估，而不是只看模型宣传。
