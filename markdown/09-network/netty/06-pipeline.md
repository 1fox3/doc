# Pipeline

> 专题：Netty
> 来源：Netty.xmind

## 补充与实践

- 补充：Netty 的核心约束是 EventLoop 不能阻塞，Pipeline 中 Handler 的线程模型必须明确。
- 实践：自定义协议优先使用长度字段、魔数、版本号、序列化类型和校验字段，便于升级与排障。
- 排障：内存泄漏通过 ResourceLeakDetector、引用计数检查和 ByteBuf 释放路径定位。

## 脑图内容

## Pipeline

### 为Handler生成名字

#### StringUtil.simpleClassName(handlerType) + "#0"

### 事件传播

#### 事件类型

- Inbound事件-读
  - channelRegistered
  - channelUnregistered
  - channelActive
  - channelInactive
  - channelRead
  - channelReadComplete
  - userEventTriggered
  - channelWritabilityChanged
  - exceptionCaught

- Outbound事件-写
  - bind
  - connect
  - close
  - deregister
  - read
  - flush

#### 执行顺序

- Inbound与添加handler顺序一致

- Outbound与添加handler逆序一致

#### 总结

- Outbound事件
  - 是请求事件
  - 发起者时Channel
  - 处理者时Unsafe
  - 事件从Pipeline中的传输方向是从Tail到Head
  - 在ChannelHandler中处理事件时，如果这个Handler不是最后一个Handler，则需要调用ctx的方法(如ctx.connect()方法)将此事件传播下去

- Inbound事件
  - 为通知事件，当某件事情已就绪后，通知上层
  - 发起者时Unsafe
  - 处理者时Channel
  - 事件在Pipeline中的传播方向时从Head到Tail
  - 在ChannelHandler中处理事件时，如果这个Handler不是最后一个Handler，则需要调用ctxfireIN_EVT()方法，将此事件传播下去
