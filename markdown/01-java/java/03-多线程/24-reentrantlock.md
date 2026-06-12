# ReentrantLock 详解

## 概述

ReentrantLock 是 `java.util.concurrent.locks` 包中的可重入独占锁，底层基于 AQS（AbstractQueuedSynchronizer）实现。相较于 `synchronized`，它提供了公平锁/非公平锁选择、可中断加锁、超时加锁、以及多个 Condition 条件队列等高级特性。

ReentrantLock 的"可重入"指同一线程可以多次获取同一把锁而不会死锁，每次加锁对应一次解锁，AQS 内部通过 `state` 计数器记录重入次数。使用时必须在 `finally` 块中调用 `unlock()`，否则锁永远不会释放。

## 核心概念

### 可重入实现：AQS state 计数

AQS 用一个 `volatile int state` 字段表示锁状态：
- `state == 0`：锁空闲。
- `state > 0`：锁被持有，值即为重入次数。

线程首次加锁时，`state` 从 0 置为 1，记录持有线程为当前线程。同一线程再次调用 `lock()` 时，检测到持有线程是自己，`state` 自增（例如变为 2）。每次 `unlock()` 使 `state` 自减，减至 0 才真正释放锁并唤醒等待队列中的线程。

```
lock()   → state: 0→1  (持有者 = Thread-A)
lock()   → state: 1→2  (同一线程重入)
unlock() → state: 2→1
unlock() → state: 1→0  (锁释放，唤醒等待线程)
```

### 公平锁 vs 非公平锁

构造时通过参数选择：

```java
ReentrantLock fairLock    = new ReentrantLock(true);   // 公平锁
ReentrantLock nonfairLock = new ReentrantLock(false);  // 非公平锁（默认）
ReentrantLock defaultLock = new ReentrantLock();       // 等同于 false
```

| 维度 | 公平锁（FairSync） | 非公平锁（NonfairSync） |
|---|---|---|
| 加锁策略 | 严格按 CLH 队列顺序 | 新线程先尝试插队 CAS |
| 吞吐量 | 较低 | 较高 |
| 饥饿风险 | 无 | 可能（低概率） |
| 适用场景 | 对公平性有要求 | 一般高并发场景 |

非公平锁在 `lock()` 时会先做一次 CAS 尝试抢锁，失败后才入队，减少了线程切换开销，因此默认选择非公平锁。

### tryLock 超时

`tryLock()` 无参版本立即返回，不进入等待队列；带超时版本等待指定时间后放弃：

```java
// 立即尝试，不等待
if (lock.tryLock()) {
    try { /* 临界区 */ }
    finally { lock.unlock(); }
} else {
    // 获取失败，执行降级逻辑
}

// 最多等待 500ms
if (lock.tryLock(500, TimeUnit.MILLISECONDS)) {
    try { /* 临界区 */ }
    finally { lock.unlock(); }
}
```

`tryLock(time, unit)` 底层调用 AQS 的 `doAcquireNanos()`，使用 `LockSupport.parkNanos()` 挂起线程，超时后自动唤醒并返回 `false`。

### lockInterruptibly 可中断

普通 `lock()` 在等待锁时忽略中断；`lockInterruptibly()` 允许等待期间响应中断：

```java
try {
    lock.lockInterruptibly();
    try {
        // 临界区
    } finally {
        lock.unlock();
    }
} catch (InterruptedException e) {
    // 被中断，执行清理逻辑
    Thread.currentThread().interrupt();
}
```

适用于需要取消等待的场景，例如用户取消操作、系统关机时打断所有等待线程。

### Condition 条件队列

Condition 是 `Object.wait/notify` 的替代方案，可以绑定到同一把锁上创建多个条件队列，精确控制线程等待与唤醒：

```java
Lock lock = new ReentrantLock();
Condition notFull  = lock.newCondition();
Condition notEmpty = lock.newCondition();
```

- `await()`：释放锁，将线程放入 Condition 的等待队列，挂起。
- `signal()`：唤醒条件队列中的一个线程，该线程重新竞争锁。
- `signalAll()`：唤醒条件队列中的所有线程。

与 `Object.wait()` 不同，可以对同一把锁创建多个 Condition，实现生产者等 `notFull`、消费者等 `notEmpty` 的精确通知。

### 必须 finally unlock

ReentrantLock 不像 `synchronized` 由 JVM 保证退出时释放锁。如果临界区抛出异常而没有在 `finally` 中解锁，锁将永久被持有，导致其他线程永久阻塞（死锁）。

