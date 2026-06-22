# synchronized 原理：monitorenter / monitorexit

## 概述

`synchronized` 是 Java 内置的互斥同步机制，在字节码层面通过 `monitorenter` 和 `monitorexit` 两条指令实现。编译器在进入同步块时插入 `monitorenter`，在退出时插入 `monitorexit`（正常退出和异常退出各一条，保证锁一定被释放）。

每个 Java 对象都关联一个 Monitor（管程），Monitor 内部维护进入次数计数器（重入计数）、持有线程引用和等待队列。线程执行 `monitorenter` 时，若计数器为 0 则获取锁并置为 1；若当前线程已持有该锁则计数器递增（支持重入）；若其他线程持有则当前线程阻塞进入等待队列。`monitorexit` 将计数器减 1，减到 0 时释放锁并唤醒等待线程。

JDK 6 对 `synchronized` 做了大量优化，引入偏向锁和轻量级锁，大幅降低了无竞争场景下的性能开销。

## 核心概念

### Monitor 对象

Monitor 是 HotSpot 中 `ObjectMonitor` 结构体的实现，关键字段如下：

| 字段 | 说明 |
|---|---|
| `_owner` | 持有锁的线程指针 |
| `_count` | 重入计数 |
| `_EntryList` | 竞争失败、阻塞等待的线程队列（BLOCKED 状态） |
| `_WaitSet` | 调用 `wait()` 后挂起的线程集合（WAITING 状态） |
| `_recursions` | 重入层数 |

重量级锁下，线程间切换依赖操作系统的 mutex（互斥量），涉及用户态/内核态切换，开销较高。

### 对象头 MarkWord

HotSpot 中，每个对象的对象头包含两部分：
- **MarkWord**（32/64 bit）：存储锁状态、GC 分代年龄、哈希码等
- **Klass Pointer**：指向类元数据

MarkWord 的低位标志位（`lock bits`）决定当前锁状态：

| 锁状态 | MarkWord 低位标志 | 存储内容 |
|---|---|---|
| 无锁 | `01` | 对象哈希码、GC 年龄 |
| 偏向锁 | `01`（偏向位=1） | 线程 ID、epoch、GC 年龄 |
| 轻量级锁 | `00` | 指向线程栈帧中 Lock Record 的指针 |
| 重量级锁 | `10` | 指向堆中 ObjectMonitor 的指针 |
| GC 标记 | `11` | 空（GC 使用） |

### 锁升级流程：无锁 → 偏向锁 → 轻量级锁 → 重量级锁

锁升级是单向不可降级的（在对象生命周期内）。

**1. 无锁状态**

对象刚创建，MarkWord 存储哈希码和 GC 年龄，低位为 `01`（偏向位为 0）。

**2. 偏向锁**

场景：同步块只被一个线程反复进入，无竞争。

- 第一次获取锁时，通过 CAS 将线程 ID 写入 MarkWord，偏向位置 1。
- 后续同一线程进入同步块时，只检查 MarkWord 中的线程 ID 是否匹配，无需 CAS 操作，几乎零开销。
- 其他线程尝试获取锁时，触发**偏向锁撤销**（revocation），需要等待 Safe Point，将 MarkWord 恢复为无锁或升级为轻量级锁。
- JDK 15 起默认禁用偏向锁（`-XX:-UseBiasedLocking`），JDK 18 彻底废弃。

**3. 轻量级锁**

场景：多线程交替执行同步块，不存在真正的并发竞争。

- 线程进入同步块前，在线程栈帧中创建 **Lock Record**，将 MarkWord 拷贝到 Lock Record（称为 Displaced Mark Word）。
- 通过 CAS 将 MarkWord 替换为指向 Lock Record 的指针，低位置 `00`。
- CAS 成功则获取锁；失败（另一线程已持有）则先**自旋**重试。
- 自旋超过阈值（自适应自旋，JDK 6+ 默认开启）仍失败，膨胀为重量级锁。

**4. 重量级锁**

场景：存在真实并发竞争。

- MarkWord 指向堆中的 ObjectMonitor，低位为 `10`。
- 竞争失败的线程进入 `_EntryList`，操作系统级别挂起（`pthread_mutex_lock`），等待持有者释放锁后唤醒。
- `wait()` / `notify()` / `notifyAll()` 只能在重量级锁（ObjectMonitor）状态下使用，否则抛 `IllegalMonitorStateException`。

### JDK 6 优化：锁粗化与锁消除

**锁消除（Lock Elimination）**

JIT 编译时，逃逸分析（Escape Analysis）发现某个锁对象不会被其他线程访问，则直接消除锁操作。

