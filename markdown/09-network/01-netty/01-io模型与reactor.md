# I/O 模型与 Reactor

## 阻塞 I/O

阻塞 I/O 中，线程在等待连接、读取数据或写入数据时会阻塞。它实现简单，适合连接数少、并发低的场景，但高并发下需要大量线程，线程切换和内存开销明显。

## 非阻塞 I/O

非阻塞 I/O 中，读写调用立即返回，应用需要轮询判断数据是否准备好。它避免了单次调用阻塞，但如果直接忙轮询，会消耗大量 CPU。

## I/O 多路复用

I/O 多路复用通过 select、poll、epoll 或 kqueue 让一个线程监听多个连接的 I/O 事件。连接就绪后，线程再进行非阻塞读写。Java NIO 的 Selector 属于这一类。

select、poll、epoll 的差异：

- select 使用固定大小 fd 集合，连接数受限制，每次调用需要拷贝和线性扫描。
- poll 使用链表结构，连接数限制较少，但仍需要线性扫描。
- epoll 基于事件通知和就绪队列，适合大量连接场景。

## Reactor 模型

Reactor 模型的核心是事件分发。Reactor 监听 I/O 事件，就绪后分发给对应 Handler 处理。

常见形态：

- 单 Reactor 单线程：一个线程处理连接、读写和业务逻辑，实现简单但容易被阻塞。
- 单 Reactor 多线程：一个 Reactor 处理 I/O，业务逻辑交给线程池。
- 主从 Reactor 多线程：主 Reactor 接收连接，从 Reactor 处理连接读写，业务逻辑可继续交给线程池。

Netty 的 BossGroup 和 WorkerGroup 属于主从 Reactor 思路。

## Proactor 与 AIO

Proactor 模型由操作系统完成异步 I/O，应用收到完成事件。Java AIO 提供 AsynchronousServerSocketChannel、AsynchronousSocketChannel 和 CompletionHandler，但在 Linux 服务端主流高性能网络编程中，NIO 加 epoll 仍更常见。

## Netty 与 Java NIO

Java NIO 提供 Selector、Channel、Buffer 等基础能力，但直接使用成本较高，需要处理半包粘包、Selector 空轮询、连接生命周期、线程模型、内存管理和异常恢复。Netty 在 NIO 之上封装了更完整的事件模型、线程模型、编解码器、内存池和扩展机制。
