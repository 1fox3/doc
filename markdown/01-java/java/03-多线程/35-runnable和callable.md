# Runnable和Callable

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 核心区别

- Runnable 的 `run` 没有返回值，不能直接抛出受检异常。
- Callable 的 `call` 有返回值，可以抛出异常，通常配合 Future 使用。

### 实践

- 需要异步结果或异常传递时使用 Callable/Future/CompletableFuture。

### 复习检查

- 能用自己的话解释 `Runnable和Callable`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `Runnable和Callable` 展开，属于 `Java 语言基础` 的复习范围。
- 建议优先掌握：Runnable在JDK1.0开始存在，Callable仅在JDK1.5时存在, Runnable没有返回结果和抛出异常检查，但Callable可以, Runnable提供run方法，Callable提供call方法。

### 复习追问

- `Runnable在JDK1.0开始存在，Callable仅在JDK1.5时存在` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `Runnable没有返回结果和抛出异常检查，但Callable可以` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `Runnable提供run方法，Callable提供call方法` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## Runnable和Callable

### Runnable在JDK1.0开始存在，Callable仅在JDK1.5时存在

### Runnable没有返回结果和抛出异常检查，但Callable可以

### Runnable提供run方法，Callable提供call方法
