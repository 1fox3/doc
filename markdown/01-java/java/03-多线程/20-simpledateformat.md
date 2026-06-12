# SimpleDateFormat 线程安全问题

## 概述

`SimpleDateFormat` 是 Java 中常用的日期格式化类，但它不是线程安全的。在多线程环境下共享同一个 `SimpleDateFormat` 实例，会导致解析或格式化结果出错，甚至抛出异常（如 `NumberFormatException`、`ArrayIndexOutOfBoundsException`）。

问题根源在于 `SimpleDateFormat` 内部持有一个 `Calendar` 字段，格式化和解析操作都会修改这个共享的 `Calendar` 实例。多个线程同时调用时，彼此会覆盖对方对 `Calendar` 的写入，导致数据竞争。

## 核心概念

### 为什么 SimpleDateFormat 不是线程安全的

`SimpleDateFormat` 的父类 `DateFormat` 中定义了 `protected Calendar calendar` 字段。`format()` 方法在执行时会调用 `calendar.setTime(date)` 修改这个字段，`parse()` 方法同样依赖 `calendar` 来存储中间状态。

```java
// DateFormat 源码（简化）
protected Calendar calendar;

public StringBuffer format(Date date, StringBuffer toAppendTo, FieldPosition pos) {
    calendar.setTime(date);  // 写共享字段 —— 非原子操作
    // ... 后续读 calendar 的各个字段
}
```

当线程 A 调用 `setTime()` 后还未读取结果，线程 B 已经覆盖了 `calendar`，线程 A 读到的就是线程 B 的数据。

### 解决方案一：局部变量（每次创建新实例）

最简单的方案：不共享实例，每个方法调用内部创建一个新的 `SimpleDateFormat`。

适用场景：调用频率较低，对象创建开销可接受。

### 解决方案二：synchronized 加锁

将共享实例的访问包裹在同步块中，同一时刻只有一个线程使用该实例。

适用场景：实例创建成本高且并发量不大，可接受锁竞争带来的性能损耗。

### 解决方案三：ThreadLocal 线程隔离

为每个线程保存一个独立的 `SimpleDateFormat` 实例，避免共享。与加锁相比，无竞争开销，性能更好。

注意：在线程池环境下，线程会被复用，`ThreadLocal` 中的值会一直存在。使用完毕后必须调用 `remove()`，否则可能导致内存泄漏，或在复用线程时读到上一个任务遗留的状态。

### 推荐方案：DateTimeFormatter（Java 8+）

`java.time.format.DateTimeFormatter` 是不可变类，天然线程安全，可以声明为静态常量全局共享，无需任何同步措施。配合 `LocalDate`、`LocalDateTime` 等新日期 API 使用，是现代 Java 项目的首选。

## 示例代码

```java
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Date;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class DateFormatDemo {

    // ---- 方案一：局部变量，每次新建实例 ----
    public static String formatWithLocalVar(Date date) {
        // 每次调用都创建新对象，线程安全，但有 GC 压力
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        return sdf.format(date);
    }

    // ---- 方案二：synchronized 加锁 ----
    private static final SimpleDateFormat SHARED_SDF =
            new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

    public static synchronized String formatWithSync(Date date) {
        return SHARED_SDF.format(date);
    }

    // ---- 方案三：ThreadLocal 线程隔离 ----
    private static final ThreadLocal<SimpleDateFormat> THREAD_LOCAL_SDF =
            ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd HH:mm:ss"));

    public static String formatWithThreadLocal(Date date) {
        try {
            return THREAD_LOCAL_SDF.get().format(date);
        } finally {
            // 线程池场景下必须 remove，防止内存泄漏
            THREAD_LOCAL_SDF.remove();
        }
    }

    // ---- 推荐：DateTimeFormatter（Java 8+，不可变，线程安全）----
    private static final DateTimeFormatter FORMATTER =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    public static String formatWithDateTimeFormatter(LocalDateTime dateTime) {
        // 静态常量，无需同步，直接并发调用
        return FORMATTER.format(dateTime);
    }

    // 模拟多线程竞争场景（不安全写法，仅用于演示问题）
    public static void demonstrateUnsafe() throws InterruptedException {
        SimpleDateFormat unsafeSdf = new SimpleDateFormat("yyyy-MM-dd");
        ExecutorService pool = Executors.newFixedThreadPool(10);

        for (int i = 0; i < 100; i++) {
            pool.submit(() -> {
                try {
                    // 多线程共享同一实例 —— 可能抛出异常或返回错误结果
                    String result = unsafeSdf.format(new Date());
                    System.out.println(Thread.currentThread().getName() + ": " + result);
                } catch (Exception e) {
                    System.err.println("解析出错: " + e.getMessage()); // NumberFormatException 等
                }
            });
        }
        pool.shutdown();
    }
}
```

```java
// ThreadLocal 在线程池中的正确用法（不 remove 的后果演示）
public class ThreadLocalLeakDemo {

    private static final ThreadLocal<SimpleDateFormat> SDF_HOLDER =
            ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd"));

    public static void process(Date date) {
        SimpleDateFormat sdf = SDF_HOLDER.get();
        String result = sdf.format(date);
        System.out.println(result);
        // 如果不 remove()，线程池复用该线程时，ThreadLocal 仍持有旧实例
        // 对于 SimpleDateFormat 来说实例本身无状态泄漏，但若持有的是含业务数据的对象
        // 则会导致上下文污染
        SDF_HOLDER.remove(); // 推荐始终 remove
    }
}
```

## 常见问题

### 1. 静态变量声明 SimpleDateFormat 导致数据错乱

最常见的错误：将 `SimpleDateFormat` 声明为类的 `static` 字段，所有线程共享一个实例。在高并发下必然出现结果互相覆盖，错误现象随机，难以复现，排查困难。

```java
// 错误写法
private static final SimpleDateFormat SDF = new SimpleDateFormat("yyyy-MM-dd");

public String format(Date date) {
    return SDF.format(date); // 多线程调用此方法时不安全
}
```

### 2. ThreadLocal 在线程池中忘记 remove 导致内存泄漏

线程池中的线程不会销毁，`ThreadLocal` 中的值会一直保留。若 `ThreadLocal` 持有的对象较大（如包含业务上下文），长期积累会导致内存泄漏。务必在 `finally` 块中调用 `remove()`。

### 3. parse() 比 format() 更容易出问题

`format()` 只读 `calendar`，`parse()` 既写又读，竞争条件更严重。多线程并发调用 `parse()` 时，更容易触发 `NumberFormatException` 或返回完全错误的日期值。

### 4. 从 SimpleDateFormat 迁移到 DateTimeFormatter 的注意点

`DateTimeFormatter` 操作的是 `LocalDate`/`LocalDateTime` 等新类型，而非 `java.util.Date`。迁移时需要同步替换日期类型。若系统中仍有 `java.util.Date`，可通过以下方式转换：

```java
// java.util.Date 转 LocalDateTime
Date legacyDate = new Date();
LocalDateTime ldt = legacyDate.toInstant()
        .atZone(ZoneId.systemDefault())
        .toLocalDateTime();

// LocalDateTime 转 java.util.Date
Date converted = Date.from(ldt.atZone(ZoneId.systemDefault()).toInstant());
```
