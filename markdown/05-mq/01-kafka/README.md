# Kafka

Kafka 是以分区日志为核心的分布式消息系统。理解 Kafka 时不要先从 API 入手，而要先抓住 `Topic -> Partition -> Log -> Segment -> Offset -> Replica` 这条主线。

## 核心特征

- 高吞吐来自顺序写、页缓存、批量发送、压缩、零拷贝和分区并行。
- 顺序性只在单分区内成立，跨分区没有全局顺序保证。
- 可靠性由副本、ISR、`acks`、`min.insync.replicas`、幂等和事务共同决定。
- 消费进度由消费者主动提交 offset，Kafka Broker 不记录“消息是否已被业务处理”。
- Kafka 原生不提供传统优先级队列、任意精度延迟队列和产品级死信队列，通常需要业务侧或流处理系统补齐。

## 文档目录

- [基础概念](01-basic-concepts.md)
- [生产者](02-producer.md)
- [消费者与 Rebalance](03-consumer-and-rebalance.md)
- [Topic、分区与副本](04-topic-partition-replica.md)
- [日志存储与清理](05-log-storage.md)
- [Controller、Broker 与 KRaft](06-controller-broker-kraft.md)
- [可靠性、幂等与事务](07-reliability-idempotence-transaction.md)
- [性能调优与故障排查](08-performance-and-troubleshooting.md)
