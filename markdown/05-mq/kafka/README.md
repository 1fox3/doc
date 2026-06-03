# Kafka

> 来源：Kafka.xmind

## 核心认知

- Kafka 是以日志为核心的高吞吐分布式消息系统，主题、分区、副本和 offset 是基础模型。
- 吞吐来自顺序写、页缓存、批量发送、零拷贝和分区并行。

## 面试重点

- Producer ack、幂等生产、事务、分区器、ISR、Leader/Follower、副本同步。
- Consumer Group、Rebalance、offset 提交、消息重复和顺序消费。

## 实践检查点

- 能解释 `acks=all`、`min.insync.replicas`、副本数之间的可靠性关系。
- 能处理 Rebalance 过频、消费滞后和分区热点问题。

## 版本与趋势

- Kafka 3.x 进入 KRaft 去 ZooKeeper 架构阶段，新集群应关注 Controller Quorum、分层存储和再均衡优化。
- Kafka 的核心仍是分区日志模型，所有吞吐、顺序、可靠性和扩展性问题都应回到分区与副本分析。

## 章节目录

- [初识Kafka](01-初识kafka.md)
- [生产者](02-生产者.md)
- [消费者](03-消费者.md)
- [主题](04-主题.md)
- [分区](05-分区.md)
- [日志](06-日志.md)
- [服务端](07-服务端.md)
- [客户端](08-客户端.md)
- [可靠性](09-可靠性.md)
- [instantiate](10-instantiate.md)
