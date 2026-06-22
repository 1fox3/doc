# JUC 原子类：AtomicInteger / LongAdder / LongAccumulator

## 概述

JUC（`java.util.concurrent`）原子类提供了无锁（lock-free）的线程安全操作，底层依赖 CPU 的 CAS（Compare-And-Swap）指令，避免了 `synchronized` 带来的上下文切换开销。

三个核心类解决的问题层次不同：`AtomicInteger` 适合低并发的单变量原子操作；`LongAdder` 通过分段思想大幅降低高并发下的 CAS 竞争；`LongAccumulator` 是 `LongAdder` 的泛化版本，支持自定义累积函数。

## 核心概念

### AtomicInteger

底层通过 `sun.misc.Unsafe` 提供的 `compareAndSwapInt` 实现原子性。核心流程：读取内存中的当前值 → 与期望值比对 → 若相等则写入新值，否则自旋重试。

关键方法：
- `getAndIncrement()` — 原子自增，返回旧值，等价于 `i++`
- `incrementAndGet()` — 原子自增，返回新值，等价于 `++i`
- `compareAndSet(expect, update)` — 暴露 CAS 语义，失败返回 false

**问题**：高并发场景下大量线程自旋重试，CPU 空转严重。例如 1000 个线程同时对同一个 `AtomicInteger` 执行 `incrementAndGet()`，只有一个线程能成功 CAS，其余 999 个全部重试，竞争越激烈性能越差。

---

### LongAdder

为解决 `AtomicInteger` 在高并发下的自旋瓶颈，`LongAdder` 引入**分段累加**思路：

- 内部维护一个 `base` 基础值和一个 `Cell[]` 数组（`Striped64` 父类实现）
- 无竞争时，所有更新直接 CAS 到 `base`
- CAS 失败（发生竞争）时，将当前线程映射到某个 `Cell`，对该 `Cell` 单独 CAS
- `Cell[]` 长度始终是 2 的次幂，上限为 CPU 核数，**仅在 CAS 失败时才创建或扩容**
- `sum()` 返回 `base + 所有 Cell 的值之和`（非强一致，读取期间可能有并发写入）

**分段原理**：多线程分散到不同 Cell，单个 Cell 的竞争压力远低于单个变量，整体吞吐量大幅提升。

**代价**：Cell 数组占用额外内存；`sum()` 不保证强一致性，只适合统计计数场景。

---

### LongAccumulator

`LongAccumulator` 是 `LongAdder` 的泛化版本，允许自定义累积函数：

```
LongAccumulator(LongBinaryOperator accumulatorFunction, long identity)
```

- `accumulatorFunction`：二元函数 `(currentValue, delta) -> newValue`，必须满足结合律和交换律
- `identity`：累积初始值（相当于 `LongAdder` 的 0）
- 内部同样使用 `Striped64` 的 Cell 分段机制

适用场景：
- 求最大值：`(a, b) -> Math.max(a, b)`，identity 为 `Long.MIN_VALUE`
- 求乘积：`(a, b) -> a * b`，identity 为 1
- 自定义递减：`(a, b) -> a - b`，identity 为初始值

## 示例代码

