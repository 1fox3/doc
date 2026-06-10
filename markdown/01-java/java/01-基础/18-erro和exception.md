# Erro和Exception

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：BIO/NIO/AIO 的差异本质是阻塞模型、事件通知机制和线程资源使用方式不同。
- 实践：高并发网络 IO 通常选择 NIO/Reactor 框架，文件传输关注缓冲区、零拷贝和背压。
- 误区：NIO 不必然更快，小规模同步调用中 BIO 可能更简单且足够稳定。

## 详细说明

### Throwable 体系

- `Throwable` 是 Java 异常体系根类，下面主要分为 `Error` 和 `Exception`。
- `Error` 表示严重错误，通常程序无法恢复，例如 `OutOfMemoryError`、`StackOverflowError`。
- `Exception` 表示程序可以捕获和处理的异常。

### 受检与非受检异常

- 受检异常：继承 `Exception` 但不继承 `RuntimeException`，编译器要求处理或声明抛出。
- 非受检异常：`RuntimeException` 及其子类，通常表示编程错误或运行期异常。
- 业务异常通常可以设计为 RuntimeException，但要有统一异常处理和错误码。

### 实践建议

- 不要捕获 `Throwable` 或 `Error` 后继续正常执行，除非是在框架边界做日志和隔离。
- 不要空 catch，至少记录上下文。
- 对外接口应统一异常响应，避免把内部堆栈直接暴露给调用方。

### 复习检查

- 能用自己的话解释 `Erro和Exception`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `Erro和Exception` 展开，属于 `Java 语言基础` 的复习范围。
- 建议优先掌握：Error, Exception, Throwable类常用方法。
- 二级节点提示了主要拆分角度：OutOfMemoryError, NoClassDefFoundError, 受查异常, 运行时异常(RuntimeException), getMessage, toString, getLocalizedMessage, printStackTrace。
- 三级节点通常对应具体细节、API、机制或易错点：IO相关异常, ClassNotFoundException, SQLException, NullPointerException, IllegalArgumentException, NumberFormatException, ClassCastException, 简要描述, 详细信息, 异常对象的本地化信息，未被覆盖的情况下等同于getMessage。

### 复习追问

- `Error` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `Exception` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `Throwable类常用方法` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

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
