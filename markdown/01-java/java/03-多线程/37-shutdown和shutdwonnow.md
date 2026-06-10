# shutdown和shutdwonNow

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 核心区别

- `shutdown`：停止接收新任务，已提交任务继续执行。
- `shutdownNow`：尝试中断正在执行的任务，并返回队列中尚未执行的任务。

### 实践建议

- 优雅停机通常先 shutdown，再 awaitTermination，超时后再 shutdownNow。任务本身也要响应中断。

### 复习检查

- 能用自己的话解释 `shutdown和shutdwonNow`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图内容

## shutdown和shutdwonNow
