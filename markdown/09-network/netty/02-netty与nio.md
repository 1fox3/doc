# Netty与NIO

> 专题：Netty
> 来源：Netty.xmind

## 补充与实践

- 补充：Netty 的核心约束是 EventLoop 不能阻塞，Pipeline 中 Handler 的线程模型必须明确。
- 实践：自定义协议优先使用长度字段、魔数、版本号、序列化类型和校验字段，便于升级与排障。
- 排障：内存泄漏通过 ResourceLeakDetector、引用计数检查和 ByteBuf 释放路径定位。

## 详细说明

### 是什么

- `Netty与NIO` 是 `Netty` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `Netty与NIO` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `Netty与NIO`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `Netty与NIO` 展开，属于 `Netty` 的复习范围。
- 建议优先掌握：Java NIO三件套, Java NIO工作原理。
- 二级节点提示了主要拆分角度：缓冲区(Buffer), 选择器(Selector), 通道(Channel), 由一个专门的线程来处理所有的I/O事件，并负责分发, 事件驱动机制：事件到的时候触发，而不是同步的去监视事件, 线程通信：线程之间通过wait、notify等方式通信，保证每次上下文切换都是有意义的，减少无谓的线程切换。
- 三级节点通常对应具体细节、API、机制或易错点：类型, 原理, 定义, SelectionKey。

### 复习追问

- `Java NIO三件套` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `Java NIO工作原理` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## Netty与NIO

### Java NIO三件套

#### 缓冲区(Buffer)

- 类型
  - ByteBuffer
  - MappedByteBuffer
    - 内存映射缓冲区
  - LongBuffer
  - DoubleBuffer
  - CharBuffer
  - FloatBuffer
  - IntBuffer
  - ShortBuffer

- 原理
  - 重点属性
    - position
      - 指定下一个将要被写入或者读取的元素索引
    - limit
      - 指定还有多少数据需要取出，或者还有多少空间可以放入数据
    - capacity
      - 制定了可以存储在缓冲区中的最大数据容量，实际上指定了底层数据的大小
  - 0 <= position <= limit <= capacity
  - flip()
    - 把limit设置为当前positon值
    - 把position设置为0
  - get()
    - position增加
  - clear()
    - 所有状态设置为初始化的值
  - wrap(array)
    - 将一个现有数组包装为缓冲区对象
  - slice()
    - 根据position和limit的位置创建子缓冲区，与父缓冲区数据共享
  - asReadOnlyBuffer()
    - 设置缓冲区为只读缓冲区
  - allocateDirect()
    - 直接在内存创建缓冲区而非JVM的堆上

#### 选择器(Selector)

- 定义
  - 是注册各种I/O事件的地方

- SelectionKey
  - 从SelectionKey中可以找到发生的事件和该事件所发生的具体的SelectableChannle，以获得客户端发送过来的数据

- 原理
  - select()
    - 该方法会阻塞，直到至少有一个事件发生

#### 通道(Channel)

- 定义
  - 通道是一个对象，可以通过它读取和写入数据，当然所有数据都是通过Buffer对象来处理

- 类型
  - ServerSocketChannel
  - SocketChannel
  - DatagramChannel
  - FileChannel

### Java NIO工作原理

#### 由一个专门的线程来处理所有的I/O事件，并负责分发

#### 事件驱动机制：事件到的时候触发，而不是同步的去监视事件

#### 线程通信：线程之间通过wait、notify等方式通信，保证每次上下文切换都是有意义的，减少无谓的线程切换
