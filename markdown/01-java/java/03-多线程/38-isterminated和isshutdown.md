# isTerminated和isShutdown

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 核心区别

- `isShutdown` 表示线程池已经开始关闭，不再接收新任务。
- `isTerminated` 表示线程池关闭流程完成，所有任务都已结束。

### 实践

- 判断线程池是否完全退出应使用 `awaitTermination` 或 `isTerminated`，不能只看 `isShutdown`。

### 复习检查

- 能用自己的话解释 `isTerminated和isShutdown`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `isTerminated和isShutdown` 展开，属于 `Java 语言基础` 的复习范围。
- 建议优先掌握：当调用shutdown后，isShutDown方法返回true, 调用shutdown后，所有提交任务完成后，isTerminated返回true。

### 复习追问

- `当调用shutdown后，isShutDown方法返回true` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `调用shutdown后，所有提交任务完成后，isTerminated返回true` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## isTerminated和isShutdown

### 当调用shutdown后，isShutDown方法返回true

### 调用shutdown后，所有提交任务完成后，isTerminated返回true
