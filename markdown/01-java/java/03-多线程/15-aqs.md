# AQS（AbstractQueuedSynchronizer）原理与内部结构

## 概述

AQS（AbstractQueuedSynchronizer）是 `java.util.concurrent.locks` 包中的抽象基类，是构建锁和同步器的底层框架。`ReentrantLock`、`Semaphore`、`CountDownLatch`、`ReentrantReadWriteLock` 等并发工具均基于 AQS 实现。

AQS 的核心思想是：用一个 `volatile int state` 字段表示共享资源的同步状态，用一个 CLH 变体双向链表队列管理等待获取资源的线程，通过 CAS 无锁地更新 `state`，并通过 `LockSupport.park/unpark` 实现线程的阻塞与唤醒。

子类只需重写 `tryAcquire`/`tryRelease`（独占模式）或 `tryAcquireShared`/`tryReleaseShared`（共享模式）即可定义自己的同步语义，AQS 负责所有线程排队和状态管理的模板逻辑。

## 核心概念

### volatile int state

`state` 是 AQS 的核心字段，用 `volatile` 修饰保证可见性：

```
private volatile int state;
```

语义由子类定义：
- `ReentrantLock`：`state == 0` 表示未锁定，`state > 0` 表示已锁定（可重入次数）。
- `Semaphore`：`state` 表示剩余许可数量。
- `CountDownLatch`：`state` 表示倒计数初始值，减到 0 时释放所有等待线程。
- `ReentrantReadWriteLock`：高 16 位存读锁计数，低 16 位存写锁计数。

### CLH 变体等待队列

AQS 维护一个基于 CLH 锁的变体双向 FIFO 链表（`Node` 链表），每个节点封装一个等待线程：

```
head <-> Node(thread1) <-> Node(thread2) <-> Node(thread3) -> null (tail)
```

Node 的关键字段：
- `waitStatus`：节点状态。`CANCELLED(1)` 表示已取消；`SIGNAL(-1)` 表示后继节点需要被唤醒；`CONDITION(-2)` 表示在 Condition 队列中等待；`PROPAGATE(-3)` 用于共享模式的传播。
- `prev` / `next`：双向链接。
- `thread`：封装的等待线程。

简化结构如下：

```java
static final class Node {
    static final Node SHARED = new Node();
    static final Node EXCLUSIVE = null;

    static final int CANCELLED =  1;
    static final int SIGNAL    = -1;
    static final int CONDITION = -2;
    static final int PROPAGATE = -3;

    volatile int waitStatus;
    volatile Node prev;
    volatile Node next;
    volatile Thread thread;
    Node nextWaiter;
}
```

与原始 CLH 队列的区别：原始 CLH 是单向链表，节点自旋检查前驱节点状态；AQS 变体为双向链表，线程阻塞（park）而非自旋，唤醒时通过 `unpark` 精确通知后继节点。

### CAS 更新 state

AQS 通过 `Unsafe` 提供的 CAS 原语保证 `state` 更新的原子性，无需加锁：

```java
// AQS 内部实现
protected final boolean compareAndSetState(int expect, int update) {
    return unsafe.compareAndSwapInt(this, stateOffset, expect, update);
}
```

典型流程（以 `ReentrantLock.lock()` 为例）：
1. 调用 `tryAcquire`，CAS 尝试将 `state` 从 0 改为 1。
2. 成功则当前线程持有锁，直接返回。
3. 失败则将当前线程封装为 `Node` 加入队尾（`addWaiter`），然后在 `acquireQueued` 中自旋尝试，仍失败则 `park` 阻塞。

### 独占模式（ReentrantLock）

`acquire` 模板方法流程：

```
acquire(1)
  -> tryAcquire(1)          // 子类实现，尝试 CAS state: 0->1
     成功: 持有锁，返回
     失败: addWaiter(EXCLUSIVE) // 入队
        -> acquireQueued()  // 自旋检查是否为头节点后继，否则 park
  -> 被 unpark 后重新 tryAcquire
```

`release` 模板方法流程：

```
release(1)
  -> tryRelease(1)          // 子类实现，state 减 1，为 0 时返回 true
  -> unparkSuccessor(head)  // 唤醒 head 的后继节点线程
```

可重入实现：`tryAcquire` 判断当前线程是否已是持有者，是则 `state++`；`tryRelease` 将 `state--`，直到 `state == 0` 才真正释放锁。

### 共享模式（Semaphore / CountDownLatch）

`acquireShared` 模板方法流程：

