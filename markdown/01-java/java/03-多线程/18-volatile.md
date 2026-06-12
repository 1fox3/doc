# volatile：可见性、有序性与内存屏障

## 概述

`volatile` 是 Java 提供的轻量级同步机制，用于解决多线程环境下的**可见性**和**有序性**问题，但不保证复合操作的原子性。它适合状态标志、配置发布、DCL 单例等场景，不适合保护 `i++`、集合修改等需要互斥的复合操作。

在现代多核 CPU 架构中，每个核心拥有独立的 L1/L2 缓存。线程对共享变量的写入首先发生在 CPU 缓存中，不会立即刷回主内存，其他核心的线程读取的可能是过时数据。`volatile` 通过内存屏障指令强制读写直接操作主内存，并禁止相关指令重排序，从而保证多线程间的内存可见性和操作有序性。

## 核心概念

### JMM 可见性语义

JMM 将内存抽象为主内存和每个线程的工作内存。普通变量的读写可能停留在线程工作内存、CPU 寄存器或缓存中，其他线程可能迟迟看不到最新值。

`volatile` 的语义可以理解为：

- `volatile` 写：把写入前的普通写和本次写一起发布出去，后续读同一变量的线程可见。
- `volatile` 读：强制读取最新值，并保证读之后的普通读写不会被重排到读之前。
- `volatile` 写 happens-before 后续对同一变量的 `volatile` 读。

### 可见性：MESI 协议与缓存一致性

CPU 通过 MESI 协议维护多核缓存一致性，缓存行状态分为：

- **M (Modified)**：当前核心独占且已修改，数据尚未写回主内存
- **E (Exclusive)**：当前核心独占且与主内存一致
- **S (Shared)**：多个核心共享，与主内存一致
- **I (Invalid)**：缓存行已失效，需从主内存重新加载

普通变量写入后，其他核心的缓存行可能仍处于 S 状态读取旧值。`volatile` 写操作触发缓存行失效广播，将其他核心的缓存行标记为 I 状态，强制其他线程下次读取时从主内存加载最新值。

### 有序性：内存屏障禁止重排序

JVM 在 `volatile` 读写前后插入内存屏障（Memory Barrier），规则如下：

| 屏障类型 | 插入位置 | 作用 |
|---|---|---|
| StoreStore | volatile 写之前 | 禁止前面的普通写与 volatile 写重排 |
| StoreLoad | volatile 写之后 | 禁止 volatile 写与后面的读重排（最重量级） |
| LoadLoad | volatile 读之后 | 禁止 volatile 读与后面的普通读重排 |
| LoadStore | volatile 读之后 | 禁止 volatile 读与后面的普通写重排 |

在 x86 架构上，StoreLoad 屏障通常由 `lock addl $0x0, (%rsp)` 或 `mfence` 指令实现，其余屏障在 x86 强内存模型下往往是空操作。

### 发布模式：用 volatile 标志发布普通字段

`volatile` 的 happens-before 可以传递普通字段的可见性，常见写法是先写普通数据，再写 `volatile` 标志：

```java
// 线程 A
result = compute();   // 普通写
ready = true;         // volatile 写

// 线程 B
if (ready) {          // volatile 读
    use(result);      // 一定能看到线程 A 写入的 result
}
```

不要把对象中所有字段都加 `volatile`。如果多个字段是一次性发布的一组数据，通常用一个 `volatile` 状态位承载发布语义更清晰。

### 不保证原子性：i++ 反例

`volatile` 只保证单次读或单次写的可见性，无法保证复合操作（读-改-写）的原子性。

`i++` 在字节码层面拆分为三步：
1. `getfield` — 读取 i 的当前值到操作数栈
2. `iadd` — 执行加 1
3. `putfield` — 将结果写回 i

两个线程同时读到相同的旧值，各自加 1 后写回，最终结果只增加了 1 而不是 2，这是典型的**写后覆盖**问题。解决方案是使用 `AtomicInteger` 或 `synchronized`。

### 双重检查锁（DCL）单例

DCL 是 `volatile` 最经典的应用场景，用于在保证懒加载的同时避免不必要的同步开销。

**为什么必须加 volatile？**

对象创建 `new Singleton()` 在字节码层面分三步：
1. `new` — 在堆上分配内存，字段初始化为零值
2. `invokespecial` — 调用构造方法，初始化字段
3. `astore` — 将引用赋值给变量

JIT 编译器可能将步骤 2 和 3 重排为先赋值引用再执行构造方法（步骤 1→3→2）。若此时另一个线程通过第一次 `if (instance == null)` 检查，会拿到一个引用非 null 但对象尚未完全初始化的实例，导致使用到半构造对象。

`volatile` 的 StoreStore 屏障保证构造方法执行完成（步骤 2）之后，引用赋值（步骤 3）才对其他线程可见，从而杜绝这一问题。

### vs synchronized 区别

| 特性 | volatile | synchronized |
|---|---|---|
| 可见性 | 保证 | 保证（unlock 前刷回主内存） |
| 有序性 | 保证（内存屏障） | 保证（临界区内禁止逃逸重排） |
| 原子性 | 不保证（单次读写除外） | 保证（临界区整体互斥） |
| 互斥/阻塞 | 不阻塞线程 | 阻塞竞争线程（monitorenter/monitorexit） |
| 修饰范围 | 只能修饰成员变量 | 可修饰方法、代码块 |
| 性能 | 轻量（无锁竞争） | 重量（存在线程挂起/唤醒开销） |
| 适用场景 | 状态标志、一写多读 | 复合操作、需要互斥的临界区 |

