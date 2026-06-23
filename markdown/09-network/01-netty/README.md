# Netty

Netty 是基于事件驱动和 Reactor 模型的高性能网络框架，核心组件包括 EventLoop、Channel、ChannelPipeline、ChannelHandler、ByteBuf、Future 和 Promise。它适合构建 RPC、网关、消息中间件、长连接服务、自定义协议和高并发网络应用。

## 章节

- [01-I/O模型与Reactor](01-io模型与reactor.md)
- [02-启动流程与核心组件](02-启动流程与核心组件.md)
- [03-Pipeline事件传播与编解码](03-pipeline事件传播与编解码.md)
- [04-ByteBuf与内存管理](04-bytebuf与内存管理.md)
- [05-高性能实践与故障排查](05-高性能实践与故障排查.md)
- [06-面试重点](06-面试重点.md)
- [07-排障案例](07-排障案例.md)

## 技术重点

- BossGroup 负责接收连接，WorkerGroup 负责连接上的读写事件。
- 一个 Channel 通常绑定一个 EventLoop，同一 Channel 的事件在同一线程串行执行。
- Pipeline 由 Inbound 和 Outbound Handler 组成，事件沿不同方向传播。
- ByteBuf 使用 readerIndex 和 writerIndex 分离读写位置，并通过引用计数管理生命周期。
- 高性能来自非阻塞 I/O、I/O 多路复用、内存池、直接内存、零拷贝、批量 flush 和减少线程切换。

## 生产原则

- 不要在 EventLoop 中执行阻塞逻辑，耗时业务应切到独立线程池。
- 自定义协议必须明确魔数、版本、序列化类型、消息长度、请求 ID 和校验字段。
- 对入站包大小、写缓冲水位、连接空闲时间、心跳间隔和业务超时设置边界。
- 开启内存泄漏检测或在压测环境验证 ByteBuf 释放路径。
