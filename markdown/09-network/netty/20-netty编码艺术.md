# Netty编码艺术

> 专题：Netty
> 来源：面试内容汇总/Netty.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## Netty编码艺术

### TCP拆包、粘包

#### 半包

- 每次从Channel中读取的数据不是一个完整的数据包

#### 粘包

- 读取数据时，读取到超过一个完整数据包的长度

### 拆包基本策略

#### 消息定长，报文长度固定

#### 报尾添加特殊分割符

#### 将消息分为消息头和消息体

#### 更复杂的自定义应用协议

### 常用解码器

#### ByteToMessageDecoder

- LineBasedFrameDecoder

- DelimiterBasedFrameDecoder
  - 分隔符解码器

- FixedLengthFrameDecoder
  - 固定长度解码器

- LengthFieldBasedFrameDecoder
  - 通用解码器
    - lengthFieldOffset
    - lengthFieldLength
    - lengthAdjustment
    - initialBytesToStrip

### 编码器

#### flush()方法才会将数据写入到Channel，write()只是将数据写入缓存，一般会调用writeAndFlush()

#### MessageToByteEncoder

- 发送的消息会组成Entry链表
  - flushedEntry
  - unflushedEntry
  - tailEntry

- ObjectEncoder

- LengthFieldPrepender