```
acquireShared(1)
  -> tryAcquireShared(1)    // 返回值 >= 0 表示成功
     成功: 检查是否需要传播唤醒（doReleaseShared）
     失败: 入队（SHARED 节点），park 阻塞
```

与独占模式的关键区别：共享模式下，头节点线程成功获取后会调用 `doReleaseShared`，级联唤醒后续共享节点，允许多个线程同时持有资源。

`CountDownLatch.countDown()` 对应 `releaseShared(1)`，当 `state` CAS 减到 0 时，`tryReleaseShared` 返回 `true`，触发 `doReleaseShared` 唤醒所有 `await` 中的线程。

### ConditionObject

`ConditionObject` 是 AQS 对 `Condition` 的实现，内部维护一条独立的条件队列，与 AQS 同步队列不是同一条队列。

- `await()`：当前线程必须已持有锁；调用后释放锁，将节点加入条件队列并 `park`。
- `signal()`：把条件队列头节点转移到 AQS 同步队列，等待重新竞争锁。
- 条件队列使用 `nextWaiter` 单向链接，同步队列使用 `prev` / `next` 双向链接。

这也是 `Condition` 相比 `Object.wait/notify` 更灵活的原因：一个 `Lock` 可以创建多个 `Condition`，分别维护不同等待条件。

### park / unpark

AQS 通过 `LockSupport.park(this)` 阻塞线程，`LockSupport.unpark(thread)` 精确唤醒指定线程，避免了 `Object.wait/notify` 需要 `synchronized` 的限制，且 `unpark` 可以先于 `park` 调用（许可证机制）：

```java
// 阻塞当前线程，blocker 用于线程转储诊断
LockSupport.park(this);

// 唤醒指定线程（即使该线程尚未 park，下次 park 会立即返回）
LockSupport.unpark(thread);
```

`park` 可被中断信号唤醒（但不抛出 `InterruptedException`，只设置中断标志），因此 `acquireQueued` 中会检查中断状态并在最终 `acquire` 返回后补充 `selfInterrupt()`。

## 示例代码

### 基于 AQS 实现不可重入互斥锁

```java
import java.util.concurrent.locks.AbstractQueuedSynchronizer;
import java.util.concurrent.locks.Condition;

public class SimpleMutex {

    // 内部同步器：state=0 未锁，state=1 已锁
    private static final class Sync extends AbstractQueuedSynchronizer {

        @Override
        protected boolean tryAcquire(int acquires) {
            // CAS 将 state 从 0 改为 1，同时记录持有线程
            if (compareAndSetState(0, 1)) {
                setExclusiveOwnerThread(Thread.currentThread());
                return true;
            }
            return false;
        }

        @Override
        protected boolean tryRelease(int releases) {
            if (getState() == 0) throw new IllegalMonitorStateException();
            setExclusiveOwnerThread(null);
            setState(0); // state 写入不需要 CAS，因为此时只有持有者才能调用
            return true;
        }

        @Override
        protected boolean isHeldExclusively() {
            return getState() == 1 && getExclusiveOwnerThread() == Thread.currentThread();
        }

        Condition newCondition() {
            return new ConditionObject();
        }
    }

    private final Sync sync = new Sync();

    public void lock()              { sync.acquire(1); }
    public boolean tryLock()        { return sync.tryAcquire(1); }
    public void unlock()            { sync.release(1); }
    public boolean isLocked()       { return sync.isHeldExclusively(); }
    public Condition newCondition() { return sync.newCondition(); }

    public static void main(String[] args) throws InterruptedException {
        SimpleMutex mutex = new SimpleMutex();
        int[] counter = {0};

        Runnable task = () -> {
            for (int i = 0; i < 1000; i++) {
                mutex.lock();
                try {
                    counter[0]++;
                } finally {
                    mutex.unlock();
                }
            }
        };

        Thread t1 = new Thread(task);
        Thread t2 = new Thread(task);
        t1.start(); t2.start();
        t1.join();  t2.join();

        System.out.println("Expected: 2000, Actual: " + counter[0]); // 2000
    }
}
```

### 基于 AQS 实现共享模式（二元信号量）

