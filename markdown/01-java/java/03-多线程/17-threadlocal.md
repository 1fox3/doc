# ThreadLocal

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：JDK 21 的虚拟线程适合大量阻塞 IO 场景，但不适合 CPU 密集型任务，也不能消除共享状态同步问题。
- 实践：线程池参数应结合任务类型、队列长度、拒绝策略、监控指标和下游容量一起设计。
- 排障：线程问题优先看 `jstack`、线程池队列、活跃线程数、锁等待和上下文切换。

## 脑图内容

## ThreadLocal

### 依靠ThreadLocalMap实现

#### 存在Entry[] table数组初始容量为16

#### ThreadLocal作为Entry的Key，且是弱引用

- 弱引用是为了当线程执行结束后，其引用的ThreadLocal对象能被JVM回收

- 为避免内存溢出，应在不使用时，用remove方法溢出
