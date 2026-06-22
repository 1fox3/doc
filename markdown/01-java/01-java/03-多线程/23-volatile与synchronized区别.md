# volatile 与 synchronized 区别

## 概述

`volatile` 和 `synchronized` 是 Java 多线程编程中两种核心的同步机制，但它们解决的问题范围不同。`volatile` 是轻量级的内存可见性保证，通过 CPU 内存屏障指令阻止编译器和处理器对读写操作进行重排序，确保一个线程的写操作对其他线程立即可见，但不提供互斥。`synchronized` 是重量级的互斥锁机制，能同时保证原子性、可见性和有序性，代价是在竞争激烈时涉及操作系统内核的线程调度。

并发编程中存在三个核心问题：原子性（复合操作不可分割）、可见性（写操作结果对其他线程可见）、有序性（禁止破坏程序逻辑的指令重排序）。两者对这三个问题的覆盖范围差异，决定了各自的适用场景。

## 核心概念

### 原子性保证范围

`synchronized` 保证临界区内所有操作的原子性，退出同步块之前不会被其他线程观察到中间状态。`volatile` 只保证单次读或单次写操作本身是原子的（对 64 位 long/double 类型在 32 位 JVM 上 volatile 还额外保证不会出现字撕裂），**不保证复合操作的原子性**。

典型反例：`volatile int i; i++` 等价于 `i = i + 1`，包含读、加、写三步，仍然不是线程安全的操作。

### 可见性保证机制

`volatile` 写操作会在写指令后插入 StoreLoad 屏障，强制将 CPU 缓存行刷新到主存；`volatile` 读操作会在读指令前插入 LoadLoad 屏障，强制从主存重新读取，而不是使用 CPU 缓存值。

`synchronized` 在 monitorenter（进入同步块）时会执行与 volatile 读等价的内存屏障，在 monitorexit（退出同步块）时会执行与 volatile 写等价的内存屏障，因此在同步块内读写的普通变量也具备可见性保证。

### 有序性保证范围

`volatile` 禁止以下两类重排序：
- volatile 写不能被重排序到其之前的任何写操作之后（保证写入顺序）
- volatile 读不能被重排序到其之后的任何读操作之前（保证读取顺序）

这使得 `volatile` 可以充当轻量级的 happens-before 关系建立点。`synchronized` 则通过对象监视器（Monitor）保证临界区内操作相对于外部线程的完整 happens-before 关系，有序性保证更强。

### 修饰对象限制

| 特性 | volatile | synchronized |
|------|----------|--------------|
| 可修饰的目标 | 仅实例变量和静态变量 | 实例方法、静态方法、代码块 |
| 修饰方法 | 不支持 | 支持（实例方法锁 this，静态方法锁 Class 对象） |
| 修饰局部变量 | 不支持 | 不支持（可指定任意对象作为锁） |

### 性能对比

`volatile` 的开销主要来自内存屏障指令，代价是禁止相关代码路径的 CPU 乱序执行优化，通常只有几个纳秒的额外延迟，无上下文切换，无线程阻塞。

`synchronized` 在无竞争时经过 JVM 优化（锁消除、锁粗化、偏向锁/轻量级锁）后开销接近 `volatile`，但在高竞争场景下会膨胀为重量级锁（基于操作系统 Mutex），引发线程挂起和唤醒，上下文切换开销可达微秒级。

JDK 15 起偏向锁被默认禁用并在 JDK 18 中正式移除，但自适应自旋和轻量级锁仍保留，低竞争场景下 `synchronized` 性能依然良好。

### 适用场景选择

**优先使用 volatile 的场景：**
- 单一写线程，多个读线程，且写操作不依赖变量旧值（状态标志位、开关量）
- 双重检查锁（DCL）中保护单例引用，防止半初始化对象泄露
- 发布不可变对象引用（引用的切换是单步操作）

