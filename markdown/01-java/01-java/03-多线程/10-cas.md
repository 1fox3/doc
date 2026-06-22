# CAS（Compare And Swap）

## 概述

CAS 是一种无锁的原子操作原语，全称 Compare And Swap（比较并交换）。其语义为：给定内存地址 V、期望值 A、新值 B，当且仅当 V 的当前值等于 A 时，将 V 更新为 B，整个过程是原子的。在 x86 架构上，这对应 `CMPXCHG` 指令，CPU 通过总线锁或缓存锁保证其原子性。

CAS 是乐观锁思想的典型实现：假设并发冲突是少数情况，先乐观地尝试更新，失败则自旋重试，而不是像 `synchronized` 那样悲观地先加锁再操作。Java 并发包（`java.util.concurrent`）中的原子类、AQS（AbstractQueuedSynchronizer）状态更新、`ConcurrentHashMap` 的部分路径，底层都依赖 CAS。

## 核心概念

### 乐观锁原理

乐观锁不阻塞线程，而是在提交时校验是否发生了冲突：

1. 读取当前值 `oldVal`
2. 计算出期望的新值 `newVal`
3. 执行 CAS：若内存值仍为 `oldVal`，则写入 `newVal`，否则重试（自旋）

与悲观锁（`synchronized`、`ReentrantLock`）的对比：

| 维度 | 乐观锁（CAS） | 悲观锁 |
|------|-------------|--------|
| 线程阻塞 | 不阻塞，自旋等待 | 阻塞，上下文切换 |
| 适用场景 | 低竞争、短临界区 | 高竞争、长临界区 |
| CPU 消耗 | 高竞争下空转消耗 CPU | 阻塞后不消耗 CPU |
| 实现复杂度 | 只能保证单变量原子性 | 可保护任意复杂逻辑 |

### Unsafe 类

`sun.misc.Unsafe` 是 Java 提供直接操作内存的后门类，CAS 的 Java 实现依赖它：

```java
// Unsafe 核心 CAS 方法签名
public final native boolean compareAndSwapInt(Object o, long offset, int expected, int update);
public final native boolean compareAndSwapLong(Object o, long offset, long expected, long update);
public final native boolean compareAndSwapObject(Object o, long offset, Object expected, Object update);
```

- `o`：对象引用
- `offset`：字段相对于对象头的内存偏移量（通过 `objectFieldOffset` 获取）
- `expected`：期望的旧值
- `update`：要写入的新值

`Unsafe` 实例无法通过 `new` 或常规方式获取，必须通过反射拿到单例：

```java
Field f = Unsafe.class.getDeclaredField("theUnsafe");
f.setAccessible(true);
Unsafe unsafe = (Unsafe) f.get(null);
```

JDK 9 之后推荐使用 `VarHandle` 替代 `Unsafe`，但底层机制相同。

### AtomicInteger 原理

`AtomicInteger` 的核心字段和自增实现：

```java
// JDK 源码（简化）
public class AtomicInteger extends Number {
    private static final Unsafe U = Unsafe.getUnsafe();
    private static final long VALUE
        = U.objectFieldOffset(AtomicInteger.class, "value");

    private volatile int value;  // volatile 保证可见性

    public final int getAndIncrement() {
        return U.getAndAddInt(this, VALUE, 1);
    }

    public final boolean compareAndSet(int expectedValue, int newValue) {
        return U.compareAndSetInt(this, VALUE, expectedValue, newValue);
    }
}
```

`U.getAndAddInt` 的实现等价于：

```java
// Unsafe.getAndAddInt 的逻辑（自旋 CAS）
public final int getAndAddInt(Object o, long offset, int delta) {
    int v;
    do {
        v = getIntVolatile(o, offset);       // 读取当前值（volatile 读）
    } while (!compareAndSwapInt(o, offset, v, v + delta));  // CAS 失败则重试
    return v;
}
```

`value` 字段声明为 `volatile`，确保每次读取都从主内存获取最新值，防止 CAS 基于过期的缓存值进行判断。

### ABA 问题

ABA 问题是 CAS 的经典缺陷：

```
线程 T1 读取值 A
线程 T2 将 A 改为 B
线程 T2 将 B 改回 A
线程 T1 执行 CAS，发现值仍为 A，认为"没有变化"，更新成功
```

T1 看到的"没有变化"是错觉，中间已经发生过两次修改。在大多数计数器场景下这无害，但在链表/栈等数据结构中，ABA 可能导致节点被错误复用，引发内存错误或逻辑错误。

**`AtomicStampedReference` 解决方案**：

在值的基础上引入版本号（stamp），CAS 时同时比较值和版本号：

```java
// 初始值 "A"，初始版本号 1
AtomicStampedReference<String> ref = new AtomicStampedReference<>("A", 1);

// 线程 T1 读取当前值和版本号
int[] stampHolder = new int[1];
String val = ref.get(stampHolder);  // val="A", stampHolder[0]=1
int stamp = stampHolder[0];

// 模拟 T2 的 ABA 操作
ref.compareAndSet("A", "B", 1, 2);  // A→B，版本 1→2
ref.compareAndSet("B", "A", 2, 3);  // B→A，版本 2→3

// T1 的 CAS 失败：值虽然是 "A"，但版本号已从 1 变为 3
boolean success = ref.compareAndSet("A", "C", stamp, stamp + 1);
System.out.println(success);  // false，ABA 被正确检测
```

`AtomicMarkableReference` 是简化版，版本号退化为一个 boolean 标记，适合只需要"是否修改过"而不关心修改次数的场景。

## 示例代码

### 自旋 CAS 实现无锁计数器

