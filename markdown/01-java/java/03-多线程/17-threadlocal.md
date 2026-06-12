# ThreadLocal、InheritableThreadLocal 与内存泄漏

## 概述

ThreadLocal 为每个线程维护一份独立的变量副本，核心目标不是解决共享变量竞争，而是通过线程隔离来彻底避免共享。常见使用场景包括：traceId 传递、用户会话信息、数据库 Connection 绑定、SimpleDateFormat 实例复用等。

数据实际存储在每个 `Thread` 对象内部的 `ThreadLocalMap` 字段中，而非 ThreadLocal 实例本身。ThreadLocal 只是一个访问入口，线程终止时其 ThreadLocalMap 随之被 GC 回收，天然实现了线程级别的生命周期隔离。

## 核心概念

### ThreadLocalMap 内部结构

`ThreadLocalMap` 是 ThreadLocal 的静态内部类，不继承 `HashMap`，采用开放地址法（线性探测）解决哈希冲突。

- `Entry[] table`：初始容量 16，负载因子 2/3，超过阈值执行 rehash
- `Entry` 继承 `WeakReference<ThreadLocal<?>>`：key（ThreadLocal 实例）是弱引用，value 是强引用
- 哈希索引计算：`threadLocalHashCode & (len - 1)`，其中 `threadLocalHashCode` 通过魔数 `0x61c88647` 递增，实现 Fibonacci 散列，减少冲突

```
Thread
 └── threadLocals: ThreadLocalMap
      └── Entry[] table
           └── Entry (WeakReference<ThreadLocal>, Object value)
```

### 弱引用 Key 的设计意图

将 ThreadLocal 实例作为弱引用 key，目的是：当外部不再持有 ThreadLocal 的强引用时，GC 可以回收 ThreadLocal 对象，此时 Entry 的 key 变为 `null`。

这样设计可以防止 ThreadLocal 实例本身无法被回收，但 **value 仍然是强引用**，不会被自动回收。

### 内存泄漏的根本原因

内存泄漏发生的条件：

1. ThreadLocal 实例没有外部强引用（key 被 GC 回收，变为 null）
2. 线程仍然存活（尤其是线程池中的复用线程）
3. 没有调用 `remove()` 清理

此时 Entry 变为 `key=null, value=业务对象` 的孤立条目，value 因为被 Entry 强引用而无法回收，持续占用内存。

ThreadLocalMap 在 `set()`、`get()`、`remove()` 时会顺带清理 key 为 null 的 Entry（`expungeStaleEntry` 方法），但这是被动触发，在线程池场景下不可依赖。

### InheritableThreadLocal

`InheritableThreadLocal` 在创建子线程时，将父线程的 `inheritableThreadLocals` 浅拷贝到子线程，实现父子线程间的上下文传递。

局限性：
- 仅在线程**创建时**拷贝一次，之后父子线程的副本相互独立
- 线程池复用线程，子线程并非每次任务都重新创建，因此 `InheritableThreadLocal` 在线程池场景下**无法正确传递上下文**
- 解决方案：使用阿里开源的 `TransmittableThreadLocal`（TTL），通过包装 Runnable/Callable 在任务提交和执行时主动传递上下文

### TransmittableThreadLocal（TTL）

`TransmittableThreadLocal` 用于解决线程池场景下父线程上下文无法传递的问题。核心流程：

1. 任务提交时，通过 `TtlRunnable` / `TtlCallable` 捕获当前线程的上下文快照。
2. 任务执行前，把快照还原到工作线程。
3. 任务执行后，清理并恢复工作线程原来的上下文，避免污染后续任务。

推荐统一用 `TtlExecutors.getTtlExecutorService(pool)` 包装线程池，避免某些提交路径忘记包装任务。

## 示例代码

### 基本用法与 remove 最佳实践

```java
public class ThreadLocalDemo {

    // 推荐声明为 static final，避免多个实例造成混乱
    private static final ThreadLocal<String> TRACE_ID = new ThreadLocal<>();

    public void handleRequest(String traceId) {
        try {
            TRACE_ID.set(traceId);
            processBusinessLogic();
        } finally {
            // 必须在 finally 中 remove，防止线程池复用时数据污染
            TRACE_ID.remove();
        }
    }

    private void processBusinessLogic() {
        // 在调用链任意位置获取，无需参数传递
        String traceId = TRACE_ID.get();
        System.out.println("Processing with traceId: " + traceId);
    }
}
```

### 线程池中的内存泄漏演示

