# EventLoop

> 专题：Netty
> 来源：Netty.xmind

## 补充与实践

- 补充：Netty 的核心约束是 EventLoop 不能阻塞，Pipeline 中 Handler 的线程模型必须明确。
- 实践：自定义协议优先使用长度字段、魔数、版本号、序列化类型和校验字段，便于升级与排障。
- 排障：内存泄漏通过 ResourceLeakDetector、引用计数检查和 ByteBuf 释放路径定位。

## 脑图内容

## EventLoop

### 作用

#### 负责执行2个任务

- 作为I/O线程，执行与Channel相关的I/O操作，包括调用Selector等待就绪的I/O事件，读写数据与数据处理等

- 作为任务队列，执行taskQueue中的任务
