# sleep和wait方法对比

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## sleep和wait方法对比

### sleep方法没有释放锁，而wait释放了锁

### wait通常用于线程间交互和通信，sleep通常用于暂停执行

### wait调用后不会自动苏醒，需要别的线程在同一个对象上调用notifyAll或notify，sleep方法会自动苏醒，wait（timeout）超时后也会自动苏醒

### sleep是Thread的方法，wait是Object的本地方法
