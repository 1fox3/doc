# ReentrantLock与synchronized

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：JDK 21 的虚拟线程适合大量阻塞 IO 场景，但不适合 CPU 密集型任务，也不能消除共享状态同步问题。
- 实践：线程池参数应结合任务类型、队列长度、拒绝策略、监控指标和下游容量一起设计。
- 排障：线程问题优先看 `jstack`、线程池队列、活跃线程数、锁等待和上下文切换。

## 详细说明

### 核心语义

- `synchronized` 提供互斥、可见性和有序性。进入同步块需要获取对象监视器，退出同步块会释放锁。
- 修饰实例方法锁的是当前对象，修饰静态方法锁的是 Class 对象。

### 锁优化

- JVM 曾有偏向锁、轻量级锁、重量级锁等优化路径；新版本中偏向锁已被废弃或移除。
- 锁升级和锁消除、锁粗化等优化都由 JVM 根据运行情况处理。

### 实践建议

- 锁粒度应尽量小，锁内避免 IO、RPC、数据库访问等慢操作。
- 多把锁同时使用时要固定加锁顺序，降低死锁风险。

### 核心能力

- ReentrantLock 是可重入独占锁，基于 AQS 实现。
- 支持公平锁/非公平锁、可中断加锁、超时加锁和多个 Condition 队列。

### 与 synchronized

- synchronized 语法简单，由 JVM 管理释放。
- ReentrantLock 功能更丰富，但必须在 finally 中手动 unlock。

### 复习检查

- 能用自己的话解释 `ReentrantLock与synchronized`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `ReentrantLock与synchronized` 展开，属于 `Java 语言基础` 的复习范围。
- 建议优先掌握：都可重入, synchronized依赖于JVM，ReentrantLock依赖于JDK的API, ReentrantLock比synchronized多了一些功能。
- 二级节点提示了主要拆分角度：可中断, 可实现公平锁, 可实现选择性通知（Condition）。

### 复习追问

- `都可重入` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `synchronized依赖于JVM，ReentrantLock依赖于JDK的API` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `ReentrantLock比synchronized多了一些功能` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## ReentrantLock与synchronized

### 都可重入

### synchronized依赖于JVM，ReentrantLock依赖于JDK的API

### ReentrantLock比synchronized多了一些功能

#### 可中断

#### 可实现公平锁

#### 可实现选择性通知（Condition）