```java
public class ThreadPoolLeakDemo {

    private static final ThreadLocal<byte[]> LEAK_PRONE = new ThreadLocal<>();

    public static void main(String[] args) throws InterruptedException {
        ExecutorService pool = Executors.newFixedThreadPool(2);

        for (int i = 0; i < 10; i++) {
            pool.execute(() -> {
                // 每次任务 set 1MB 数据，但没有 remove
                LEAK_PRONE.set(new byte[1024 * 1024]);

                // 模拟业务处理
                doWork();

                // 线程归还到池中，ThreadLocalMap 中的 Entry 仍然存活
                // 下次该线程执行新任务时，旧的 value 依然在 map 中
            });
        }

        pool.shutdown();
    }

    // 正确写法：
    public static void correctUsage(ExecutorService pool) {
        pool.execute(() -> {
            try {
                LEAK_PRONE.set(new byte[1024 * 1024]);
                doWork();
            } finally {
                LEAK_PRONE.remove(); // 任务结束前强制清理
            }
        });
    }

    private static void doWork() { /* 业务逻辑 */ }
}
```

### InheritableThreadLocal 与线程池的问题

```java
public class InheritableDemo {

    private static final InheritableThreadLocal<String> USER_CONTEXT =
            new InheritableThreadLocal<>();

    public static void main(String[] args) throws InterruptedException {
        ExecutorService pool = Executors.newFixedThreadPool(1);

        // 第一次提交：父线程设置用户 A
        USER_CONTEXT.set("UserA");
        pool.submit(() -> {
            // 线程首次创建时继承父线程上下文，输出 UserA（正确）
            System.out.println("Task1: " + USER_CONTEXT.get());
        });

        Thread.sleep(100);

        // 第二次提交：父线程切换为用户 B
        USER_CONTEXT.set("UserB");
        pool.submit(() -> {
            // 线程池复用已有线程，不会重新继承，仍然输出 UserA（错误！）
            System.out.println("Task2: " + USER_CONTEXT.get());
        });

        pool.shutdown();
    }
}
```

### withInitial 初始化默认值

```java
// 使用 withInitial 提供默认值，避免 get() 返回 null
private static final ThreadLocal<List<String>> BUFFER =
        ThreadLocal.withInitial(ArrayList::new);

// 等价于重写 initialValue()
private static final ThreadLocal<SimpleDateFormat> DATE_FORMAT =
        new ThreadLocal<>() {
            @Override
            protected SimpleDateFormat initialValue() {
                return new SimpleDateFormat("yyyy-MM-dd");
            }
        };
```

### TransmittableThreadLocal 使用

```java
import com.alibaba.ttl.TransmittableThreadLocal;
import com.alibaba.ttl.TtlRunnable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class TTLDemo {

    private static final TransmittableThreadLocal<String> TRACE_ID =
            new TransmittableThreadLocal<>();

    public static void main(String[] args) {
        ExecutorService pool = Executors.newFixedThreadPool(2);
        TRACE_ID.set("trace-xyz-999");

        Runnable task = TtlRunnable.get(() -> {
            System.out.println("traceId=" + TRACE_ID.get());
        });

        pool.submit(task);
        pool.shutdown();
    }
}
```

## 常见问题

### 1. 线程池中数据污染（未 remove）

线程池的核心线程长期存活，任务执行结束后 ThreadLocalMap 不会自动清理。若下一个任务调用 `get()` 而未先 `set()`，可能读取到上一个任务遗留的数据，造成业务逻辑错误（如用户信息串用）。

**解决**：在任务的 `finally` 块中始终调用 `remove()`。

### 2. InheritableThreadLocal 在线程池中失效

线程池复用已有线程，子线程不会在每次任务提交时重新创建，因此父线程对 `InheritableThreadLocal` 的更新不会传播到池中已有线程。

**解决**：使用 `TransmittableThreadLocal`（com.alibaba:transmittable-thread-local），配合 `TtlRunnable.get(runnable)` 或 `TtlExecutors.getTtlExecutorService(pool)` 包装线程池。

### 3. ThreadLocal 声明为实例变量

若 ThreadLocal 声明为非静态实例字段，每次创建外部对象实例都会产生一个新的 ThreadLocal，导致 ThreadLocalMap 中积累大量 Entry，加速内存压力。

**解决**：始终将 ThreadLocal 声明为 `private static final`。

### 4. 大对象 value 导致内存占用过高

ThreadLocalMap 中 value 的生命周期与线程绑定。若 value 是大对象（如缓存、连接、大 byte 数组），且线程长期存活（如线程池核心线程），即使主动置为 null（`THREAD_LOCAL.set(null)`），Entry 仍然存在，value 引用被 Entry 持有。

**解决**：必须调用 `remove()` 而非 `set(null)`，前者会真正从 ThreadLocalMap 中删除 Entry。

### 5. TTL 包装遗漏导致上下文丢失

TTL 只有在任务提交路径被包装时才生效。如果部分代码直接使用原始 `ExecutorService` 提交任务，这些任务仍然读不到提交线程的上下文。生产中应统一在线程池创建处包装，而不是靠每个调用点手动包装。
