# ForkJoin 框架

## 概述

ForkJoin 框架是 JDK 7 引入的并行计算框架，设计目标是高效利用多核 CPU 处理**可递归分解的大任务**。其核心思想与 MapReduce 一致：将大任务拆分（Fork）成若干互相独立的子任务，子任务执行完毕后将结果合并（Join），最终得到完整结果。

框架底层依赖 **work-stealing（工作窃取）算法**，每个工作线程维护一个双端队列（deque）。线程优先从自己队列的**尾部**取任务执行；当本地队列为空时，会从其他线程队列的**头部**"窃取"任务。这种设计减少了线程竞争，使得线程空闲时间极短，CPU 利用率高。

ForkJoin 适合 CPU 密集型、任务可均匀分解、子任务之间无数据依赖的场景。对于 I/O 密集型或任务粒度极细的场景，ForkJoin 的收益有限，甚至带来额外开销。

## 核心概念

### ForkJoinPool

`ForkJoinPool` 是 ForkJoin 框架的线程池实现，负责管理工作线程并调度任务。默认并行度等于 `Runtime.getRuntime().availableProcessors()`（CPU 核数）。

JDK 8 起存在一个全局共享的 **common pool**（`ForkJoinPool.commonPool()`），`parallelStream` 默认使用该池。可通过系统属性调整其并行度：

```
-Djava.util.concurrent.ForkJoinPool.common.parallelism=8
```

`ForkJoinPool` 提供三种提交任务的方式：

| 方法 | 是否阻塞 | 返回值 |
|------|----------|--------|
| `execute(task)` | 否 | void，fire-and-forget |
| `invoke(task)` / `invokeAll(tasks)` | 是，等待完成 | task 的计算结果 |
| `submit(task)` | 否 | `ForkJoinTask<T>`，可后续 `.get()` |

### ForkJoinTask

`ForkJoinTask<V>` 是 ForkJoin 框架中任务的抽象基类，实现了 `Future<V>`。实际使用时继承其两个子类：

- **`RecursiveTask<V>`**：有返回值的递归任务，重写 `compute()` 方法并返回结果。
- **`RecursiveAction`**：无返回值的递归任务，重写 `compute()` 方法执行副作用操作。

任务内部通过 `fork()` 提交子任务到当前工作线程的队列，通过 `join()` 阻塞等待子任务结果。

### work-stealing 算法

每个工作线程持有一个双端队列：

- 线程自身从**队尾**取任务（LIFO，利用局部性）。
- 空闲线程从**其他线程队列的头部**窃取任务（FIFO，减少竞争）。

这种非对称访问方式使得窃取与被窃取线程极少发生 CAS 冲突，整体吞吐量显著优于传统单队列线程池。

### parallelStream 底层原理

`Collection.parallelStream()` 基于 ForkJoin 实现。流操作被封装为 `ForkJoinTask` 提交到 `ForkJoinPool.commonPool()`，框架自动完成数据分割（`Spliterator`）、子任务派发和结果合并。

默认并行度 = CPU 核数 - 1（主线程也会参与计算）。若需要隔离业务使用独立线程池，需显式创建 `ForkJoinPool` 并在其中提交流操作：

```java
ForkJoinPool pool = new ForkJoinPool(4);
pool.submit(() -> list.parallelStream().forEach(...)).get();
```

## 示例代码

使用 `RecursiveTask` 并行求和：