```java
import java.util.concurrent.locks.AbstractQueuedSynchronizer;

/**
 * 演示 AQS 共享模式：最多允许 N 个线程同时进入
 */
public class SharedLatch {

    private static final class Sync extends AbstractQueuedSynchronizer {

        Sync(int count) {
            setState(count); // 初始化许可数
        }

        // 返回值 >= 0 表示获取成功
        @Override
        protected int tryAcquireShared(int acquires) {
            for (;;) {
                int current = getState();
                int next = current - acquires;
                if (next < 0) return next; // 许可不足，返回负数，触发排队
                if (compareAndSetState(current, next)) return next;
            }
        }

        @Override
        protected boolean tryReleaseShared(int releases) {
            for (;;) {
                int current = getState();
                int next = current + releases;
                if (compareAndSetState(current, next)) return true;
            }
        }
    }

    private final Sync sync;

    public SharedLatch(int permits) {
        sync = new Sync(permits);
    }

    public void acquire() throws InterruptedException {
        sync.acquireSharedInterruptibly(1);
    }

    public void release() {
        sync.releaseShared(1);
    }

    public static void main(String[] args) {
        SharedLatch latch = new SharedLatch(3); // 最多 3 个线程同时运行

        for (int i = 0; i < 6; i++) {
            int id = i;
            new Thread(() -> {
                try {
                    latch.acquire();
                    System.out.println("Thread-" + id + " acquired, time=" + System.currentTimeMillis());
                    Thread.sleep(1000);
                    latch.release();
                    System.out.println("Thread-" + id + " released");
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }).start();
        }
    }
}
```

### park/unpark 与中断处理演示

```java
import java.util.concurrent.locks.LockSupport;

public class ParkUnparkDemo {

    public static void main(String[] args) throws InterruptedException {
        Thread waiter = new Thread(() -> {
            System.out.println("waiter: about to park");
            LockSupport.park(Thread.currentThread()); // 阻塞
            // park 被唤醒后不抛异常，需手动检查中断
            if (Thread.interrupted()) {
                System.out.println("waiter: was interrupted");
            } else {
                System.out.println("waiter: unparked normally");
            }
        });

        waiter.start();
        Thread.sleep(500);

        // unpark 可以在 park 之前调用，许可证会被储存
        LockSupport.unpark(waiter);
        waiter.join();

        // 演示：unpark 先于 park 调用
        Thread t2 = new Thread(() -> {
            LockSupport.unpark(Thread.currentThread()); // 先存入许可
            System.out.println("t2: unpark called before park");
            LockSupport.park(); // 立即返回，消耗之前存入的许可
            System.out.println("t2: park returned immediately");
        });
        t2.start();
        t2.join();
    }
}
```

## 常见问题

### 1. tryAcquire 自旋导致 CPU 飙高

AQS 的 `acquireQueued` 并非无限自旋——节点入队后最多自旋一次（检查前驱是否为 head），随即 `park` 阻塞。若应用层在循环中手动调用 `tryLock` 而不使用 `lock`（带排队），才会真正自旋消耗 CPU。区分 `tryLock()`（立即返回）和 `lock()`（排队等待）的使用场景。

### 2. Condition.await() 与中断

`ConditionObject.await()` 会将线程移入 Condition 队列并释放锁，被 `signal` 后重新进入 AQS 同步队列竞争锁。若在 `await` 期间线程被中断，`await` 会抛出 `InterruptedException` 并清除中断标志。若需要不响应中断的等待，应使用 `awaitUninterruptibly()`。

### 3. 共享模式下的"惊群"与传播

`CountDownLatch.countDown()` 减到 0 后调用 `doReleaseShared`，会级联唤醒所有 SHARED 节点。`doReleaseShared` 内部通过 CAS 将 head 的 `waitStatus` 从 `SIGNAL` 改为 0 再触发 `unparkSuccessor`，防止多个释放线程重复唤醒同一后继节点（并发 `countDown` 场景）。

### 4. 公平锁与非公平锁的 AQS 实现差异

非公平锁（`ReentrantLock` 默认）：`lock()` 时先 CAS 抢一次，失败再入队，已入队线程也可能被新线程超越，吞吐量高但可能饥饿。

公平锁：`tryAcquire` 中额外检查 `hasQueuedPredecessors()`，若同步队列中已有等待线程则当前线程直接入队，保证严格 FIFO，但上下文切换开销更大。

### 5. 为什么 unparkSuccessor 会从 tail 向前找节点

AQS 入队时先设置 `node.prev = tail`，再 CAS 更新 `tail`，最后设置前驱的 `next`。在 CAS 成功但 `next` 尚未写入的短暂窗口内，从 `head.next` 向后遍历可能看不到新节点；从 `tail` 反向遍历则可以依赖已设置好的 `prev` 链找到有效后继。
