# Pipeline 事件传播与编解码

## ChannelPipeline

ChannelPipeline 是 Handler 链，每个 Channel 拥有自己的 Pipeline。Pipeline 中包含 ChannelHandlerContext，Context 连接 Handler、Pipeline 和 Channel，负责事件传播。

## Inbound 与 Outbound

Inbound 事件从网络进入应用，方向通常是 Head 到 Tail。常见事件包括 channelActive、channelRead、channelReadComplete、exceptionCaught、userEventTriggered。

Outbound 事件从应用写回网络，方向通常是 Tail 到 Head。常见事件包括 write、flush、connect、bind、close。

Handler 类型：

- ChannelInboundHandler：处理入站事件。
- ChannelOutboundHandler：处理出站事件。
- ChannelDuplexHandler：同时处理入站和出站事件。

事件传播要点：

- Inbound Handler 中调用 `ctx.fireChannelRead(msg)` 继续向后传播。
- Outbound Handler 中调用 `ctx.write(msg, promise)` 继续向前传播。
- `ctx.write` 从当前 Context 向前找 Outbound Handler，`channel.write` 从 Pipeline 尾部开始传播。

## 粘包与半包

TCP 是字节流协议，不保留应用消息边界。一次 write 不等于一次 read。应用层协议必须自行定义边界。
常见解决方式：

- 固定长度协议：每条消息固定长度，简单但浪费空间。
- 分隔符协议：用特定分隔符标记消息结束，适合文本协议。
- 长度字段协议：消息头包含 body 长度，通用且适合二进制协议。
- TLV 协议：Type、Length、Value，扩展性较好。

## 编解码器

Decoder 将 ByteBuf 转换为业务对象，Encoder 将业务对象转换为 ByteBuf。常用基类包括 ByteToMessageDecoder、MessageToByteEncoder、MessageToMessageDecoder、MessageToMessageEncoder。

编解码原则：

- 解码前检查 readableBytes，数据不完整时不要移动 readerIndex 或使用 mark/reset 恢复。
- 对消息长度设置上限，防止异常大包导致内存打爆。
- 协议头建议包含魔数、版本、序列化类型、压缩类型、消息类型、请求 ID、长度和校验字段。
- 解码异常时关闭连接或丢弃非法数据，避免连接进入不可恢复状态。

## 消息发送

- `write` 只写入出站缓冲区，不一定立即写到 Socket。
- `flush` 将缓冲区数据刷到底层通道。
- `writeAndFlush` 等于 write 后 flush，使用简单但高频小包场景可能增加系统调用。

批量发送时可以多次 write 后统一 flush，减少系统调用和网络包数量。

## 心跳与空闲检测

IdleStateHandler 可检测读空闲、写空闲和读写空闲。常用于心跳、断连检测和连接保活。

心跳设计要点：

- 心跳间隔小于连接超时。
- 连续多次心跳失败再关闭连接，避免网络抖动误杀。
- 心跳包应轻量，避免进入复杂业务处理链路。
