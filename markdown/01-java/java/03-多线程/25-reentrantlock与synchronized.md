# ReentrantLock 与 synchronized 对比

## 概述

`synchronized` 和 `ReentrantLock` 都是 Java 中用于实现互斥同步的可重入锁。两者的核心差异在于实现层次：`synchronized` 是 JVM 内置关键字，由字节码指令 `monitorenter`/`monitorexit` 驱动，JVM 负责锁的获取与释放；`ReentrantLock` 是 JDK 标准库（`java.util.concurrent.locks`）提供的 API，基于 AQS（AbstractQueuedSynchronizer）实现，需要开发者手动管理锁的释放。

两者都保证可见性、有序性和互斥性，都支持可重入（同一线程可多次获取同一把锁而不死锁）。实际选型时，`synchronized` 更简洁安全，`ReentrantLock` 在需要高级特性时才有替换价值。

## 核心概念

### 可重入机制

两者的可重入都通过持有线程标识 + 计数器实现。`synchronized` 的计数器由 JVM 对象头（Mark Word）中的 monitor 记录；`ReentrantLock` 的计数器由 AQS 的 `state` 字段加上 `exclusiveOwnerThread` 记录。每次重入计数加 1，每次退出减 1，归零才真正释放锁。

### 实现层次差异

| 维度 | synchronized | ReentrantLock |
|------|-------------|---------------|
| 实现层次 | JVM 内置，C++ 实现 | JDK API，纯 Java + Unsafe |
| 锁释放 | JVM 自动（异常也释放） | 必须手动 `unlock()`，须放 `finally` |
| 锁升级 | JVM 自动偏向→轻量→重量 | 无 JVM 级别优化 |
| 性能 | 低争用下极快 | 高争用下更可控 |

### ReentrantLock 额外特性

**1. 可中断加锁（lockInterruptibly）**

`lock()` 会无限等待，`lockInterruptibly()` 在等待期间可响应 `Thread.interrupt()`，适合需要超时取消的场景。

**2. 公平锁**

构造时传入 `true` 启用公平锁：`new ReentrantLock(true)`。公平锁按 FIFO 顺序授予锁，避免线程饥饿，但吞吐量低于非公平锁（默认非公平）。非公平锁在唤醒等待线程前允许新线程抢占，减少了线程切换开销。

**3. tryLock 超时**

`tryLock()` 立即返回 boolean，`tryLock(timeout, unit)` 等待指定时间后返回，可用于实现锁超时降级或熔断逻辑，不会死锁挂死。

**4. 多 Condition 队列**

`synchronized` 只有一个等待队列（`Object.wait/notify`），`ReentrantLock` 通过 `lock.newCondition()` 可创建多个独立的 `Condition` 对象，实现精确的线程唤醒（如生产者只唤醒消费者，消费者只唤醒生产者），避免 `notifyAll` 的无效唤醒。

### synchronized 自动释放

`synchronized` 无论正常退出还是抛出异常，JVM 都会在退出同步块时执行 `monitorexit` 释放锁，不会因为忘记解锁而死锁。`ReentrantLock` 一旦 `unlock()` 没放在 `finally` 块中，异常路径会导致锁永久不释放，其他线程永久阻塞。

## 示例代码

