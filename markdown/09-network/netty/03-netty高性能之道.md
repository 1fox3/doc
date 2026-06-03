# Netty高性能之道

> 专题：Netty
> 来源：Netty.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## Netty高性能之道

### I/O传输模型

#### 基于Reactor的NIO模型

#### 零拷贝

- Netty接收和发送ByteBuffer采用DirectBuffer，使用堆外直接内存进行Socket读写

- Netty提供了组合Buffer对象，可以聚合多个ByteBuffer对象，用户可以像操作一个Buffer那样方便地对组合Buffer进行操作

- Netty中文传输采用了transferTo()方法，它可以直接将文件缓冲区的数据发送到目标Channel，避免了传统通过循环write()方式导致的内存拷贝问题

#### 内存池

- ByteBuf分类
  - UnpooledUnsafeDirectByteBuf
  - UnpooledHeapByteBuf
    - UnpooledUnsafeHeapByteBuf
  - PooledByteBuf
    - PooledHeapByteBuf
      - PooledUnsafeHeapByteBuf
    - PooledUnsafeDirectByteBuf
    - PooledDirectByteBuf
  - UnpooledDirectByteBuf

- ByteBufAllocator分类
  - PooledByteBufAllocator
  - UnpooledByteBufAllocator

- 缓存分配
  - PoolArena
    - DirectArena
    - HeapArena

### 数据协议

### 线程模型

#### Reactor线程模型

- Reactor单线程模型

- Reactor多线程模型

- 主从Reactor多线程模型

#### 无锁化串行

- ChannelPipeline
