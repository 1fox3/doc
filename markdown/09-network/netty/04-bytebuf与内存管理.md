# ByteBuf 与内存管理

## ByteBuf 基本模型

ByteBuf 是 Netty 的字节缓冲区抽象，相比 Java NIO ByteBuffer 更易用。它使用 readerIndex 和 writerIndex 分离读写位置，不需要频繁 flip。

关键属性：

- readerIndex：下一个读取位置。
- writerIndex：下一个写入位置。
- capacity：当前容量。
- maxCapacity：最大容量。
- readableBytes：可读字节数。
- writableBytes：可写字节数。

## 常用操作

- read：读取并移动 readerIndex，例如 readByte、readInt、readBytes。
- write：写入并移动 writerIndex，例如 writeByte、writeInt、writeBytes。
- get：按索引读取但不移动指针。
- set：按索引写入但不移动指针。
- mark/reset：标记和恢复 readerIndex 或 writerIndex。

解码时如果数据不足，应避免错误推进 readerIndex。常见做法是先判断 readableBytes，或使用 markReaderIndex 和 resetReaderIndex。

## 堆内存与直接内存

- Heap ByteBuf：基于 JVM 堆内存，分配回收受 GC 管理，访问 Java 数组方便。
- Direct ByteBuf：基于堆外直接内存，网络 I/O 时减少一次堆内到堆外复制，适合高性能场景。

直接内存不受 Java 堆大小直接限制，但受 MaxDirectMemorySize 和系统内存限制。泄漏时可能表现为堆内存正常但进程 RSS 持续上涨。

## 池化与非池化

PooledByteBufAllocator 通过内存池复用 ByteBuf，减少频繁分配和释放。Unpooled 每次直接分配，简单但高并发下开销更大。

池化内存通常按 Arena、Chunk、Page、Subpage 管理：

- Arena：分配管理单元，减少多线程竞争。
- Chunk：大块内存，常见为 16MB 级别。
- Page：Chunk 内的页，常见为 8KB。
- Subpage：用于小对象分配。

## 引用计数

ByteBuf 实现 ReferenceCounted，通过 retain 增加引用计数，通过 release 减少引用计数。引用计数归零后内存可回收。

释放原则：

- 入站 ByteBuf 由最后消费它的 Handler 负责释放。
- 如果将 ByteBuf 继续向后传播，不要提前 release。
- 如果缓存或异步使用 ByteBuf，需要 retain，并在使用完成后 release。
- 派生 ByteBuf 如 slice、duplicate 通常共享底层内存，要关注生命周期。

## 零拷贝

Netty 零拷贝主要体现在：

- 使用 DirectByteBuf 减少 JVM 堆和 native 内存之间复制。
- CompositeByteBuf 组合多个 ByteBuf，避免合并复制。
- slice、duplicate 创建视图，避免复制底层数据。
- FileRegion 通过 sendfile 发送文件，减少用户态和内核态拷贝。

## 内存泄漏定位

ResourceLeakDetector 可检测 ByteBuf 泄漏。常用级别包括 SIMPLE、ADVANCED、PARANOID。压测和排障时可提高检测级别，生产环境需权衡性能开销。

常见泄漏原因：

- 自定义 Handler 消费 ByteBuf 后未 release。
- 异步处理 ByteBuf 未 retain 或未 release。
- 异常分支提前返回导致释放路径遗漏。
- 派生 ByteBuf 生命周期和原始 ByteBuf 混淆。
