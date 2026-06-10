# sleep和wait方法对比

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 核心区别

- `sleep` 是 Thread 的静态方法，不释放对象锁。
- `wait` 是 Object 方法，必须在 synchronized 中调用，调用后会释放对象锁并进入等待队列。
- `wait` 需要通过 `notify/notifyAll` 或超时唤醒，唤醒后还要重新竞争锁。

### 实践建议

- 生产代码中更推荐使用 `CountDownLatch`、`Condition`、BlockingQueue 等更高层并发工具。

### 复习检查

- 能用自己的话解释 `sleep和wait方法对比`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `sleep和wait方法对比` 展开，属于 `Java 语言基础` 的复习范围。
- 建议优先掌握：sleep方法没有释放锁，而wait释放了锁, wait通常用于线程间交互和通信，sleep通常用于暂停执行, wait调用后不会自动苏醒，需要别的线程在同一个对象上调用notifyAll或notify，sleep方法会自动苏醒，wait（timeout）超时后也会自动苏醒, sleep是Thread的方法，wait是Object的本地方法。

### 复习追问

- `sleep方法没有释放锁，而wait释放了锁` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `wait通常用于线程间交互和通信，sleep通常用于暂停执行` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `wait调用后不会自动苏醒，需要别的线程在同一个对象上调用notifyAll或notify，sleep方法会自动苏醒，wait（timeout）超时后也会自动苏醒` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `sleep是Thread的方法，wait是Object的本地方法` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## sleep和wait方法对比

### sleep方法没有释放锁，而wait释放了锁

### wait通常用于线程间交互和通信，sleep通常用于暂停执行

### wait调用后不会自动苏醒，需要别的线程在同一个对象上调用notifyAll或notify，sleep方法会自动苏醒，wait（timeout）超时后也会自动苏醒

### sleep是Thread的方法，wait是Object的本地方法
