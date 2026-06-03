# 内存分配ByteBuf

> 专题：Netty
> 来源：Netty.xmind

## 补充与实践

- 补充：Netty 的核心约束是 EventLoop 不能阻塞，Pipeline 中 Handler 的线程模型必须明确。
- 实践：自定义协议优先使用长度字段、魔数、版本号、序列化类型和校验字段，便于升级与排障。
- 排障：内存泄漏通过 ResourceLeakDetector、引用计数检查和 ByteBuf 释放路径定位。

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
