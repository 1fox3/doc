# sleep() 与 wait() 对比

## 概述

`Thread.sleep()` 和 `Object.wait()` 都能让线程暂停执行，但两者的设计目的、底层机制和使用限制截然不同。`sleep()` 是纯粹的时间等待，适用于控制执行节奏；`wait()` 是线程协作机制的核心，用于线程间的条件同步。

混淆这两个方法是并发编程中的常见错误，理解它们的区别能避免死锁、虚假唤醒等并发问题。

## 核心概念

### 所属类

| 方法 | 所属类 | 方法类型 |
|------|--------|---------|
| `sleep(long millis)` | `java.lang.Thread` | 静态方法 |
| `wait()` / `wait(long timeout)` | `java.lang.Object` | 实例方法 |

`wait()` 定义在 `Object` 上，意味着任何 Java 对象都可以作为锁对象（monitor）来协调线程。这是 Java 将线程同步机制内置到对象模型中的设计决策。

### 是否释放锁

这是两者最关键的区别：

- **`sleep()`**：持有的锁不会释放。线程进入休眠期间，其持有的所有 `synchronized` 锁仍然被占用，其他等待该锁的线程无法继续执行。
- **`wait()`**：调用后立即释放当前对象的监视器锁（即 `synchronized` 块/方法使用的锁），允许其他线程进入同步块。线程进入该对象的等待队列（wait set）。

### 使用限制（synchronized 块）

- **`sleep()`**：可以在任意位置调用，不要求在 `synchronized` 块内。
- **`wait()`**：必须在持有对象监视器锁的情况下调用，即必须在 `synchronized(obj)` 块内或 `synchronized` 方法内调用，否则抛出 `IllegalMonitorStateException`。

### 唤醒方式

| 方法 | 唤醒条件 |
|------|---------|
| `sleep(millis)` | 休眠时间到期后自动唤醒；或被 `Thread.interrupt()` 中断（抛出 `InterruptedException`） |
| `wait()` | 必须由其他线程调用同一对象的 `notify()` 或 `notifyAll()` 唤醒；或使用 `wait(timeout)` 超时后自动唤醒；或被 `Thread.interrupt()` 中断 |

`wait()` 被唤醒后，线程不能立即执行，需要重新竞争对象的监视器锁，竞争成功后才能从 `wait()` 返回继续执行。

### 使用场景

- **`sleep()`**：用于固定时间的暂停，如轮询间隔、限速、模拟延迟。不涉及线程间状态通知。
- **`wait()`**：用于线程间的条件等待和通知，典型场景是生产者-消费者模型：消费者等待队列非空，生产者生产后通知消费者。

## 示例代码

`sleep()` 不释放锁的演示：

```java
public class SleepLockDemo {
    private static final Object lock = new Object();

    public static void main(String[] args) {
        Thread sleeper = new Thread(() -> {
            synchronized (lock) {
                System.out.println("sleeper 获得锁，开始 sleep");
                try {
                    Thread.sleep(3000); // 持有锁休眠，其他线程无法获得 lock
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                System.out.println("sleeper 唤醒，释放锁");
            }
        });

        Thread waiter = new Thread(() -> {
            // 等待 sleeper 先拿到锁
            try { Thread.sleep(100); } catch (InterruptedException e) {}
            System.out.println("waiter 尝试获取锁...");
            synchronized (lock) {
                // 只有 sleeper sleep 结束释放锁后，waiter 才能进入
                System.out.println("waiter 获得锁");
            }
        });

        sleeper.start();
        waiter.start();
    }
}
```

`wait()`/`notify()` 生产者-消费者模型：

```java
import java.util.LinkedList;
import java.util.Queue;

public class ProducerConsumerDemo {
    private static final Queue<Integer> queue = new LinkedList<>();
    private static final int MAX_SIZE = 5;
    private static final Object lock = new Object();

    public static void main(String[] args) {
        Thread producer = new Thread(() -> {
            int item = 0;
            while (true) {
                synchronized (lock) {
                    // 必须用 while 而非 if，防止虚假唤醒
                    while (queue.size() == MAX_SIZE) {
                        try {
                            System.out.println("队列满，生产者 wait，释放锁");
                            lock.wait(); // 释放 lock，进入等待队列
                        } catch (InterruptedException e) {
                            Thread.currentThread().interrupt();
                            return;
                        }
                    }
                    queue.offer(item);
                    System.out.println("生产: " + item++);
                    lock.notifyAll(); // 唤醒等待的消费者线程
                }
            }
        });

        Thread consumer = new Thread(() -> {
            while (true) {
                synchronized (lock) {
                    while (queue.isEmpty()) {
                        try {
                            System.out.println("队列空，消费者 wait，释放锁");
                            lock.wait();
                        } catch (InterruptedException e) {
                            Thread.currentThread().interrupt();
                            return;
                        }
                    }
                    int item = queue.poll();
                    System.out.println("消费: " + item);
                    lock.notifyAll(); // 唤醒等待的生产者线程
                }
                try { Thread.sleep(500); } catch (InterruptedException e) {}
            }
        });

        producer.start();
        consumer.start();
    }
}
```

## 常见问题

### 1. 在 synchronized 块外调用 wait() 导致异常

`wait()` 在 `synchronized` 块外调用会抛出 `IllegalMonitorStateException`，运行时才报错，编译器不检查。必须确保调用 `wait()` 的对象与 `synchronized` 括号内的对象是同一个实例。

```java
// 错误示范 —— lock 对象不匹配
synchronized (lockA) {
    lockB.wait(); // 抛出 IllegalMonitorStateException
}
```

### 2. 应使用 while 而非 if 检查等待条件

线程被 `notify()` 唤醒后，不代表条件一定满足（可能存在虚假唤醒，或被 `notifyAll()` 唤醒但条件仍不成立）。必须用 `while` 循环重新检查条件：

```java
// 正确
while (!condition) {
    lock.wait();
}

// 错误 —— 虚假唤醒后会继续执行，导致数据不一致
if (!condition) {
    lock.wait();
}
```

### 3. sleep() 期间持有锁导致其他线程长时间阻塞

如果在 `synchronized` 块内调用 `sleep()`，其他所有等待该锁的线程都会被阻塞，可能引发性能瓶颈甚至类死锁现象。生产环境应避免在持有锁时做长时间等待，考虑改用 `Condition.await()` 或 `BlockingQueue`。

### 4. notify() vs notifyAll() 的选择

`notify()` 只唤醒等待队列中的一个线程（JVM 选择，不保证顺序），若唤醒的线程条件不满足又重新 `wait()`，而真正满足条件的线程没有被唤醒，会导致信号丢失。多数情况下应优先使用 `notifyAll()` 确保所有等待线程重新竞争，牺牲一定性能换取正确性。
