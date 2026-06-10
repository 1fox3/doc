# Pipeline

> 专题：Netty
> 来源：Netty.xmind

## 补充与实践

- 补充：Netty 的核心约束是 EventLoop 不能阻塞，Pipeline 中 Handler 的线程模型必须明确。
- 实践：自定义协议优先使用长度字段、魔数、版本号、序列化类型和校验字段，便于升级与排障。
- 排障：内存泄漏通过 ResourceLeakDetector、引用计数检查和 ByteBuf 释放路径定位。

## 详细说明

### 是什么

- `Pipeline` 是 `Netty` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `Pipeline` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `Pipeline`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `Pipeline` 展开，属于 `Netty` 的复习范围。
- 建议优先掌握：为Handler生成名字, 事件传播。
- 二级节点提示了主要拆分角度：StringUtil.simpleClassName(handlerType) + "#0", 事件类型, 执行顺序, 总结。
- 三级节点通常对应具体细节、API、机制或易错点：Inbound事件-读, Outbound事件-写, Inbound与添加handler顺序一致, Outbound与添加handler逆序一致, Outbound事件, Inbound事件。

### 复习追问

- `为Handler生成名字` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `事件传播` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

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
