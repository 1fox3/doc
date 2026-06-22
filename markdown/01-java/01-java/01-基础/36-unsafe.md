# Unsafe

`sun.misc.Unsafe` 是 JDK 内部底层能力类，可直接操作内存、CAS、线程调度等，绕过 Java 部分安全检查。业务代码不应直接使用，是 `AtomicXxx`、`LockSupport`、`ConcurrentHashMap`、Netty 等底层组件的基础。JDK 17+ 路径迁移至 `jdk.internal.misc.Unsafe`。

## 获取实例

构造器私有且有 Caller 检查，普通代码需通过反射获取：

```java
import sun.misc.Unsafe;
import java.lang.reflect.Field;

public class UnsafeHolder {
    public static final Unsafe UNSAFE;
    static {
        try {
            Field f = Unsafe.class.getDeclaredField("theUnsafe");
            f.setAccessible(true);
            UNSAFE = (Unsafe) f.get(null);
        } catch (Exception e) {
            throw new ExceptionInInitializerError(e);
        }
    }
}
```

## 功能一：CAS 原子操作

```java
import sun.misc.Unsafe;
import java.lang.reflect.Field;

public class AtomicCounter {

    private static final Unsafe UNSAFE = UnsafeHolder.UNSAFE;
    private static final long VALUE_OFFSET;

    static {
        try {
            VALUE_OFFSET = UNSAFE.objectFieldOffset(
                    AtomicCounter.class.getDeclaredField("value"));
        } catch (NoSuchFieldException e) {
            throw new ExceptionInInitializerError(e);
        }
    }

    private volatile int value;

    public int get() { return value; }

    public int getAndIncrement() {
        int current;
        do { current = value; }
        while (!UNSAFE.compareAndSwapInt(this, VALUE_OFFSET, current, current + 1));
        return current;
    }

    public boolean compareAndSet(int expect, int update) {
        return UNSAFE.compareAndSwapInt(this, VALUE_OFFSET, expect, update);
    }

    public static void main(String[] args) throws InterruptedException {
        AtomicCounter counter = new AtomicCounter();
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) counter.getAndIncrement();
            });
            threads[i].start();
        }
        for (Thread t : threads) t.join();
        System.out.println("期望: 10000, 实际: " + counter.get()); // 10000
    }
}
```

| 方法 | 说明 |
|------|------|
| `compareAndSwapInt(obj, offset, expected, update)` | int 字段 CAS |
| `compareAndSwapLong(obj, offset, expected, update)` | long 字段 CAS |
| `compareAndSwapObject(obj, offset, expected, update)` | 引用字段 CAS |
| `objectFieldOffset(Field)` | 获取字段相对于对象头的内存偏移量 |

## 功能二：堆外内存操作

```java
public class OffHeapBuffer {

    private static final Unsafe UNSAFE = UnsafeHolder.UNSAFE;

    private long address;
    private final long capacity;

    public OffHeapBuffer(long capacity) {
        this.capacity = capacity;
        this.address = UNSAFE.allocateMemory(capacity);
        UNSAFE.setMemory(address, capacity, (byte) 0); // 清零，避免脏数据
    }

    public void putLong(long index, long value) {
        UNSAFE.putLong(address + index * Long.BYTES, value);
    }

    public long getLong(long index) {
        return UNSAFE.getLong(address + index * Long.BYTES);
    }

    public void free() {
        if (address != 0) {
            UNSAFE.freeMemory(address); // 必须手动释放，否则内存泄漏
            address = 0;
        }
    }

    public static void main(String[] args) {
        OffHeapBuffer buf = new OffHeapBuffer(1024);
        try {
            buf.putLong(0, 42L);
            buf.putLong(1, 100L);
            System.out.println(buf.getLong(0)); // 42
            System.out.println(buf.getLong(1)); // 100
        } finally {
            buf.free();
        }
    }
}
```

| 方法 | 说明 |
|------|------|
| `allocateMemory(bytes)` | 分配堆外内存，返回起始地址 |
| `reallocateMemory(addr, bytes)` | 重新分配（类似 realloc） |
| `freeMemory(addr)` | 释放堆外内存 |
| `setMemory(addr, bytes, value)` | 批量填充字节（清零常用） |
| `copyMemory(src, dst, bytes)` | 内存块拷贝 |
| `putLong/getLong(addr, value)` | 按地址读写基本类型 |

## 功能三：绕过构造器创建对象

```java
public class InstanceCreation {

    static class Config {
        private final String host;
        private final int port;

        public Config(String host, int port) {
            if (host == null || host.isBlank()) throw new IllegalArgumentException("host required");
            this.host = host;
            this.port = port;
        }

        @Override
        public String toString() { return host + ":" + port; }
    }

    public static void main(String[] args) throws Exception {
        Unsafe unsafe = UnsafeHolder.UNSAFE;

        // 绕过构造器，字段均为默认值（null / 0）
        Config config = (Config) unsafe.allocateInstance(Config.class);
        System.out.println(config.host); // null
        System.out.println(config.port); // 0

        // 反序列化场景：手动写入字段值
        long hostOffset = unsafe.objectFieldOffset(Config.class.getDeclaredField("host"));
        long portOffset = unsafe.objectFieldOffset(Config.class.getDeclaredField("port"));

        unsafe.putObject(config, hostOffset, "127.0.0.1");
        unsafe.putInt(config, portOffset, 8080);

        System.out.println(config); // 127.0.0.1:8080
    }
}
```

