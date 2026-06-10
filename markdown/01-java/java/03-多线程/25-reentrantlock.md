# ReentrantLock

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 核心能力

- ReentrantLock 是可重入独占锁，基于 AQS 实现。
- 支持公平锁/非公平锁、可中断加锁、超时加锁和多个 Condition 队列。

### 与 synchronized

- synchronized 语法简单，由 JVM 管理释放。
- ReentrantLock 功能更丰富，但必须在 finally 中手动 unlock。

### 复习检查

- 能用自己的话解释 `ReentrantLock`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `ReentrantLock` 展开，属于 `Java 语言基础` 的复习范围。
- 建议优先掌握：可重入锁, 内部类Sync继承AQS，并且有公平锁(FairSync)和非公平锁(NonfairSync)两个子类。

### 复习追问

- `可重入锁` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `内部类Sync继承AQS，并且有公平锁(FairSync)和非公平锁(NonfairSync)两个子类` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## ReentrantLock

### 可重入锁

### 内部类Sync继承AQS，并且有公平锁(FairSync)和非公平锁(NonfairSync)两个子类