```java
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.TimeUnit;

public class LockComparison {

    // --- 1. synchronized 基本用法 ---
    private final Object monitor = new Object();
    private int count = 0;

    public void incrementSync() {
        synchronized (monitor) {
            count++;
        } // JVM 自动释放，异常也不例外
    }

    // --- 2. ReentrantLock 标准用法：unlock 必须在 finally ---
    private final ReentrantLock lock = new ReentrantLock();

    public void incrementLock() {
        lock.lock();
        try {
            count++;
        } finally {
            lock.unlock(); // 缺少此行 -> 其他线程永久阻塞
        }
    }

    // --- 3. tryLock 超时，避免死等 ---
    public boolean tryIncrement() throws InterruptedException {
        if (lock.tryLock(200, TimeUnit.MILLISECONDS)) {
            try {
                count++;
                return true;
            } finally {
                lock.unlock();
            }
        }
        return false; // 超时放弃，不会挂死
    }

    // --- 4. 可中断加锁 ---
    public void interruptibleIncrement() throws InterruptedException {
        lock.lockInterruptibly(); // 等待期间可被 interrupt() 取消
        try {
            count++;
        } finally {
            lock.unlock();
        }
    }

    // --- 5. 多 Condition：有界队列（生产者/消费者精确唤醒）---
    static class BoundedQueue<T> {
        private final Object[] items;
        private int head, tail, size;

        private final ReentrantLock lock = new ReentrantLock();
        private final Condition notFull  = lock.newCondition(); // 生产者等待此条件
        private final Condition notEmpty = lock.newCondition(); // 消费者等待此条件

        BoundedQueue(int capacity) {
            items = new Object[capacity];
        }

        public void put(T item) throws InterruptedException {
            lock.lock();
            try {
                while (size == items.length) {
                    notFull.await(); // 只有生产者在这里等
                }
                items[tail] = item;
                tail = (tail + 1) % items.length;
                size++;
                notEmpty.signal(); // 精确唤醒一个消费者，不影响生产者
            } finally {
                lock.unlock();
            }
        }

        @SuppressWarnings("unchecked")
        public T take() throws InterruptedException {
            lock.lock();
            try {
                while (size == 0) {
                    notEmpty.await(); // 只有消费者在这里等
                }
                T item = (T) items[head];
                head = (head + 1) % items.length;
                size--;
                notFull.signal(); // 精确唤醒一个生产者
                return item;
            } finally {
                lock.unlock();
            }
        }
    }

    // --- 6. 公平锁示例 ---
    private final ReentrantLock fairLock = new ReentrantLock(true); // FIFO 顺序

    public void fairOperation() {
        fairLock.lock();
        try {
            // 保证等待最久的线程先获得锁，牺牲吞吐量换公平性
        } finally {
            fairLock.unlock();
        }
    }
}
```

```java
// 可重入验证：两种锁都支持同一线程重复获取
public class ReentrantDemo {

    // synchronized 可重入
    public synchronized void outer() {
        System.out.println("outer");
        inner(); // 同一线程再次进入同步方法，不死锁
    }

    public synchronized void inner() {
        System.out.println("inner");
    }

    // ReentrantLock 可重入：state 从 1 -> 2 -> 1 -> 0
    private final ReentrantLock lock = new ReentrantLock();

    public void outerLock() {
        lock.lock(); // state = 1
        try {
            innerLock();
        } finally {
            lock.unlock(); // state = 1
        }
    }

    public void innerLock() {
        lock.lock(); // state = 2，同线程直接通过
        try {
            System.out.println("hold count: " + lock.getHoldCount()); // 2
        } finally {
            lock.unlock(); // state = 1
        }
    }
}
```

## 常见问题

**1. 忘记在 finally 中调用 unlock()**

`ReentrantLock` 最常见的错误。只要 `lock()` 调用成功，`unlock()` 就必须在 `finally` 块执行。若 `lock()` 和 `try` 之间抛异常（极少见，但可能），则不应在 `finally` 中解锁，正确写法是 `lock()` 紧贴 `try{` 的前一行。

**2. 公平锁不等于绝对公平**

公平锁保证的是等待队列的 FIFO，但从操作系统调度到 JVM 层面存在延迟，不保证业务层面的严格顺序。同时公平锁会显著降低吞吐量（大量线程切换），只在有明确饥饿问题时才开启。

**3. Condition.await() 必须在持有锁的情况下调用**

与 `Object.wait()` 一样，`condition.await()` 必须在 `lock.lock()` 之后调用，否则抛 `IllegalMonitorStateException`。await 期间锁会自动释放，被 signal 唤醒后重新竞争锁。

**4. synchronized 在 JDK 新版本中性能已大幅提升，盲目替换得不偿失**

JDK 15 前偏向锁默认开启，JDK 15+ 偏向锁已废弃（JEP 374），但轻量级锁、锁粗化、锁消除等优化仍然有效。低并发场景下 `synchronized` 开销极小，过度使用 `ReentrantLock` 只会增加代码复杂度和出错风险。只有在需要可中断、超时、公平锁或多 Condition 时才应选择 `ReentrantLock`。