### 伪共享与性能开销

CPU 以缓存行（通常 64 字节）为单位维护一致性。如果两个高频写入的变量落在同一缓存行，其中一个变量的写入会导致其他核心上的整条缓存行失效，即使另一个线程写的是不同变量，也会被拖慢。这称为伪共享。

`volatile` 热点字段尤其容易放大伪共享，因为它本身会触发缓存行失效广播。Java 8+ 可以使用 `@Contended`（需要 `-XX:-RestrictContended`），或通过字段填充降低冲突。高频计数场景应优先考虑 `LongAdder`，不要用 `volatile long` 做并发计数器。

## 示例代码

```java
// 示例 1：状态标志（正确用法）
public class Worker implements Runnable {
    // 没有 volatile：主线程修改后，工作线程可能永远看不到变化（CPU 缓存中读旧值）
    private volatile boolean running = true;

    @Override
    public void run() {
        while (running) {
            // 执行任务
        }
        System.out.println("Worker stopped.");
    }

    public void stop() {
        running = false; // volatile 写，立即对工作线程可见
    }
}
```

```java
// 示例 2：volatile 不能保证原子性（错误用法）
public class Counter {
    private volatile int count = 0;

    // 线程不安全！volatile 无法保护 i++ 的读-改-写复合操作
    public void increment() {
        count++; // 等价于：read count -> add 1 -> write count，三步非原子
    }

    // 正确方案 1：使用 AtomicInteger
    private AtomicInteger atomicCount = new AtomicInteger(0);
    public void safeIncrement() {
        atomicCount.incrementAndGet(); // CAS 保证原子性
    }

    // 正确方案 2：使用 synchronized
    public synchronized void synchronizedIncrement() {
        count++;
    }
}
```

```java
// 示例 3：双重检查锁（DCL）单例 —— volatile 的经典应用
public class Singleton {
    // 必须加 volatile，防止构造方法与引用赋值被 JIT 重排序
    private static volatile Singleton instance;

    private Singleton() {
        // 假设构造方法有耗时初始化
    }

    public static Singleton getInstance() {
        if (instance == null) {                    // 第一次检查：避免不必要的加锁
            synchronized (Singleton.class) {
                if (instance == null) {            // 第二次检查：防止多线程重复创建
                    instance = new Singleton();    // volatile 保证：构造完成后引用才对外可见
                }
            }
        }
        return instance;
    }
}
```

```java
// 示例 4：演示缺少 volatile 时的可见性问题（可在 -server 模式下复现）
public class VisibilityDemo {
    // 去掉 volatile 后，JVM 可能将 flag 提升到寄存器，循环永不退出
    private static volatile boolean flag = false;

    public static void main(String[] args) throws InterruptedException {
        Thread reader = new Thread(() -> {
            int count = 0;
            while (!flag) {  // 无 volatile 时，可能读到缓存中的 false
                count++;
            }
            System.out.println("Saw flag=true, count=" + count);
        });

        reader.start();
        Thread.sleep(100);
        flag = true;  // 主线程写入
        reader.join();
    }
}
```

## 常见问题

### 1. volatile 修饰引用变量，不保护对象内部字段

```java
private volatile User user = new User();
```

`volatile` 只保证 `user` 引用本身的可见性（即引用地址的读写），不保证 `User` 对象内部字段（如 `user.name`）的可见性。对内部字段的并发修改仍需要额外同步。

### 2. long 和 double 的 64 位非原子读写

在 32 位 JVM 上，对 `long`/`double` 的读写可能被拆分为两次 32 位操作，存在读到半个旧值半个新值的撕裂问题。加 `volatile` 可保证 64 位变量读写的原子性。在现代 64 位 JVM 上该问题极少出现，但规范上仍建议对共享的 `long`/`double` 加 `volatile`。

### 3. DCL 模式去掉 volatile 的隐患

去掉 `volatile` 后，JIT 编译器可合法地将 `new Singleton()` 重排为先暴露引用再执行构造方法。在弱内存模型的 CPU（如 ARM、PowerPC）上，另一个线程可能通过第一次 null 检查后，直接拿到半构造的对象并调用其方法，导致 NPE 或数据错误。这是一种极难复现但真实存在的 bug。

### 4. volatile 读比 synchronized 更廉价，但不是免费的

volatile 读在 x86 上几乎无额外开销（L1 缓存命中），但 volatile 写需要触发 StoreLoad 屏障（`lock` 前缀指令），会导致其他核心缓存行失效，在高频写入场景下对性能影响明显。高并发计数器应优先考虑 `LongAdder` 而非 `volatile long`。

### 5. volatile 的 happens-before 依赖同一个变量

`volatile` 写 happens-before 后续对**同一个 volatile 变量**的读。不要用多个互不相关的 `volatile` 变量拼凑互斥语义；如果需要保护一组操作的原子性，仍然要用 `synchronized`、`Lock` 或原子类。
