# 网络编程

本目录当前以 Netty 为主线，聚焦 Java 高性能网络编程、NIO/Reactor、事件驱动、编解码、内存管理和生产排障。已删除脑图来源、复习话术、模板占位和非技术内容。

## 目录

- [Netty](01-netty/README.md)：I/O 模型、EventLoop、Channel、Pipeline、ByteBuf、编解码、内存池、零拷贝、背压和排障。
- [Netty 面试重点](01-netty/06-面试重点.md)：I/O 模型、Reactor、Pipeline、ByteBuf 和高性能点。
- [Netty 排障案例](01-netty/07-排障案例.md)：EventLoop 阻塞、直接内存泄漏、粘包半包和写缓冲堆积。

## 学习重点

- 理解阻塞 I/O、非阻塞 I/O、I/O 多路复用、Reactor 和 Proactor 的差异。
- 掌握 Netty 的线程模型，避免在 EventLoop 中执行阻塞逻辑。
- 掌握 ChannelPipeline、Inbound/Outbound Handler、编解码器和事件传播。
- 掌握 ByteBuf 引用计数、池化内存、直接内存和内存泄漏定位。
- 生产排障重点关注连接数、EventLoop 阻塞、写缓冲水位、半包粘包、空轮询、GC 和直接内存。
