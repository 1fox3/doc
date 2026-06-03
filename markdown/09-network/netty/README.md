# Netty

> 来源：Netty.xmind, 面试内容汇总/Netty.xmind

## 核心认知

- Netty 是基于事件驱动和 Reactor 模型的高性能网络框架，核心是 EventLoop、Channel、Pipeline 和 ByteBuf。
- 高性能来自非阻塞 IO、线程模型、内存池、零拷贝和减少上下文切换。

## 面试重点

- NIO/Reactor、Boss/Worker、ChannelPipeline、Handler、ByteBuf、粘包拆包。
- 编解码器、心跳、空闲检测、内存泄漏检测、背压和写缓冲水位。

## 实践检查点

- 能实现一个长度字段或分隔符协议，并处理半包/粘包。
- 能排查 Netty 内存泄漏、EventLoop 阻塞和连接数异常。

## 版本与趋势

- Netty 4.1 仍是主流，HTTP/2、QUIC、native transport、内存泄漏检测和背压控制是生产关注点。
- 不要在 EventLoop 中执行阻塞逻辑，业务耗时任务应切到独立线程池。

## 章节目录

### Netty.xmind

- [I/O通信模型](01-i-o通信模型.md)
- [Netty与NIO](02-netty与nio.md)
- [Netty高性能之道](03-netty高性能之道.md)
- [Bootstrap](04-bootstrap.md)
- [EventLoop](05-eventloop.md)
- [Pipeline](06-pipeline.md)
- [Future和Promise](07-future和promise.md)
- [内存分配ByteBuf](08-内存分配bytebuf.md)
- [Netty编码艺术](09-netty编码艺术.md)
- [Netty高性能](10-netty高性能.md)
- [设计模式与Netty](11-设计模式与netty.md)
- [instantiate](12-instantiate.md)
### 面试内容汇总/Netty.xmind

- [消息发送方式](13-消息发送方式.md)
- [超时时间](14-超时时间.md)
- [高性能体现](15-高性能体现.md)
- [I/O通信模型](16-i-o通信模型.md)
- [内存池](17-内存池.md)
- [处理JDK空轮询Bug](18-处理jdk空轮询bug.md)
- [事件传播](19-事件传播.md)
- [Netty编码艺术](20-netty编码艺术.md)
- [instantiate](21-instantiate.md)
