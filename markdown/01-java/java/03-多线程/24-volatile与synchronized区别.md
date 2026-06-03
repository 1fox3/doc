# volatile与synchronized区别

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：JDK 21 的虚拟线程适合大量阻塞 IO 场景，但不适合 CPU 密集型任务，也不能消除共享状态同步问题。
- 实践：线程池参数应结合任务类型、队列长度、拒绝策略、监控指标和下游容量一起设计。
- 排障：线程问题优先看 `jstack`、线程池队列、活跃线程数、锁等待和上下文切换。

## 脑图内容

## volatile与synchronized区别

### volatile关键字时线程同步的轻量级实现，性能比synchronized要好

### volatile只能用于修饰变量，synchronized可以修饰方法以及代码块

### volatile只能保证数据的可见性，synchronized可以保证可见性和原子性

### volatile主要用于解决变量在多个线程之间的可见性，synchronized解决多个线程之间访问资源的同步性