**必须使用 synchronized（或 Lock/原子类）的场景：**
- 复合操作需要原子性（check-then-act、read-modify-write）
- 需要等待/通知机制（wait/notify）
- 多个变量之间存在不变式约束，需要作为一个整体原子更新

## 示例代码

```java
// 示例1：volatile 正确用法 —— 停止标志
public class StopFlagDemo {
    // volatile 保证 running 的写对其他线程立即可见
    private volatile boolean running = true;

    public void stop() {
        running = false; // 单次写，不依赖旧值，volatile 足够
    }

    public void run() {
        while (running) {
            // 业务逻辑
        }
    }
}
```

```java
// 示例2：volatile 的错误用法 —— 复合操作不原子
public class VolatileCounterBug {
    private volatile int count = 0;

    // 错误：i++ 是 read-modify-write，volatile 无法保证原子性
    // 多线程并发调用时 count 最终结果小于期望值
    public void increment() {
        count++; // 非线程安全！
    }

    // 正确做法：改用 AtomicInteger 或 synchronized
}
```

```java
// 示例3：双重检查锁（DCL）—— volatile 的典型正确用法
public class Singleton {
    // volatile 防止 instance = new Singleton() 的指令重排序：
    // 正常顺序：1.分配内存 2.初始化对象 3.赋值引用
    // 无 volatile 时可能重排为：1.分配内存 3.赋值引用 2.初始化对象
    // 另一线程在步骤3之后、步骤2之前读取到非 null 但未完成初始化的引用
    private static volatile Singleton instance;

    private Singleton() {}

    public static Singleton getInstance() {
        if (instance == null) {                   // 第一次检查（无锁）
            synchronized (Singleton.class) {
                if (instance == null) {           // 第二次检查（有锁）
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

```java
// 示例4：synchronized 保证复合操作原子性
public class SafeCounter {
    private int count = 0;

    // synchronized 保证 check-then-act 整体原子执行
    public synchronized void increment() {
        count++;
    }

    public synchronized int getAndReset() {
        int current = count;
        count = 0;
        return current; // 读取和重置是原子的整体操作
    }
}
```

```java
// 示例5：不变式约束 —— 必须用 synchronized，volatile 不够
public class BoundedCounter {
    private int value = 0;
    private final int MAX = 100;

    // value 的读取和条件判断必须在同一个锁保护下
    // 两个 volatile 变量无法保证它们之间的不变式
    public synchronized boolean increment() {
        if (value < MAX) {
            value++;
            return true;
        }
        return false;
    }
}
```

## 常见问题

**1. volatile long/double 在 32 位 JVM 上的字撕裂问题**

在 32 位 JVM 中，64 位的 long 和 double 类型的读写可能被拆分为两个 32 位操作，导致一个线程读到另一个线程写入了一半的脏值（字撕裂）。加上 `volatile` 后 JVM 规范保证这类读写的原子性，可以消除字撕裂风险。64 位 JVM 上通常不存在此问题，但加 volatile 是更安全的做法。

**2. volatile 无法替代 synchronized 保护临界区**

即使将共享变量声明为 volatile，多个线程同时执行 `if (flag) { doSomething(); flag = false; }` 这类 check-then-act 操作时，仍然存在竞态条件。volatile 只保证每次读写看到最新值，不保证操作序列的原子性。

**3. synchronized 的锁对象选择错误导致失效**

对不同实例的实例方法加锁，锁的是不同的对象，多个实例间不互斥。如果需要跨实例的互斥，应锁在静态字段或 Class 对象上。常见错误：在 `synchronized(new Object())` 上同步，每次都是新锁对象，完全不起互斥作用。

**4. 发布可变对象引用时 volatile 不足以保证内部状态安全**

`volatile` 保证引用本身的可见性，但不保护引用指向的对象内部状态。若其他线程在看到新引用后继续修改对象内部字段，仍需对对象内部操作进行同步。volatile 只适合发布不可变对象或完成初始化后不再修改的对象的引用。
