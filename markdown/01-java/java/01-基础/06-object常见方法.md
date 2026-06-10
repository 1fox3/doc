# Object常见方法

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### getClass()

- 签名：`public final native Class<?> getClass()`。
- 作用：返回对象运行时的 `Class` 对象，用于获取类元信息。
- 特点：`final` 方法，子类不能重写；返回的是运行时实际类型，不是声明类型。
- 常见场景：反射、日志打印、框架类型判断、注解解析。

### hashCode()

- 签名：`public native int hashCode()`。
- 作用：返回对象的哈希码，主要服务于 `HashMap`、`HashSet`、`Hashtable` 等哈希容器。
- 默认实现通常与对象地址相关，但规范不要求必须等于内存地址。
- 注意：如果重写 `equals`，通常必须同时重写 `hashCode`，保证相等对象哈希值相同。

### equals(Object obj)

- 签名：`public boolean equals(Object obj)`。
- 作用：判断两个对象是否相等。Object 默认实现等价于 `this == obj`，即比较引用是否相同。
- 常见重写场景：值对象、DTO、业务唯一对象等需要按字段或业务主键判断相等。
- 注意：需要满足自反性、对称性、传递性、一致性和非空性。

### clone()

- 签名：`protected native Object clone() throws CloneNotSupportedException`。
- 作用：创建并返回当前对象的一个副本。
- 使用条件：类通常需要实现 `Cloneable` 接口，否则调用 `Object#clone` 会抛出 `CloneNotSupportedException`。
- 注意：默认是浅拷贝，引用字段仍指向原对象中的引用对象；深拷贝需要手动处理。
- 实践建议：业务代码更推荐拷贝构造器、静态工厂或映射工具，少直接依赖 `clone`。

### toString()

- 签名：`public String toString()`。
- 作用：返回对象的字符串表示。Object 默认格式通常是 `类名@哈希值十六进制`。
- 常见重写场景：日志、调试、错误定位、对象摘要展示。
- 注意：不要在 `toString` 中输出密码、token、身份证等敏感信息，也不要触发复杂远程调用或懒加载风暴。

### notify()

- 签名：`public final native void notify()`。
- 作用：随机唤醒一个正在该对象监视器上等待的线程。
- 使用条件：必须在持有该对象监视器时调用，即在 `synchronized(obj)` 或同步方法中调用。
- 注意：被唤醒线程不会立刻执行，需要重新竞争锁。

### notifyAll()

- 签名：`public final native void notifyAll()`。
- 作用：唤醒所有正在该对象监视器上等待的线程。
- 使用条件：同样必须在持有对象监视器时调用。
- 实践建议：条件复杂或多个线程等待不同条件时，`notifyAll` 通常比 `notify` 更安全，但会带来更多线程竞争。

### wait(long timeout)

- 签名：`public final native void wait(long timeout) throws InterruptedException`。
- 作用：让当前线程释放对象锁并进入等待，直到被唤醒、超时或中断。
- 使用条件：必须在持有对象监视器时调用。
- 注意：`timeout` 为 0 表示无限等待。

### wait(long timeout, int nanos)

- 签名：`public final void wait(long timeout, int nanos) throws InterruptedException`。
- 作用：在毫秒基础上增加纳秒级等待参数。
- 注意：实际唤醒精度受操作系统调度影响，不应依赖它实现严格纳秒级定时。

### wait()

- 签名：`public final void wait() throws InterruptedException`。
- 作用：无限期等待，直到其他线程调用同一对象的 `notify/notifyAll` 或当前线程被中断。
- 实践建议：调用 `wait` 应放在 while 条件循环中，防止虚假唤醒。

### finalize()

- 签名：`protected void finalize() throws Throwable`。
- 作用：对象被垃圾回收前可能被 JVM 调用，用于资源清理。
- 现状：`finalize` 已被废弃，不推荐使用，后续版本中会被移除。
- 原因：执行时机不确定、性能差、容易导致对象复活和资源泄漏。
- 替代方案：使用 `try-with-resources`、`AutoCloseable`、显式 `close`、Cleaner 或框架生命周期回调。

### wait/notify 使用示例

```java
public class WaitNotifyDemo {
    private final Object lock = new Object();
    private boolean ready = false;

    public void waitReady() throws InterruptedException {
        synchronized (lock) {
            while (!ready) { // 防止虚假唤醒
                lock.wait();
            }
            System.out.println("ready");
        }
    }

    public void makeReady() {
        synchronized (lock) {
            ready = true;
            lock.notifyAll();
        }
    }
}
```

### 复习检查

- 能用自己的话解释 `Object常见方法`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `Object常见方法` 展开，属于 `Java 语言基础` 的复习范围。
- 建议优先掌握：public final native Class<?> getClass(), public native int hashCode(), public boolean equals(Object obj), protected native Object clone() throws CloneNotSupportedException, public String toString(), public final native void notify(), public final native void notifyAll(), public final native void wait(long timeout) throws InterruptedException。

### 复习追问

- `public final native Class<?> getClass()` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `public native int hashCode()` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `public boolean equals(Object obj)` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `protected native Object clone() throws CloneNotSupportedException` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `public String toString()` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## Object常见方法

### public final native Class<?> getClass()

### public native int hashCode()

### public boolean equals(Object obj)

### protected native Object clone() throws CloneNotSupportedException

### public String toString()

### public final native void notify()

### public final native void notifyAll()

### public final native void wait(long timeout) throws InterruptedException

### public final void wait(long timeout, int nanos) throws InterruptedException

### public final void wait() throws InterruptedException

### protected void finalize() throws Throwable { }
