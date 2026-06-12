# StampedLock

## 概述

`StampedLock` 是 Java 8 引入的一种高性能读写锁，位于 `java.util.concurrent.locks` 包。它不是基于 `AQS` 实现的，而是基于 CLH 队列独立实现，在读多写少的场景下性能显著优于 `ReentrantReadWriteLock`。

核心设计思想是引入"乐观读"模式：读操作不加锁，仅在读取完毕后通过 `validate(stamp)` 验证期间是否有写操作发生。这使得读线程不阻塞写线程，避免了传统读写锁中读锁饥饿写锁的问题。

重要约束：`StampedLock` 不可重入、不支持 `Condition`，且在中断处理上存在已知缺陷，使用时必须了解这些限制。

## 核心概念

### 三种锁模式

**写锁（WriteLock）**

独占模式，与读写互斥。调用 `writeLock()` 返回一个 stamp（戳），释放时必须将该 stamp 传入 `unlockWrite(stamp)`。写锁会阻塞所有读线程（包括乐观读的 validate 校验失败）。

**悲观读锁（ReadLock）**

共享模式，多个悲观读可以同时持有，但不能与写锁共存。行为与 `ReentrantReadWriteLock` 的读锁相似。在有写锁竞争时，性能没有明显优势。

**乐观读（Optimistic Read）**

非锁定模式，通过 `tryOptimisticRead()` 获取一个 stamp，之后读取数据，最后调用 `validate(stamp)` 检查在此期间是否有写锁被获取。

- 如果 `validate` 返回 `true`：读取数据有效，无需升级
- 如果 `validate` 返回 `false`：有写操作介入，必须升级为悲观读锁重新读取

### stamp 戳机制

stamp 是一个 `long` 类型的版本号，每次锁状态变化（加锁、释放）都会更新。

- `0` 表示获取锁失败（`tryWriteLock()` / `tryReadLock()` 返回 0 即失败）
- `tryOptimisticRead()` 返回 0 说明当前有写锁，应直接退化为悲观读
- stamp 必须被妥善保存，解锁时传入错误 stamp 会抛出 `IllegalMonitorStateException`

### 乐观读 validate 校验

validate 的核心逻辑是对比当前 stamp 与 `tryOptimisticRead()` 返回的 stamp 是否一致（内部通过 `state & SBITS` 比较）。validate 是一个 happens-before 边界，使用时需保证：

1. 读取的字段声明为 `volatile`，或在 validate 校验之后再访问局部变量副本
2. 乐观读期间不能有任何锁获取操作
3. validate 失败后，之前读到的数据必须全部丢弃，重新通过悲观读获取

### 锁模式转换

`StampedLock` 提供三个转换方法，避免释放再重新加锁的开销：

| 方法 | 说明 |
|------|------|
| `tryConvertToWriteLock(stamp)` | 尝试将读锁或乐观读升级为写锁 |
| `tryConvertToReadLock(stamp)` | 尝试将写锁降级为读锁 |
| `tryConvertToOptimisticRead(stamp)` | 将写锁或读锁转换为乐观读戳 |

转换失败（返回 0）时，需手动释放原锁后重新获取目标锁。

### 不可重入

`StampedLock` 不支持重入。同一线程在持有写锁的情况下再次调用 `writeLock()` 会直接死锁，同样不支持 `readLock()` 的重入。这是与 `ReentrantReadWriteLock` 最重要的行为差异之一。

### 不支持 Condition

`StampedLock` 没有实现 `Lock` 接口，因此没有 `newCondition()` 方法，无法用于需要条件等待（`await/signal`）的场景。如果需要条件变量配合读写锁，必须使用 `ReentrantReadWriteLock`。

### 中断导致 CPU 飙升（已知缺陷）

`StampedLock` 的 `writeLockInterruptibly()` 和 `readLockInterruptibly()` 存在一个已知问题：当线程在等待锁期间被中断后，线程并不会立即退出等待，而是在自旋中持续消耗 CPU，直到获取到锁才响应中断。

规避方式：
- 优先使用非中断版本 `writeLock()` / `readLock()`
- 或使用 `tryWriteLock(timeout, unit)` 替代中断版本
- JDK 本身在 Java 9+ 仍保留此问题，使用时需评估场景

### vs ReentrantReadWriteLock 性能对比

