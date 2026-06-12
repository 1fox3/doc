# 多线程

Java 多线程核心知识体系，涵盖线程基础、锁机制、并发工具、线程池与异步编程。

## 目录

| 文件 | 主题 |
|------|------|
| [01-进程间通信](01-进程间通信.md) | IPC：管道、消息队列、Socket、RPC |
| [02-线程间通信](02-线程间通信.md) | wait/notify、Condition、BlockingQueue、LockSupport |
| [03-创建线程](03-创建线程.md) | Thread、Runnable、Callable、线程池 |
| [04-守护线程](04-守护线程.md) | Daemon Thread、setDaemon |
| [05-线程状态](05-线程状态.md) | NEW/RUNNABLE/BLOCKED/WAITING/TIMED_WAITING/TERMINATED |
| [06-线程顺序执行的方法](06-线程顺序执行的方法.md) | join、Condition.await、CountDownLatch |
| [07-线程中断](07-线程中断.md) | interrupt、isInterrupted、sleep/wait 区别、yield |
| [08-线程异常处理](08-线程异常处理.md) | UncaughtExceptionHandler、Future.get、afterExecute |
| [09-线程终止](09-线程终止.md) | volatile 标志、interrupt 协作、shutdown |
| [10-cas](10-cas.md) | CAS 原理、Unsafe、ABA 问题、AtomicStampedReference |
| [11-juc](11-juc.md) | AtomicInteger、LongAdder、LongAccumulator |
| [12-锁](12-锁.md) | synchronized、ReentrantLock、ReadWriteLock、StampedLock |
| [13-线程池](13-线程池.md) | ThreadPoolExecutor 7参数、拒绝策略、命名、监控、关闭 |
| [14-线程异步](14-线程异步.md) | Future、CompletableFuture、@Async |
| [15-aqs](15-aqs.md) | AQS 原理：state、CLH 队列、Node、Condition、独占/共享模式 |
| [16-forkjoin](16-forkjoin.md) | ForkJoinPool、RecursiveTask、work-stealing |
| [17-threadlocal](17-threadlocal.md) | ThreadLocal、InheritableThreadLocal、TTL、内存泄漏 |
| [18-volatile](18-volatile.md) | 可见性、有序性、内存屏障、发布模式、DCL 单例 |
| [19-线程同步](19-线程同步.md) | CountDownLatch、CyclicBarrier、Semaphore、Exchanger、LockSupport 对比 |
| [20-simpledateformat](20-simpledateformat.md) | 线程不安全原因、ThreadLocal/DateTimeFormatter 方案 |
| [21-sleep和wait方法对比](21-sleep和wait方法对比.md) | sleep vs wait：所属类、锁释放、唤醒方式 |
| [22-synchronized](22-synchronized.md) | monitorenter/monitorexit、锁升级、JDK6 优化 |
| [23-volatile与synchronized区别](23-volatile与synchronized区别.md) | 原子性/可见性/有序性对比 |
| [24-reentrantlock](24-reentrantlock.md) | 可重入、公平锁、tryLock、Condition |
| [25-reentrantlock与synchronized](25-reentrantlock与synchronized.md) | 功能对比：可中断、公平锁、多条件队列 |
| [26-reentrantreadwritelock](26-reentrantreadwritelock.md) | 读读共享、读写互斥、锁降级 |
| [27-stampedlock](27-stampedlock.md) | 乐观读、stamp 戳、三种模式 |
