# Object常见方法

## 方法总览

| 方法签名 | 作用 | 关键注意点 |
|----------|------|------------|
| `public final native Class<?> getClass()` | 返回对象运行时的 `Class` 对象 | `final` 不可重写；返回运行时实际类型，非声明类型 |
| `public native int hashCode()` | 返回对象哈希码 | 重写 `equals` 时必须同时重写，保证相等对象哈希值相同 |
| `public boolean equals(Object obj)` | 判断对象相等，默认等价于 `==` | 需满足自反性、对称性、传递性、一致性、非空性 |
| `protected native Object clone() throws CloneNotSupportedException` | 返回对象副本 | 需实现 `Cloneable`；默认浅拷贝，深拷贝需手动处理 |
| `public String toString()` | 返回字符串表示，默认为 `类名@哈希值十六进制` | 不要输出敏感信息；不要触发懒加载或远程调用 |
| `public final native void notify()` | 随机唤醒一个等待线程 | 必须在持有对象监视器时调用；被唤醒线程需重新竞争锁 |
| `public final native void notifyAll()` | 唤醒所有等待线程 | 多条件等待时比 `notify` 更安全，但竞争更多 |
| `public final void wait() throws InterruptedException` | 无限期等待直到被唤醒或中断 | 必须在持有监视器时调用；应放在 `while` 循环中防止虚假唤醒 |
| `public final native void wait(long timeout) throws InterruptedException` | 等待至多 timeout 毫秒 | `timeout=0` 表示无限等待 |
| `public final void wait(long timeout, int nanos) throws InterruptedException` | 毫秒+纳秒精度等待 | 实际精度受 OS 调度限制，不应依赖纳秒级精度 |
| `protected void finalize() throws Throwable` | GC 前资源清理回调 | 已废弃，执行时机不确定；替代方案：`try-with-resources`、`AutoCloseable`、Cleaner |

## 示例

```java
public class WaitNotifyDemo {
    private final Object lock = new Object();
    private boolean ready = false;

    public void waitReady() throws InterruptedException {
        synchronized (lock) {
            while (!ready) { // while 防止虚假唤醒
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
