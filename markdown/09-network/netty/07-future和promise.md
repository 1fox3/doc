# Future和Promise

> 专题：Netty
> 来源：Netty.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## Future和Promise

### Future

#### java.util.concurrent.Future

- get

#### Netty扩展了java的Future

- isSuccess

- isCancellable

- cause

- addListener

- addListeners

- removeListener

- removeListeners

- sync

- syncUninterruptibly

- await

- awaitUninterruptibly

- getNow

- cancel

#### ChannelFuture又扩展了Netty的Future

- channel

- addListener

- addListeners

- removeListener

- removeListeners

- sync

- syncUniterruptibly

- await

- awaitUninterruptibly

- isVoid

### Pormise

#### java原生Promise

- setSuccess

- trySuccess

- setFailure

- tryFailure

- setUncancellable

- addListener

- addListeners

- removeListener

- removeListeners

- await

- awaitUninterruptibly

- sync

- syncUninterruptibly

#### ChannelPromise扩展了Promise和ChannelFuture，绑定了Channel

- channel

- setSuccess

- trySuccess

- setFailure

- addListener

- addListeners

- removeListener

- removeListeners

- await

- awaitUninterruptibly

- sync

- syncUninterruptibly

- unvoid
