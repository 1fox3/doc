# Bootstrap

> 专题：Netty
> 来源：Netty.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 是什么

- `Bootstrap` 是 `Netty` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `Bootstrap` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `Bootstrap`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `Bootstrap` 展开，属于 `Netty` 的复习范围。
- 建议优先掌握：Channel, NioSokcetChannel初始化, Unsafe属性初始化。
- 二级节点提示了主要拆分角度：相当于一个Socket的抽象，它为用户提供了关于Socket状态以及对Socket的读写操作。, 类别, 是Netty提供的一个便利的工厂类，可以通过它来完成客户端和服务端的Netty初始化, 调用NioSocketChannel.newSocket(DEFAULT_SELECOTR_PROVIDER)打开一个新的JavaNiOSokcetChannel, 初始化AbstractChannel(Channel parent)对象，并给属性赋值, AbstractNIOChannel中被赋值的属性如下, NioSocketChannel中被赋值的属性, Unsafe其实是对java底层Socket操作的封装, 提供的方法。
- 三级节点通常对应具体细节、API、机制或易错点：NioSocketChannel, NioServerSocketChannel, NioDatagramChannel, NioSctpChannel, NioSctpServerChannel, OioSocketChannel, OioServerSocketChannel, OioDatagramChannel, OioSctpChannel, OioSctpServerChannel。

### 复习追问

- `Channel` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `NioSokcetChannel初始化` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `Unsafe属性初始化` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## Bootstrap

### Channel

#### 相当于一个Socket的抽象，它为用户提供了关于Socket状态以及对Socket的读写操作。

#### 类别

- NioSocketChannel

- NioServerSocketChannel

- NioDatagramChannel

- NioSctpChannel

- NioSctpServerChannel

- OioSocketChannel

- OioServerSocketChannel

- OioDatagramChannel

- OioSctpChannel

- OioSctpServerChannel

### Bootstrap

#### 是Netty提供的一个便利的工厂类，可以通过它来完成客户端和服务端的Netty初始化

### NioSokcetChannel初始化

#### 调用NioSocketChannel.newSocket(DEFAULT_SELECOTR_PROVIDER)打开一个新的JavaNiOSokcetChannel

#### 初始化AbstractChannel(Channel parent)对象，并给属性赋值

- id
  - 每个channel都会被分配一个唯一的id

- parent
  - 默认为null

- unsafe
  - 通过调用newUnsafe()方法实例化一个Unsafe对象，它的类型时AbstractNioByteCahnnel.NioByteUnsafe内部类

- pipeline
  - 通过调用new DefaultChannelPipline(this)创建的实例

#### AbstractNIOChannel中被赋值的属性如下

- ch
  - 被复制为java原生的SocketChannel，即JavaNIOSocketChannel

- readInterestOp
  - 被赋值为SelectionKey.OP_READ

- ch
  - 被配置为非阻塞，即调用ch.configureBlocking(false)方法

#### NioSocketChannel中被赋值的属性

- config = new NioSocketChannelConfig(this, socket.sockey())

### Unsafe属性初始化

#### Unsafe其实是对java底层Socket操作的封装

#### 提供的方法

- register

- bind

- connect

- disconnect

- close

- closeForcibly

- deregister

- beginRead

- write

- flush

### ChannelPipline初始化

#### 维护了一个以AbstractChannelHandlerContext为元素节点的双向连表

#### head

- ChannelOutboundHandler

#### tail

- ChannelInboundHandler

### EventLoopGroup初始化

#### EvemtLoopGroup内部维护了一个类型为EventExecutor的child数组，其大小时nThreads，这样构成了一个线程池

#### 在实例化NioEventLoopGroup时，如果指定线程池大小，则nThreads就是指定的值，反之时CPU核数*2

#### 在MultiThreadEventExecutorGroup中调用newChild()方法来初始化children数组

#### newChild()方法时在NioEventLoopGroup中实现的，它返回一个NioEventLoo实例

#### 初始化NioEventLoop对象时，属性赋值如下

- provider
  - 就是在NioEventLoopGroup构造其中，调用SelectorProvider.provider()方法获取的SelectorProvider对象

- selector
  - 就是在NioEventLoop构造器中，调用provider.openSelector()方法获取Selector对象

### Channel注册到Selector

#### AbstractNioChannel的doRegister()方法，通过javaChannel().register(eventloop().selector, 0, this)将Channel对应的Java NIO的SocketChannel注册到一个eventLoop的Selector中

### boosGroup

#### 只用于服务端的accept。也就是用于处理客户端的新连接接入请求

### workerGroup

#### 负责客户端连接通道的I/O操作

### 处理JDK空轮询Bug

#### 判断空轮询依据

- 极端时间内，轮询了512次(io.netty.selectorAutoRebuildThreshold)

#### 处理方式

- 创建一个新的Selector

- 将原来的Selector中注册的事件全部取消

- 将可用事件重新注册到新的Selector，并激活
