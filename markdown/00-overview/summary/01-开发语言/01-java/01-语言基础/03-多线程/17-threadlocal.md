# ThreadLocal

> 专题：重点汇总
> 来源：重点汇总.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## ThreadLocal

### 依靠ThreadLocalMap实现

#### 存在Entry[] table数组初始容量为16

#### ThreadLocal作为Entry的Key，且是弱引用

- 弱引用是为了当线程执行结束后，其引用的ThreadLocal对象能被JVM回收

- 为避免内存溢出，应在不使用时，用remove方法溢出
