# 多线程

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：JDK 21 的虚拟线程适合大量阻塞 IO 场景，但不适合 CPU 密集型任务，也不能消除共享状态同步问题。
- 实践：线程池参数应结合任务类型、队列长度、拒绝策略、监控指标和下游容量一起设计。
- 排障：线程问题优先看 `jstack`、线程池队列、活跃线程数、锁等待和上下文切换。

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
