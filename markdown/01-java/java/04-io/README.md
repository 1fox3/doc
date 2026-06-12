# Java IO

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind，已按技术主题重新整理。

## 学习主线

- 先区分 `byte` 与 `char`：二进制数据使用字节流，文本数据使用字符流，字符流本质上需要通过 `Charset` 完成编解码。
- 再理解流的组合方式：节点流直接连接数据源，过滤流通过装饰器增强能力，例如缓冲、基本类型读写、对象序列化、打印输出。
- 文件操作优先使用 `java.nio.file.Files` 和 `Path`，传统 `FileInputStream`、`FileWriter` 等 API 更适合理解底层模型或维护旧代码。
- 网络高并发场景关注 `NIO` 的 `Buffer`、`Channel`、`Selector`，它解决的是线程资源和事件通知问题，不是所有场景都比 BIO 更快。

## 章节目录

- [IO 模型与分类](01-io模型与分类.md)
- [字节流与字符流](02-字节流与字符流.md)
- [缓冲流、转换流与打印流](03-缓冲转换打印流.md)
- [文件读写与 Files API](04-文件读写与files.md)
- [序列化](05-序列化.md)
- [NIO 核心机制](06-nio核心机制.md)
- [设计模式与实践检查](07-设计模式与实践检查.md)

## 面试表达

- 定义：Java IO 是 JDK 提供的数据输入输出 API，覆盖内存、文件、网络、管道、对象序列化等数据交换场景。
- 分类：按方向分为输入流和输出流，按单位分为字节流和字符流，按功能分为节点流和过滤流。
- 关键点：字符流必须明确编码；缓冲流减少系统调用或底层写入次数；`flush` 只刷新缓冲区，`close` 会释放资源并通常触发一次刷新。
- 工程取舍：小规模阻塞调用用 BIO 简单稳定，高并发网络 IO 通常使用 NIO/Reactor 框架，文件传输关注缓冲区、零拷贝和背压。

## 常见误区

- `InputStream` 读的是字节，不存在“只支持 ASCII”的说法；字符集处理发生在 `InputStreamReader`、`Reader` 或显式解码逻辑中。
- `Reader` 的 `read()` 每次读取一个字符，但 `Reader` 也支持批量读取 `char[]`；不是只能逐字符读取。
- `PrintWriter` 是字符输出流，继承 `Writer`；`PrintStream` 是字节输出流，继承 `FilterOutputStream`。
- `BufferedReader` 与 `BufferedWriter` 默认缓冲区是 8192 个字符；`BufferedInputStream` 与 `BufferedOutputStream` 默认是 8192 个字节。
- `PrintStream` 和 `PrintWriter` 默认不会因为普通写入就自动刷新；只有开启 `autoFlush` 且调用 `println`、`printf` 或 `format` 等特定方法时才会自动刷新。
