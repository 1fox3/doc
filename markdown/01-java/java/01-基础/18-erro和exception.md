# Erro和Exception

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：BIO/NIO/AIO 的差异本质是阻塞模型、事件通知机制和线程资源使用方式不同。
- 实践：高并发网络 IO 通常选择 NIO/Reactor 框架，文件传输关注缓冲区、零拷贝和背压。
- 误区：NIO 不必然更快，小规模同步调用中 BIO 可能更简单且足够稳定。

## 脑图内容

## Erro和Exception

### Error

#### OutOfMemoryError

#### NoClassDefFoundError

### Exception

#### 受查异常

- IO相关异常

- ClassNotFoundException

- SQLException

#### 运行时异常(RuntimeException)

- NullPointerException

- IllegalArgumentException

- NumberFormatException

- ClassCastException

### Throwable类常用方法

#### getMessage

- 简要描述

#### toString

- 详细信息

#### getLocalizedMessage

- 异常对象的本地化信息，未被覆盖的情况下等同于getMessage

#### printStackTrace

- 在控制台上答应Throwable封装的异常信息