| 维度 | StampedLock | ReentrantReadWriteLock |
|------|-------------|------------------------|
| 乐观读 | 支持，读不阻塞写 | 不支持 |
| 读写性能（读多写少） | 显著更高 | 一般 |
| 可重入 | 不支持 | 支持 |
| Condition | 不支持 | 支持（写锁） |
| 实现基础 | 独立 CLH | AQS |
| 写锁饥饿 | 有内置防饥饿机制 | 读锁可能饥饿写锁 |
| 中断安全 | 有缺陷 | 正常 |

## 示例代码

### 标准乐观读模式

```java
import java.util.concurrent.locks.StampedLock;

public class Point {
    private double x, y;
    private final StampedLock lock = new StampedLock();

    // 写操作：独占写锁
    public void move(double deltaX, double deltaY) {
        long stamp = lock.writeLock();
        try {
            x += deltaX;
            y += deltaY;
        } finally {
            lock.unlockWrite(stamp);
        }
    }

    // 读操作：乐观读 -> 失败则退化悲观读
    public double distanceFromOrigin() {
        // 1. 尝试乐观读，获取 stamp
        long stamp = lock.tryOptimisticRead();

        // 2. 读取数据到局部变量（此时可能有写操作并发）
        double currentX = x;
        double currentY = y;

        // 3. validate 校验：检查读取期间是否有写锁介入
        if (!lock.validate(stamp)) {
            // 4. 校验失败，升级为悲观读锁
            stamp = lock.readLock();
            try {
                currentX = x;
                currentY = y;
            } finally {
                lock.unlockRead(stamp);
            }
        }

        // 5. 使用局部变量副本计算，此时数据已确保一致
        return Math.sqrt(currentX * currentX + currentY * currentY);
    }
}
```

### 锁升级：读锁转写锁

```java
public void moveIfAtOrigin(double newX, double newY) {
    long stamp = lock.readLock();
    try {
        while (x == 0.0 && y == 0.0) {
            // 尝试将读锁升级为写锁
            long writeStamp = lock.tryConvertToWriteLock(stamp);
            if (writeStamp != 0L) {
                // 升级成功，更新 stamp 并写入
                stamp = writeStamp;
                x = newX;
                y = newY;
                break;
            } else {
                // 升级失败：有其他读线程，先释放读锁再获取写锁
                lock.unlockRead(stamp);
                stamp = lock.writeLock();
            }
        }
    } finally {
        lock.unlock(stamp); // unlock 方法根据 stamp 类型自动选择解锁方式
    }
}
```

### tryOptimisticRead 返回 0 的处理

```java
public String readData() {
    long stamp = lock.tryOptimisticRead();
    // stamp == 0 说明当前有写锁持有，乐观读无意义，直接悲观读
    if (stamp == 0L) {
        stamp = lock.readLock();
        try {
            return doRead();
        } finally {
            lock.unlockRead(stamp);
        }
    }

    String result = doRead();

    if (!lock.validate(stamp)) {
        // 乐观读失败，退化悲观读
        stamp = lock.readLock();
        try {
            return doRead();
        } finally {
            lock.unlockRead(stamp);
        }
    }
    return result;
}
```

## 常见问题

**1. 乐观读后不 validate 直接使用数据**

乐观读不加锁，读取期间写线程可能修改数据。必须在 `validate` 通过后才能信任读到的数据。常见错误是在多字段读取时，部分字段来自写操作前、部分来自写操作后，导致数据状态不一致。

**2. stamp 被丢弃或传错**

解锁时传入错误的 stamp 会抛出 `IllegalMonitorStateException`。常见场景：在锁模式转换后仍用旧 stamp 解锁。正确做法是锁转换后立即更新 stamp 变量，始终在 finally 块中用当前有效 stamp 解锁。

**3. 在持有锁时调用可能阻塞的方法**

由于 `StampedLock` 不可重入，在持有写锁的代码路径中调用任何会尝试获取同一锁的方法（无论是直接还是间接）都会死锁。需要仔细审查调用链。

**4. 中断场景下的 CPU 飙升**

不要在需要响应中断的场景使用 `writeLockInterruptibly()` / `readLockInterruptibly()`。如果确实需要超时或中断，改用 `tryWriteLock(long time, TimeUnit unit)` + 外部轮询逻辑，并在调用方做好超时兜底处理。
