# RocketMQ

RocketMQ 是面向业务消息场景的分布式消息系统，核心优势是顺序消息、事务消息、延迟消息、重试死信和高可靠投递能力。学习 RocketMQ 应围绕 `NameServer -> Broker -> CommitLog -> ConsumeQueue -> Producer/Consumer` 主线展开。

## 核心特征

- NameServer 负责轻量级路由注册与发现，节点之间不通信。
- Broker 使用 CommitLog 顺序写保存消息主体，通过 ConsumeQueue 构建按 Topic/Queue 的消费索引。
- Producer 支持同步、异步、单向发送和队列选择。
- Consumer 支持集群消费、广播消费、并发消费、顺序消费、Push/Pull/Pop 等模式。
- 高可用能力包括传统主从复制、同步/异步刷盘、同步/异步复制、DLedger 和 RocketMQ 5.x Proxy。

## 文档目录

- [基础概念与架构](01-basic-concepts.md)
- [NameServer](02-nameserver.md)
- [消息发送](03-producer-send.md)
- [消息类型](04-message-types.md)
- [消息存储](05-message-storage.md)
- [消息消费与 Rebalance](06-consumer-rebalance.md)
- [重试、延迟与死信](07-retry-delay-dead-letter.md)
- [顺序消息与事务消息](08-order-and-transaction.md)
- [高可用、安全与可观测性](09-ha-security-observability.md)
- [RocketMQ 5.x 要点](10-rocketmq-5x.md)