```java
// 看似有锁，实际 JIT 会消除 StringBuffer 内部的 synchronized
public String buildString() {
    StringBuffer sb = new StringBuffer(); // 局部变量，不逃逸
    sb.append("a");
    sb.append("b");
    sb.append("c");
    return sb.toString();
}
```

**锁粗化（Lock Coarsening）**

JIT 检测到对同一对象的多次连续加锁/解锁，将其合并为一次更大范围的锁，减少重复获取释放的开销。

```java
// 优化前：每次 append 都加锁/解锁
for (int i = 0; i < 1000; i++) {
    synchronizedList.add(i); // 内部有 synchronized
}
// JIT 可能将锁粗化为整个循环外层的一把锁
```

## 示例代码

```java
/**
 * 演示 synchronized 的字节码结构和重入特性
 */
public class SynchronizedDemo {

    private final Object lock = new Object();
    private int count = 0;

    // 同步实例方法：锁是 this 对象
    public synchronized void increment() {
        count++;
        // 字节码：monitorenter（方法标志 ACC_SYNCHRONIZED，隐式）
        // 退出时自动 monitorexit
    }

    // 同步代码块：锁是 lock 对象
    public void incrementWithBlock() {
        synchronized (lock) {
            // 字节码插入 monitorenter
            count++;
            innerMethod(); // 重入：同一线程再次进入 synchronized(lock)
            // 字节码插入 monitorexit（正常路径）
        }
        // 字节码插入 monitorexit（异常路径，在 finally 块中）
    }

    // 演示重入：同一线程可多次获取同一把锁
    private synchronized void innerMethod() {
        // 若调用方已持有 this 锁，_count 递增，不阻塞
        System.out.println("reentrant, count=" + count);
    }

    // 静态同步方法：锁是 SynchronizedDemo.class 对象
    public static synchronized void staticMethod() {
        System.out.println("lock on Class object");
    }

    public static void main(String[] args) throws InterruptedException {
        SynchronizedDemo demo = new SynchronizedDemo();

        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 10000; i++) demo.increment();
        });
        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 10000; i++) demo.increment();
        });

        t1.start();
        t2.start();
        t1.join();
        t2.join();

        System.out.println("Final count: " + demo.count); // 期望 20000
    }
}
```

```java
/**
 * 通过 javap -verbose 观察字节码中的 monitorenter / monitorexit
 *
 * 编译后运行：javap -verbose SynchronizedBytecode.class
 * 可在字节码中看到：
 *   monitorenter
 *   ...
 *   monitorexit   <- 正常出口
 *   ...
 *   monitorexit   <- 异常出口（在 exception table 的 handler 中）
 */
public class SynchronizedBytecode {

    public void syncBlock(Object obj) {
        synchronized (obj) {
            System.out.println("inside sync block");
        }
    }
}
```

```java
/**
 * 演示 wait / notify 必须在持有 Monitor 的情况下调用
 */
public class WaitNotifyDemo {

    private final Object monitor = new Object();
    private boolean ready = false;

    public void producer() throws InterruptedException {
        synchronized (monitor) {       // 必须先持有锁
            ready = true;
            monitor.notifyAll();       // 唤醒在 monitor 上等待的线程
        }
    }

    public void consumer() throws InterruptedException {
        synchronized (monitor) {       // 必须先持有锁
            while (!ready) {
                monitor.wait();        // 释放锁并进入 _WaitSet，被唤醒后重新竞争锁
            }
            System.out.println("consumer: data ready");
        }
    }
}
```

## 常见问题

**1. 锁对象不能为 null**

`synchronized(null)` 会在运行时抛出 `NullPointerException`（在 `monitorenter` 指令执行时检查）。使用字段作为锁对象时，要确保字段在同步块执行前已完成初始化，或声明为 `final`。

**2. 同步方法与同步块的锁对象不同**

`synchronized void foo()` 锁的是 `this`，`synchronized(SomeClass.class)` 锁的是 Class 对象，二者不互斥。混用实例锁和类锁时，线程可能同时进入本应互斥的区域。

**3. wait() 必须放在循环中**

`wait()` 返回后不代表条件已满足（虚假唤醒，spurious wakeup）。正确写法：
```java
synchronized (lock) {
    while (!condition) {   // 用 while，不用 if
        lock.wait();
    }
    // 条件已满足，继续执行
}
```

**4. 锁升级后不会自动降级**

偏向锁一旦被撤销（发生竞争），同一对象不会再次进入偏向锁状态（epoch 机制除外）。在高竞争场景下，偏向锁的撤销开销（需 Safe Point）反而比直接使用轻量级锁更差。JDK 15+ 已默认关闭偏向锁，高并发场景无需手动干预，但旧代码若依赖偏向锁优化需重新评估性能基线。