```java
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.LongAccumulator;
import java.util.concurrent.atomic.LongAdder;

public class AtomicDemo {

    static final int THREAD_COUNT = 50;
    static final int INC_PER_THREAD = 10_000;

    public static void main(String[] args) throws InterruptedException {
        demoAtomicInteger();
        demoLongAdder();
        demoLongAccumulator();
    }

    // AtomicInteger：低并发单变量自增
    static void demoAtomicInteger() throws InterruptedException {
        AtomicInteger counter = new AtomicInteger(0);
        CountDownLatch latch = new CountDownLatch(THREAD_COUNT);

        for (int i = 0; i < THREAD_COUNT; i++) {
            new Thread(() -> {
                for (int j = 0; j < INC_PER_THREAD; j++) {
                    counter.incrementAndGet();
                }
                latch.countDown();
            }).start();
        }
        latch.await();
        System.out.println("AtomicInteger result: " + counter.get());
        // 期望：500000

        // CAS 手动控制示例
        AtomicInteger cas = new AtomicInteger(10);
        boolean success = cas.compareAndSet(10, 20); // true，值变为 20
        boolean fail    = cas.compareAndSet(10, 30); // false，当前值已是 20
        System.out.println("CAS success=" + success + ", fail=" + fail + ", val=" + cas.get());
    }

    // LongAdder：高并发计数，分段减少竞争
    static void demoLongAdder() throws InterruptedException {
        LongAdder adder = new LongAdder();
        CountDownLatch latch = new CountDownLatch(THREAD_COUNT);

        for (int i = 0; i < THREAD_COUNT; i++) {
            new Thread(() -> {
                for (int j = 0; j < INC_PER_THREAD; j++) {
                    adder.increment(); // 等价于 add(1)
                }
                latch.countDown();
            }).start();
        }
        latch.await();
        System.out.println("LongAdder result: " + adder.sum());
        // sum() 读取 base + 所有 Cell 之和，非强一致

        adder.reset(); // 将 base 和所有 Cell 清零
        System.out.println("After reset: " + adder.sum()); // 0
    }

    // LongAccumulator：自定义累积函数（此处演示求最大值）
    static void demoLongAccumulator() throws InterruptedException {
        // identity = Long.MIN_VALUE，函数取最大值
        LongAccumulator maxAcc = new LongAccumulator(Math::max, Long.MIN_VALUE);
        CountDownLatch latch = new CountDownLatch(THREAD_COUNT);

        for (int i = 0; i < THREAD_COUNT; i++) {
            final long val = i * 7L; // 各线程提交不同值
            new Thread(() -> {
                maxAcc.accumulate(val);
                latch.countDown();
            }).start();
        }
        latch.await();
        System.out.println("Max value: " + maxAcc.get());
        // 期望：(50-1)*7 = 343

        // 乘积累加器
        LongAccumulator mulAcc = new LongAccumulator((a, b) -> a * b, 1L);
        mulAcc.accumulate(2);
        mulAcc.accumulate(3);
        mulAcc.accumulate(5);
        System.out.println("Product: " + mulAcc.get()); // 30
    }
}
```

```java
// 对比：AtomicInteger vs LongAdder 高并发吞吐量测试
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.atomic.LongAdder;

public class ThroughputComparison {

    public static void main(String[] args) throws InterruptedException {
        int threads = Runtime.getRuntime().availableProcessors() * 4;
        long duration = 2_000; // ms

        // AtomicLong
        AtomicLong atomicLong = new AtomicLong();
        long atomicOps = benchmark(threads, duration, atomicLong::incrementAndGet);

        // LongAdder
        LongAdder longAdder = new LongAdder();
        long adderOps = benchmark(threads, duration, () -> { longAdder.increment(); return 0L; });

        System.out.printf("AtomicLong ops/s: %,d%n", atomicOps * 1000 / duration);
        System.out.printf("LongAdder  ops/s: %,d%n", adderOps  * 1000 / duration);
        // 高并发下 LongAdder 通常领先 AtomicLong 数倍
    }

    static long benchmark(int threads, long durationMs,
                          java.util.concurrent.Callable<Long> op) throws InterruptedException {
        java.util.concurrent.atomic.AtomicLong total = new java.util.concurrent.atomic.AtomicLong();
        Thread[] ts = new Thread[threads];
        volatile boolean[] running = {true};

        for (int i = 0; i < threads; i++) {
            ts[i] = new Thread(() -> {
                long count = 0;
                while (running[0]) {
                    try { op.call(); } catch (Exception ignored) {}
                    count++;
                }
                total.addAndGet(count);
            });
            ts[i].start();
        }
        Thread.sleep(durationMs);
        running[0] = false;
        for (Thread t : ts) t.join();
        return total.get();
    }
}
```

## 常见问题

**1. LongAdder.sum() 不是强一致的**

`sum()` 遍历 Cell 数组时不加锁，读取期间其他线程可能继续写入，导致返回值不精确。若需要精确快照（如生成报表），应在业务层加锁或改用 `AtomicLong`。`LongAdder` 只适合"近似统计"场景，如 QPS 计数、事件累计。

**2. LongAccumulator 的函数必须满足结合律和交换律**

`accumulate()` 的执行顺序不确定（多线程分散到不同 Cell），若函数不满足交换律（如减法 `a - b`），结果将不确定。例如三个线程分别提交 1、2、3，减法结果可能是 `1-2-3 = -4` 也可能是 `3-1-2 = 0`，取决于执行顺序。

**3. AtomicInteger 的 ABA 问题**

CAS 只比较值，不追踪版本。若值从 A 变为 B 再变回 A，CAS 会误判为"未修改"。需要版本号时应改用 `AtomicStampedReference<Integer>`，它在比较时同时校验 stamp（版本号）。

**4. Cell 数组的内存开销不可忽视**

每个 `Cell` 使用 `@Contended` 注解填充缓存行（64 字节），防止伪共享（false sharing）。在核数较多的机器上，Cell 数组最大可达 CPU 核数个 Cell，每个占 64 字节，整体内存开销需纳入考量。若应用中存在大量 `LongAdder` 实例且核数高，内存压力不可忽视。