## 功能四：volatile 字段读写

```java
public class VolatileFieldAccess {

    static class Node {
        Object next; // 声明时非 volatile
    }

    private static final long NEXT_OFFSET;
    private static final Unsafe UNSAFE = UnsafeHolder.UNSAFE;

    static {
        try {
            NEXT_OFFSET = UNSAFE.objectFieldOffset(Node.class.getDeclaredField("next"));
        } catch (NoSuchFieldException e) {
            throw new ExceptionInInitializerError(e);
        }
    }

    // 以 volatile 语义读取 next
    public static Object getNextVolatile(Node node) {
        return UNSAFE.getObjectVolatile(node, NEXT_OFFSET);
    }

    // 以 volatile 语义写入 next（有 StoreLoad 屏障）
    public static void setNextVolatile(Node node, Object value) {
        UNSAFE.putObjectVolatile(node, NEXT_OFFSET, value);
    }

    // 有序写（Store-Store 屏障，比 volatile 写开销低）
    public static void setNextOrdered(Node node, Object value) {
        UNSAFE.putOrderedObject(node, NEXT_OFFSET, value);
    }
}
```

## 功能五：线程调度 park / unpark

```java
public class ParkDemo {

    public static void main(String[] args) throws InterruptedException {
        Unsafe unsafe = UnsafeHolder.UNSAFE;

        Thread worker = new Thread(() -> {
            System.out.println("worker: 开始 park");
            unsafe.park(false, 0L); // 阻塞，直到 unpark 或线程中断
            System.out.println("worker: 被唤醒");
        });

        worker.start();
        Thread.sleep(500);

        System.out.println("main: 发送 unpark");
        unsafe.unpark(worker);
        worker.join();
    }
}
```

`park(isAbsolute, time)` 参数说明：
- `isAbsolute=false, time=0`：无限等待
- `isAbsolute=false, time=N`：相对超时，单位纳秒
- `isAbsolute=true,  time=N`：绝对超时，Unix 毫秒时间戳

## 功能六：内存屏障（Java 9+）

```java
Unsafe unsafe = UnsafeHolder.UNSAFE;

unsafe.loadFence();   // Load-Load + Load-Store，禁止读重排序
unsafe.storeFence();  // Store-Store + Load-Store，禁止写重排序
unsafe.fullFence();   // 完整屏障（等价于 volatile 写后的 StoreLoad）
```

## 功能七：数组操作

```java
public class ArrayAccess {

    private static final Unsafe UNSAFE = UnsafeHolder.UNSAFE;
    private static final int BASE  = UNSAFE.arrayBaseOffset(int[].class);
    private static final int SCALE = UNSAFE.arrayIndexScale(int[].class);

    public static int getVolatile(int[] arr, int index) {
        return UNSAFE.getIntVolatile(arr, (long) BASE + (long) index * SCALE);
    }

    public static void setVolatile(int[] arr, int index, int value) {
        UNSAFE.putIntVolatile(arr, (long) BASE + (long) index * SCALE, value);
    }

    public static boolean casElement(int[] arr, int index, int expect, int update) {
        return UNSAFE.compareAndSwapInt(arr, (long) BASE + (long) index * SCALE, expect, update);
    }

    public static void main(String[] args) {
        int[] arr = new int[]{1, 2, 3};
        System.out.println(getVolatile(arr, 1)); // 2
        casElement(arr, 1, 2, 99);
        System.out.println(getVolatile(arr, 1)); // 99
    }
}
```

## 注意点

- **堆外内存泄漏**：`allocateMemory` 必须对应 `freeMemory`，GC 不会自动回收，建议用 try-finally 或 Cleaner。
- **字段偏移量不可硬编码**：不同 JVM/平台字段布局可能不同，必须运行时通过 `objectFieldOffset` 动态获取。
- **内存越界导致 JVM crash**：堆外内存越界不抛异常，直接触发段错误（SIGSEGV），进程崩溃。
- **`allocateInstance` 陷阱**：所有字段含 `final` 均为默认值，使用前必须手动赋值。
- **ABA 问题**：CAS 只比较值，无法感知中间变化，需配合版本号（`AtomicStampedReference`）。
- **JDK 9+ 模块化限制**：需要 `--add-opens java.base/sun.misc=ALL-UNNAMED`，否则反射报 `InaccessibleObjectException`。

## 生产场景速查

| 场景 | 框架/说明 |
|------|-----------|
| 原子类底层 | `AtomicInteger`、`AtomicReference` 等 CAS 实现 |
| 锁实现 | `AQS` 的 state 字段 CAS |
| 线程挂起 | `LockSupport.park/unpark` |
| 堆外缓冲区 | `DirectByteBuffer`、Netty `PooledByteBuf` |
| 反序列化 | Kryo、Hessian 用 `allocateInstance` 跳过构造器 |
| 高性能队列 | Disruptor 用偏移量 + 内存屏障替代锁 |

## 现代替代方案

| Unsafe 用法 | 推荐替代 | 版本 |
|-------------|----------|------|
| CAS | `VarHandle` | Java 9+ |
| 堆外内存 | `MemorySegment`（Foreign Memory API） | Java 21 GA |
| 内存屏障 | `VarHandle.fullFence/acquireFence/releaseFence` | Java 9+ |
| park/unpark | `LockSupport`（已封装） | 所有版本 |
