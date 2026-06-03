# Object常见方法

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

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