```java
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.CountDownLatch;

public class CasDemo {

    private final AtomicInteger counter = new AtomicInteger(0);

    // 无锁安全自增
    public int increment() {
        return counter.incrementAndGet();
    }

    // 手动演示 CAS 自旋逻辑（等价于 incrementAndGet）
    public int manualIncrement() {
        int oldVal, newVal;
        do {
            oldVal = counter.get();
            newVal = oldVal + 1;
        } while (!counter.compareAndSet(oldVal, newVal));
        return newVal;
    }

    public static void main(String[] args) throws InterruptedException {
        CasDemo demo = new CasDemo();
        int threadCount = 10;
        int incrementsPerThread = 1000;
        CountDownLatch latch = new CountDownLatch(threadCount);

        for (int i = 0; i < threadCount; i++) {
            new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    demo.increment();
                }
                latch.countDown();
            }).start();
        }

        latch.await();
        // 期望输出 10000，无锁下也能保证正确
        System.out.println("Final count: " + demo.counter.get());
    }
}
```

### ABA 问题复现与 AtomicStampedReference 修复

```java
import java.util.concurrent.atomic.AtomicReference;
import java.util.concurrent.atomic.AtomicStampedReference;

public class AbaDemo {

    public static void main(String[] args) throws InterruptedException {

        // ---- 演示 ABA 问题（AtomicReference 无法感知）----
        AtomicReference<String> ref = new AtomicReference<>("A");

        Thread t1 = new Thread(() -> {
            String snapshot = ref.get();  // 读到 "A"
            try { Thread.sleep(100); } catch (InterruptedException e) {}
            // T2 已将值改为 B 再改回 A，但 T1 的 CAS 仍然成功
            boolean ok = ref.compareAndSet(snapshot, "C");
            System.out.println("AtomicReference CAS success (ABA not detected): " + ok);
        });

        Thread t2 = new Thread(() -> {
            ref.compareAndSet("A", "B");  // A → B
            ref.compareAndSet("B", "A");  // B → A（ABA 完成）
        });

        t1.start(); t2.start();
        t1.join(); t2.join();

        // ---- 使用 AtomicStampedReference 解决 ABA ----
        AtomicStampedReference<String> stampedRef = new AtomicStampedReference<>("A", 0);

        Thread t3 = new Thread(() -> {
            int[] stamp = new int[1];
            String val = stampedRef.get(stamp);  // val="A", stamp=0
            int capturedStamp = stamp[0];
            try { Thread.sleep(100); } catch (InterruptedException e) {}
            // 即使值还是 "A"，版本号已变，CAS 失败
            boolean ok = stampedRef.compareAndSet(val, "C", capturedStamp, capturedStamp + 1);
            System.out.println("AtomicStampedReference CAS success (ABA detected): " + ok);
        });

        Thread t4 = new Thread(() -> {
            stampedRef.compareAndSet("A", "B", 0, 1);  // stamp 0→1
            stampedRef.compareAndSet("B", "A", 1, 2);  // stamp 1→2
        });

        t3.start(); t4.start();
        t3.join(); t4.join();
    }
}
```

### 基于 Unsafe 手写原子操作（了解底层）

```java
import sun.misc.Unsafe;
import java.lang.reflect.Field;

public class UnsafeCasDemo {
    private volatile int value = 0;
    private static final Unsafe UNSAFE;
    private static final long VALUE_OFFSET;

    static {
        try {
            Field f = Unsafe.class.getDeclaredField("theUnsafe");
            f.setAccessible(true);
            UNSAFE = (Unsafe) f.get(null);
            VALUE_OFFSET = UNSAFE.objectFieldOffset(
                UnsafeCasDemo.class.getDeclaredField("value"));
        } catch (Exception e) {
            throw new ExceptionInInitializerError(e);
        }
    }

    public boolean compareAndSet(int expected, int update) {
        return UNSAFE.compareAndSwapInt(this, VALUE_OFFSET, expected, update);
    }

    public int get() {
        return value;
    }

    public static void main(String[] args) {
        UnsafeCasDemo demo = new UnsafeCasDemo();
        System.out.println(demo.compareAndSet(0, 1));  // true
        System.out.println(demo.compareAndSet(0, 2));  // false，当前值是 1 不是 0
        System.out.println(demo.get());                 // 1
    }
}
```

## 常见问题

### 自旋消耗 CPU

CAS 失败后会原地自旋重试，在高竞争场景下大量线程持续循环会把 CPU 打满。JDK 8 的 `LongAdder` 通过分段（Cell 数组）降低单点竞争，是高并发计数的更优选择。评估标准：若 CAS 重试次数频繁（可通过 JMX 或 Arthas 观测），应考虑换用锁或分段结构。

### 只能保证单个变量的原子性

CAS 本身只能原子地更新一个内存地址的值。若业务需要同时原子地更新多个变量，CAS 无法直接满足，需要：
- 将多个变量封装为一个不可变对象，用 `AtomicReference` 整体替换
- 或退回使用 `synchronized` / `ReentrantLock`

### ABA 问题被忽视

大多数计数器场景 ABA 无害，但在无锁链表、无锁栈、无锁队列等数据结构中，节点的 ABA 会导致已释放的节点被重新引用，产生难以复现的 bug。凡是通过 CAS 操作指针/引用的场景，都应评估是否需要 `AtomicStampedReference`。

### Unsafe 的使用风险

直接使用 `Unsafe` 绕过了 JVM 的安全检查，错误的 offset 计算或对象类型不匹配会导致 JVM crash，而不是抛出异常。生产代码应优先使用 `AtomicXxx` 系列类或 JDK 9+ 的 `VarHandle`，仅在实现底层框架时才直接操作 `Unsafe`。
