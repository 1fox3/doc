# ThreadLocal

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：JDK 21 的虚拟线程适合大量阻塞 IO 场景，但不适合 CPU 密集型任务，也不能消除共享状态同步问题。
- 实践：线程池参数应结合任务类型、队列长度、拒绝策略、监控指标和下游容量一起设计。
- 排障：线程问题优先看 `jstack`、线程池队列、活跃线程数、锁等待和上下文切换。

## 详细说明

### 核心概念

- ThreadLocal 为每个线程保存一份独立变量副本，常用于线程上下文、traceId、用户信息、日期格式化对象等。
- 数据实际存放在线程对象的 ThreadLocalMap 中，key 是 ThreadLocal 的弱引用，value 是业务对象。

### 内存泄漏风险

- 线程池中的线程会被复用，如果任务结束后不 remove，value 可能长期挂在线程上。
- 最佳实践是在 `finally` 中调用 `remove()`。

### 面试重点

- ThreadLocal 不是为了解决共享变量竞争，而是用线程隔离避免共享。在线程池、异步任务和父子线程传递场景要特别谨慎。

### 复习检查

- 能用自己的话解释 `ThreadLocal`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `ThreadLocal` 展开，属于 `Java 语言基础` 的复习范围。
- 建议优先掌握：依靠ThreadLocalMap实现。
- 二级节点提示了主要拆分角度：存在Entry[] table数组初始容量为16, ThreadLocal作为Entry的Key，且是弱引用。
- 三级节点通常对应具体细节、API、机制或易错点：弱引用是为了当线程执行结束后，其引用的ThreadLocal对象能被JVM回收, 为避免内存溢出，应在不使用时，用remove方法溢出。

### 复习追问

- `依靠ThreadLocalMap实现` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## ThreadLocal

### 依靠ThreadLocalMap实现

#### 存在Entry[] table数组初始容量为16

#### ThreadLocal作为Entry的Key，且是弱引用

- 弱引用是为了当线程执行结束后，其引用的ThreadLocal对象能被JVM回收

- 为避免内存溢出，应在不使用时，用remove方法溢出