标准写法：

```java
lock.lock();
try {
    // 临界区代码
} finally {
    lock.unlock(); // 无论是否异常，必须执行
}
```

## 示例代码

### 基础用法与重入演示

```java
import java.util.concurrent.locks.ReentrantLock;

public class ReentrantLockDemo {
    private final ReentrantLock lock = new ReentrantLock();
    private int count = 0;

    public void outerMethod() {
        lock.lock();
        try {
            System.out.println("外层加锁，state=" + lock.getHoldCount()); // 1
            innerMethod(); // 重入
            count++;
        } finally {
            lock.unlock();
        }
    }

    private void innerMethod() {
        lock.lock(); // 同一线程再次加锁，state 变为 2
        try {
            System.out.println("内层加锁，state=" + lock.getHoldCount()); // 2
        } finally {
            lock.unlock(); // state 变回 1
        }
    }

    public static void main(String[] args) {
        ReentrantLockDemo demo = new ReentrantLockDemo();
        demo.outerMethod();
        System.out.println("释放完毕，isLocked=" + demo.lock.isLocked()); // false
    }
}
```

### 生产者-消费者（Condition 精确通知）

```java
import java.util.ArrayDeque;
import java.util.Queue;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

public class BoundedBuffer<T> {
    private final Queue<T> buffer;
    private final int capacity;
    private final ReentrantLock lock = new ReentrantLock();
    private final Condition notFull  = lock.newCondition();
    private final Condition notEmpty = lock.newCondition();

    public BoundedBuffer(int capacity) {
        this.capacity = capacity;
        this.buffer = new ArrayDeque<>(capacity);
    }

    public void put(T item) throws InterruptedException {
        lock.lock();
        try {
            while (buffer.size() == capacity) {
                notFull.await(); // 队列满，生产者等待
            }
            buffer.offer(item);
            notEmpty.signal(); // 唤醒消费者
        } finally {
            lock.unlock();
        }
    }

    public T take() throws InterruptedException {
        lock.lock();
        try {
            while (buffer.isEmpty()) {
                notEmpty.await(); // 队列空，消费者等待
            }
            T item = buffer.poll();
            notFull.signal(); // 唤醒生产者
            return item;
        } finally {
            lock.unlock();
        }
    }
}
```

### tryLock 防死锁示例

```java
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;

public class TryLockDemo {
    private static final ReentrantLock lockA = new ReentrantLock();
    private static final ReentrantLock lockB = new ReentrantLock();

    public static void transfer(String from, String to) throws InterruptedException {
        while (true) {
            if (lockA.tryLock(100, TimeUnit.MILLISECONDS)) {
                try {
                    if (lockB.tryLock(100, TimeUnit.MILLISECONDS)) {
                        try {
                            System.out.println("转账：" + from + " -> " + to);
                            return;
                        } finally {
                            lockB.unlock();
                        }
                    }
                } finally {
                    lockA.unlock();
                }
            }
            // 两把锁都没拿到或只拿到一把，随机退避后重试
            Thread.sleep((long) (Math.random() * 50));
        }
    }
}
```

## 常见问题

### 忘记在 finally 中 unlock

最常见的错误。临界区如果抛出 `RuntimeException`，若没有 `finally { lock.unlock(); }`，锁永远不会释放，其他线程永远阻塞。即使使用 `tryLock` 成功后也必须遵循此规则。

### Condition.await() 前必须持有锁

调用 `condition.await()` 时，当前线程必须已经持有对应的锁，否则抛出 `IllegalMonitorStateException`。与 `synchronized` 中调用 `object.wait()` 需要在 `synchronized` 块内一样。

### await() 使用 while 而非 if 检查条件

```java
// 错误：if 可能因虚假唤醒（spurious wakeup）导致问题
if (buffer.isEmpty()) {
    notEmpty.await();
}

// 正确：while 循环重新检查条件
while (buffer.isEmpty()) {
    notEmpty.await();
}
```

AQS 实现中虚假唤醒概率极低，但 Java 规范不保证，必须用 `while` 循环。

### 公平锁不等于绝对公平

公平锁保证等待队列中的线程按序获锁，但并不保证业务层面的公平。例如，线程 A 释放锁后，线程 B 被唤醒，在 B 真正运行前，一个刚进来的线程 C 因为公平策略也会排在 B 之后——这里 C 依然需要入队。但如果 B 还未入队，C 可能先于 B 拿到锁（这是非公平锁的行为）。公平锁的开销主要来自于每次加锁都需要检查队列。
