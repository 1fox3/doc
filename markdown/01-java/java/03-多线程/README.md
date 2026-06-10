# 多线程

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：JDK 21 的虚拟线程适合大量阻塞 IO 场景，但不适合 CPU 密集型任务，也不能消除共享状态同步问题。
- 实践：线程池参数应结合任务类型、队列长度、拒绝策略、监控指标和下游容量一起设计。
- 排障：线程问题优先看 `jstack`、线程池队列、活跃线程数、锁等待和上下文切换。

## 详细说明

### 是什么

- `多线程` 是 `Java 语言基础` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `多线程` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `多线程`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 子章节

- [进程间通信](01-进程间通信.md)
- [线程间通信](02-线程间通信.md)
- [创建线程](03-创建线程.md)
- [守护线程](04-守护线程.md)
- [线程状态](05-线程状态.md)
- [线程顺序执行的方法](06-线程顺序执行的方法.md)
- [线程中断](07-线程中断.md)
- [线程异常处理](08-线程异常处理.md)
- [线程终止](09-线程终止.md)
- [CAS](10-cas.md)
- [JUC](11-juc.md)
- [锁](12-锁.md)
- [线程池](13-线程池.md)
- [线程异步](14-线程异步.md)
- [AQS](15-aqs.md)
- [ForkJoin](16-forkjoin.md)
- [ThreadLocal](17-threadlocal.md)
- [volatile](18-volatile.md)
- [线程同步](19-线程同步.md)
- [SimpleDateFormat](20-simpledateformat.md)
- [sleep和wait方法对比](21-sleep和wait方法对比.md)
- [volatile](22-volatile.md)
- [synchronized](23-synchronized.md)
- [volatile与synchronized区别](24-volatile与synchronized区别.md)
- [ReentrantLock](25-reentrantlock.md)
- [ReentrantLock与synchronized](26-reentrantlock与synchronized.md)
- [ReentrantReadWriteLock](27-reentrantreadwritelock.md)
- [StampedLock](28-stampedlock.md)
- [ThreadLocal](29-threadlocal.md)
- [线程池](30-线程池.md)
- [Future](31-future.md)
- [CompletableFuture](32-completablefuture.md)
- [AQS](33-aqs.md)
- [线程同步](34-线程同步.md)
- [Runnable和Callable](35-runnable和callable.md)
- [execute和submit](36-execute和submit.md)
- [shutdown和shutdwonNow](37-shutdown和shutdwonnow.md)
- [isTerminated和isShutdown](38-isterminated和isshutdown.md)
