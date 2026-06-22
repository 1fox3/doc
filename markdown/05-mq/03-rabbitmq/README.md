# RabbitMQ

RabbitMQ 是基于 AMQP 模型的消息中间件，核心能力是灵活路由、确认机制、队列语义、死信、延迟、优先级和集群高可用。理解 RabbitMQ 应围绕 `Producer -> Exchange -> Binding -> Queue -> Consumer` 这条链路展开。

## 核心特征

- Exchange 负责路由，Queue 负责存储，Binding 描述交换机到队列的绑定关系。
- Channel 是复用在 TCP Connection 上的轻量通信通道。
- Publisher Confirm、mandatory return、consumer ack、持久化和 quorum queue 共同构成可靠投递链路。
- Prefetch/QoS 对消费端公平性、吞吐和内存压力影响很大。
- RabbitMQ 更适合业务消息和复杂路由，不适合作为超大吞吐日志流平台替代 Kafka。

## 文档目录

- [AMQP 基础概念](01-amqp-basic-concepts.md)
- [Exchange、Queue 与 Binding](02-exchange-queue-binding.md)
- [工作模式与路由](03-work-modes-routing.md)
- [生产确认与可靠投递](04-producer-confirm.md)
- [消费确认与 QoS](05-consumer-ack-qos.md)
- [持久化、死信与延迟队列](06-persistence-dead-letter-delay.md)
- [优先级、队列类型与集群](07-queue-types-cluster.md)
- [性能调优与故障排查](08-performance-and-troubleshooting.md)
