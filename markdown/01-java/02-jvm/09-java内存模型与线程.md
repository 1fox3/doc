# Java 内存模型与线程

Java 内存模型 JMM 定义线程之间如何通过内存交互，以及 JVM、编译器和处理器在保证正确性的前提下可以做哪些重排序。它是理解 `volatile`、`synchronized`、`final`、CAS 和安全发布的基础。

## 核心问题

- 原子性：操作是否不可分割。
- 可见性：一个线程修改共享变量后，其他线程何时可见。
- 有序性：程序执行顺序与源码顺序、编译器重排序、CPU 重排序之间的关系。

## 主内存与工作内存

- JMM 把共享变量存放在主内存中。
- 每个线程有自己的工作内存，保存共享变量副本。
- 线程对共享变量的读写需要经过工作内存，不能直接读写其他线程的工作内存。

## 内存交互操作

- `lock`：把主内存变量标记为线程独占。
- `unlock`：释放主内存变量锁定。
- `read`：从主内存读取变量值。
- `load`：把 read 得到的值放入工作内存变量副本。
- `use`：把工作内存变量值传递给执行引擎。
- `assign`：把执行引擎结果赋给工作内存变量。
- `store`：把工作内存变量值传送到主内存。
- `write`：把 store 的值写入主内存变量。

这些操作是 JMM 的抽象描述，不等同于具体 CPU 指令。

## volatile

- 保证变量读写的可见性。
- 禁止特定类型的指令重排序。
- 单次读写具有原子性，但复合操作如 `i++` 不具备原子性。
- 写 `volatile` 变量前的普通写，对之后读到该 `volatile` 的线程可见。
- `volatile` 适合状态标记、发布引用和单写多读场景，不适合替代锁保护复合不变量。

### volatile 屏障语义

- volatile 写前通常需要 StoreStore，写后需要 StoreLoad，防止前面的普通写被重排到 volatile 写之后，也防止后续读写越过 volatile 写。
- volatile 读后通常需要 LoadLoad 和 LoadStore，防止后续普通读写被重排到 volatile 读之前。
- 具体屏障映射取决于 CPU 架构，JMM 约束的是 Java 程序可观察语义。

## 内存屏障

- LoadLoad：禁止前后读操作重排序。
- LoadStore：禁止前读后写重排序。
- StoreStore：禁止前后写操作重排序。
- StoreLoad：禁止前写后读重排序，成本通常最高。
- `volatile`、锁、CAS 和 VarHandle 会按语义插入相应屏障。

## happens-before 规则

- 程序次序规则：单线程内前面的操作先行发生于后面的操作。
- 锁规则：同一个锁的 unlock 先行发生于后续 lock。
- volatile 规则：对 volatile 变量的写先行发生于后续读。
- 传递规则：如果 A 先行发生于 B，B 先行发生于 C，则 A 先行发生于 C。
- 线程启动规则：`Thread.start()` 先行发生于新线程中的动作。
- 线程终止规则：线程中所有操作先行发生于其他线程检测到该线程终止。
- 线程中断规则：调用 `interrupt()` 先行发生于被中断线程检测到中断。
- 对象终结规则：对象构造完成先行发生于 `finalize()` 执行。

### happens-before 理解

- happens-before 不等于物理时间先后，而是 JMM 定义的可见性和有序性关系。
- 如果两个操作之间没有 happens-before，JVM 和 CPU 可以在不破坏单线程语义的前提下重排序，读到旧值也是允许的。
- 正确并发程序应通过锁、volatile、线程启动/终止、并发工具类等建立明确的 happens-before。

## final 语义

- 构造函数中对 `final` 字段的写，正常构造完成后对其他线程可见。
- 如果构造期间 `this` 逸出，`final` 安全保证可能被破坏。
- `final` 引用保证引用本身初始化可见，不保证引用对象内部可变字段不可变。

## CAS 与内存语义

- CAS 成功通常同时具备读和写的内存语义，失败也至少读取了当前值。
- `Atomic*`、AQS、并发队列和锁实现大量依赖 CAS 和 volatile 字段配合。
- VarHandle 提供 plain、opaque、acquire、release、volatile 等不同访问模式，可按需要选择更精确的内存语义。

## synchronized 内存语义

- 进入 synchronized 块相当于 acquire，退出 synchronized 块相当于 release。
- 对同一把锁，前一次 unlock happens-before 后一次 lock。
- synchronized 同时提供互斥、可见性和有序性约束，volatile 只适合单变量可见性和有序性场景。

## DCL 单例

```java
class Singleton {
    private static volatile Singleton instance;

    static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

- `volatile` 防止对象引用赋值与构造过程相关写入发生不安全重排序。
- 外层判空减少加锁开销，内层判空保证并发下只创建一次。
- 更简单的写法是静态内部类或枚举单例，利用类初始化的线程安全保证。

## 指令重排序

- 编译器重排序：JIT 在不改变单线程语义的前提下调整指令。
- 处理器重排序：CPU 为流水线和缓存优化调整执行顺序。
- 内存系统重排序：缓存、写缓冲区导致其他处理器观察到的顺序变化。
- happens-before 和内存屏障约束这些重排序对多线程程序的可见行为。

## 线程状态

- `NEW`：线程对象已创建但未启动。
- `RUNNABLE`：可运行或正在运行，包括等待 CPU 时间片。
- `BLOCKED`：等待进入 synchronized 监视器。
- `WAITING`：无限期等待其他线程动作，例如 `Object.wait()`、`Thread.join()`。
- `TIMED_WAITING`：限时等待，例如 `sleep()`、带超时的 `wait()`。
- `TERMINATED`：线程已结束。

## 安全发布

- 使用静态初始化发布对象。
- 使用 `volatile` 引用发布对象。
- 使用锁保护对象发布和访问。
- 使用线程安全容器发布对象。
- 避免构造函数中启动线程、注册回调或把 `this` 暴露给其他对象。

## 常见并发错误

- 双重检查锁如果没有 `volatile`，可能因对象引用发布早于构造完成而读到半初始化对象。
- 只用 `volatile` 保护多个字段时，不能保证跨字段不变量一致。
- 依赖 `sleep()` 或时间等待建立可见性是不可靠的，应使用锁、volatile、CountDownLatch、Future 等同步机制。
