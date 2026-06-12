# ReentrantReadWriteLock

## 概述

`ReentrantReadWriteLock` 是 Java `java.util.concurrent.locks` 包中对 `ReadWriteLock` 接口的标准实现。它将锁拆分为读锁（`ReadLock`）和写锁（`WriteLock`）两把互相关联的锁，核心目的是在保证线程安全的前提下，让并发读操作不相互阻塞，从而提升读多写少场景下的吞吐量。

与 `synchronized` 或 `ReentrantLock` 的排他锁模型不同，读写锁允许多个读线程同时持有读锁，但写线程必须独占锁——既不允许其他写线程并发写，也不允许读线程并发读。这三条规则通常简记为：**读读共享、读写互斥、写写互斥**。

## 核心概念

### 实现 ReadWriteLock 接口

`ReadWriteLock` 接口只有两个方法：

```java
public interface ReadWriteLock {
    Lock readLock();
    Lock writeLock();
}
```

`ReentrantReadWriteLock` 实现了该接口，内部维护一个 `int` 状态字段，高 16 位记录读锁的持有计数，低 16 位记录写锁的重入次数，读写锁共享同一个 AQS 同步器。

### 互斥规则

| 操作 | 是否互斥 |
|------|----------|
| 读 + 读 | 不互斥（并发允许） |
| 读 + 写 | 互斥（写线程等待所有读锁释放） |
| 写 + 写 | 互斥（同一时刻只有一个写线程） |
| 写 + 读 | 互斥（写锁持有期间读线程阻塞） |

### 可重入性

读锁和写锁都支持可重入，同一线程可以多次获取读锁或写锁，但必须对应释放相同次数。写锁的重入计数存在低 16 位；读锁的重入计数通过 `ThreadLocal` 单独为每个读线程维护。

### 锁降级（写锁 → 读锁）

锁降级指的是：在**持有写锁期间**，先获取读锁，然后释放写锁，最终仅持有读锁。这是合法且常见的操作，JDK 官方文档明确支持。

```
写锁已持有 → 获取读锁 → 释放写锁 → 继续以读锁持有
```

降级的目的：写完数据后，防止数据被其他线程修改（写锁释放前先拿读锁），同时允许其他读线程并发读取。

**锁升级（读锁 → 写锁）不被支持。** 若线程 A 持有读锁并试图获取写锁，由于写锁需要等待所有读锁释放，而读锁本身被 A 持有，造成自身死锁。`ReentrantReadWriteLock` 不会检测这种情况，线程将永久阻塞。

### 公平模式与非公平模式

构造时可选公平（`fair=true`）或非公平（默认）模式：

- **非公平模式**：吞吐量更高，写线程可能长时间等待（写饥饿风险）。
- **公平模式**：基于 AQS 的 FIFO 队列，按请求顺序授予锁，写饥饿风险低，但整体吞吐较低。

## 示例代码

### 基本读写锁用法

```java
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class CacheStore {
    private final ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();
    private final ReentrantReadWriteLock.ReadLock readLock = rwLock.readLock();
    private final ReentrantReadWriteLock.WriteLock writeLock = rwLock.writeLock();

    private String cache;

    public String read() {
        readLock.lock();
        try {
            // 多线程可以同时执行到这里
            System.out.println(Thread.currentThread().getName() + " 读取: " + cache);
            return cache;
        } finally {
            readLock.unlock(); // finally 块保证锁必定释放
        }
    }

    public void write(String value) {
        writeLock.lock();
        try {
            // 同一时刻只有一个线程可以执行到这里
            System.out.println(Thread.currentThread().getName() + " 写入: " + value);
            cache = value;
        } finally {
            writeLock.unlock();
        }
    }
}
```

### 锁降级示例

```java
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class LockDemotionExample {
    private final ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();
    private volatile boolean dataReady = false;
    private String data;

    public String processData() {
        rwLock.readLock().lock();
        if (!dataReady) {
            // 需要更新数据，先释放读锁，再获取写锁
            rwLock.readLock().unlock();
            rwLock.writeLock().lock();
            try {
                // 双重检查，防止其他线程在等待期间已完成更新
                if (!dataReady) {
                    data = "initialized data";
                    dataReady = true;
                }
                // 锁降级：在持有写锁期间获取读锁
                rwLock.readLock().lock();
            } finally {
                rwLock.writeLock().unlock(); // 释放写锁，此时仍持有读锁
            }
        }
        // 以下代码在读锁保护下执行
        try {
            return data;
        } finally {
            rwLock.readLock().unlock();
        }
    }
}
```

### 并发验证：读读不互斥

```java
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class ReadConcurrencyDemo {
    public static void main(String[] args) throws InterruptedException {
        ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();

        Runnable reader = () -> {
            rwLock.readLock().lock();
            try {
                System.out.println(Thread.currentThread().getName() + " 获取读锁，开始读...");
                Thread.sleep(1000); // 模拟耗时读操作
                System.out.println(Thread.currentThread().getName() + " 读完毕");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                rwLock.readLock().unlock();
            }
        };

        Thread t1 = new Thread(reader, "Reader-1");
        Thread t2 = new Thread(reader, "Reader-2");
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        // 输出：Reader-1 和 Reader-2 几乎同时打印"获取读锁"，证明读锁并发
    }
}
```

## 常见问题

### 1. 忘记在 finally 中释放锁导致死锁

读锁或写锁获取后，若业务代码抛出未捕获异常而没有 `finally` 释放，锁将永久被持有，后续所有线程阻塞。**始终将 `unlock()` 放在 `finally` 块中**，这是使用任何显式锁的基本原则。

### 2. 尝试锁升级导致线程永久阻塞

持有读锁的线程调用 `writeLock().lock()` 会死锁，因为写锁需要等所有读锁释放，而读锁被自己持有。正确做法：先完全释放读锁，再获取写锁（中间需要重新校验状态）。

### 3. 写操作频繁时读写锁反而更慢

`ReentrantReadWriteLock` 内部状态管理比 `ReentrantLock` 更复杂，在写多读少的场景下，额外的 AQS 状态操作带来的开销会超过读并发的收益。基准测试是决策依据，而不是凭直觉选型。

### 4. 非公平模式下写线程饥饿

默认非公平模式下，持续涌入的读线程可能使写线程长时间无法获取写锁（写饥饿）。`ReentrantReadWriteLock` 的非公平实现对此有部分缓解（写线程在队列头部时会阻塞新的读请求），但在极端读压力下仍可能发生。JDK 8 之后可考虑 `StampedLock` 的乐观读模式作为替代方案。
