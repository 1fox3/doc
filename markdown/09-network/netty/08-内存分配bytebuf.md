# 内存分配ByteBuf

> 专题：Netty
> 来源：Netty.xmind

## 补充与实践

- 补充：Netty 的核心约束是 EventLoop 不能阻塞，Pipeline 中 Handler 的线程模型必须明确。
- 实践：自定义协议优先使用长度字段、魔数、版本号、序列化类型和校验字段，便于升级与排障。
- 排障：内存泄漏通过 ResourceLeakDetector、引用计数检查和 ByteBuf 释放路径定位。

## 详细说明

### 是什么

- `内存分配ByteBuf` 是 `Netty` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `内存分配ByteBuf` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `内存分配ByteBuf`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `内存分配ByteBuf` 展开，属于 `Netty` 的复习范围。
- 建议优先掌握：重点API, 重点属性, 分类, ByteBufAllocator, 非池化内存分配, 池化内存分配。
- 二级节点提示了主要拆分角度：read, write, set, mark, reset, readerIndex, writerIndex, markedReaderIndex, markedWriterIndex, maxCapacity。
- 三级节点通常对应具体细节、API、机制或易错点：readByte, readUnsignedByte, readShort, readInt, readLong, readableBytes, writeByte, writeableBytes, maxWriteableBytes, setByte。

### 复习追问

- `重点API` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `重点属性` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `分类` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `ByteBufAllocator` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `非池化内存分配` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## 内存分配ByteBuf

### 重点API

#### read

- readByte

- readUnsignedByte

- readShort

- readInt

- readLong

- readableBytes

#### write

- writeByte

- writeableBytes

- maxWriteableBytes

#### set

- setByte

#### mark

- markReaderIndex

- markWriterIndex

#### reset

- resetReaderIndex

- resetWriterIndex

### 重点属性

#### readerIndex

#### writerIndex

#### markedReaderIndex

#### markedWriterIndex

#### maxCapacity

### 分类

#### Pooled

#### Unsafe

#### Direct

### ByteBufAllocator

#### buffer

#### ioBuffer

#### headpBuffer

#### directBuffer

#### compositeBuffer

### 非池化内存分配

#### 堆内内存分配

#### 对外内存分配

### 池化内存分配

#### PooledByteBufAllocator

- tinyCacheSize

- smallCacheSize

- normalCacheSize

#### DirectArena内存分配流程

- 优先从对象池里获得PooledByteBuf进行复用

- 然后在缓存中进行内存分配

- 最后考虑从内存堆里进行内存分配

### 内存规格划分

#### tiny(0~512Byte)

- 0Byte

- 16Byte

- 32Byte

- 48Byte

- 64Byte

- ...

- 496Byte

#### small(512Byte~8KB)

- 512Byte

- 1KB

- 2KB

- 4KB

#### normal(8KB~16MB)

- 8KB

- 16KB

- 32KB

#### huge(16MB以上)

### Page级别内存分配

#### Chunk(16MB)

- 每个Chunk都以双向连表的形式保存在一个ChunkList中

- ChunkList会根据使用率划分
  - qInit
  - q000
  - q025
  - q050
  - q075
  - q100

#### Page(8KB)

#### PoolSubPage

- chunk
  - 页面属于哪个Chunk

- bitmap
  - 用于记录子夜的内存分配情况

- prev
  - 上个子页

- next
  - 下个子页

- elemSize
  - 子页按照多大内存进行划分

#### 记录以分配内存使用的是用数组表示的2叉数

- [0,0,1,1,2,2,2,2...]
