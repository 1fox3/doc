# Netty与NIO

> 专题：Netty
> 来源：Netty.xmind

## 补充与实践

- 补充：Netty 的核心约束是 EventLoop 不能阻塞，Pipeline 中 Handler 的线程模型必须明确。
- 实践：自定义协议优先使用长度字段、魔数、版本号、序列化类型和校验字段，便于升级与排障。
- 排障：内存泄漏通过 ResourceLeakDetector、引用计数检查和 ByteBuf 释放路径定位。

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