```java
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveTask;

public class ParallelSum extends RecursiveTask<Long> {

    private static final int THRESHOLD = 1000; // 子任务拆分阈值
    private final long[] array;
    private final int start;
    private final int end;

    public ParallelSum(long[] array, int start, int end) {
        this.array = array;
        this.start = start;
        this.end = end;
    }

    @Override
    protected Long compute() {
        int length = end - start;
        if (length <= THRESHOLD) {
            // 任务足够小，直接顺序计算
            long sum = 0;
            for (int i = start; i < end; i++) {
                sum += array[i];
            }
            return sum;
        }

        int mid = start + length / 2;
        ParallelSum leftTask  = new ParallelSum(array, start, mid);
        ParallelSum rightTask = new ParallelSum(array, mid, end);

        leftTask.fork();                    // 异步提交左半部分
        long rightResult = rightTask.compute(); // 当前线程直接执行右半部分
        long leftResult  = leftTask.join(); // 等待左半部分完成

        return leftResult + rightResult;
    }

    public static void main(String[] args) {
        int size = 10_000_000;
        long[] data = new long[size];
        for (int i = 0; i < size; i++) data[i] = i + 1;

        ForkJoinPool pool = new ForkJoinPool();
        long result = pool.invoke(new ParallelSum(data, 0, size));
        System.out.println("Sum = " + result); // 50000005000000
        pool.shutdown();
    }
}
```

使用 `RecursiveAction` 并行归并排序（无返回值）：

```java
import java.util.Arrays;
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveAction;

public class ParallelMergeSort extends RecursiveAction {

    private static final int THRESHOLD = 512;
    private final int[] array;
    private final int start;
    private final int end;

    public ParallelMergeSort(int[] array, int start, int end) {
        this.array = array;
        this.start = start;
        this.end   = end;
    }

    @Override
    protected void compute() {
        if (end - start <= THRESHOLD) {
            Arrays.sort(array, start, end);
            return;
        }
        int mid = (start + end) / 2;
        ParallelMergeSort left  = new ParallelMergeSort(array, start, mid);
        ParallelMergeSort right = new ParallelMergeSort(array, mid, end);
        invokeAll(left, right);    // 并行执行两个子任务并等待完成
        merge(array, start, mid, end);
    }

    private void merge(int[] a, int lo, int mid, int hi) {
        int[] tmp = Arrays.copyOfRange(a, lo, hi);
        int i = 0, j = mid - lo, k = lo;
        while (i < mid - lo && j < hi - lo) {
            a[k++] = (tmp[i] <= tmp[j]) ? tmp[i++] : tmp[j++];
        }
        while (i < mid - lo) a[k++] = tmp[i++];
        while (j < hi - lo)  a[k++] = tmp[j++];
    }

    public static void main(String[] args) {
        int[] data = {5, 3, 8, 1, 9, 2, 7, 4, 6};
        ForkJoinPool pool = new ForkJoinPool();
        pool.invoke(new ParallelMergeSort(data, 0, data.length));
        System.out.println(Arrays.toString(data)); // [1, 2, 3, 4, 5, 6, 7, 8, 9]
    }
}
```

## 常见问题

### 1. 调用栈深度过大导致 StackOverflowError

任务拆分粒度过细、递归层级过深时，每次 `fork()` + `join()` 都会在栈上累积帧，导致 `StackOverflowError`。解决方式：合理设置 `THRESHOLD`，确保任务层级在几十层以内，避免无限制递归。

### 2. 线程堆积导致性能崩溃

ForkJoin 框架中，工作线程阻塞时（如在 `join()` 内部等待子任务）会**补偿性地创建新线程**以维持并行度。若任务拆分过深或子任务中存在阻塞 I/O，补偿线程会持续创建，最终线程数量失控，系统资源耗尽。应避免在 ForkJoin 任务内部做 I/O 或加锁等待。

### 3. parallelStream 中事务与 ThreadLocal 失效

`parallelStream` 运行在 ForkJoinPool 的工作线程上，与提交任务的主线程**不共享事务上下文**（如 Spring 的 `@Transactional` 基于 ThreadLocal 传播事务，子线程中无法获取）。同理，主线程设置的 `ThreadLocal` 变量在工作线程中不可见。需要事务保证时，应在单线程流中操作，或手动传递上下文。

### 4. parallelStream 非线程安全的集合操作

`parallelStream` 的终止操作（如 `forEach`）是并发执行的，若将结果写入非线程安全的集合（如 `ArrayList`），会产生数据竞争。应使用 `collect(Collectors.toList())` 代替手动 `add()`，或使用线程安全容器（`ConcurrentLinkedQueue` 等）。
