# 可靠性、幂等与事务

## 写入可靠性

可靠写入至少需要同时考虑：

- 副本数是否足够。
- ISR 中是否有足够副本。
- Producer `acks` 是否等待足够确认。
- Broker 是否允许 unclean leader election。
- 消费端是否在业务完成后提交 offset。

常见高可靠组合：`replication.factor=3`、`acks=all`、`min.insync.replicas=2`、`unclean.leader.election.enable=false`。

## 幂等生产者

幂等生产者通过 Producer ID、Producer Epoch、分区内序列号去重，解决重试导致的单分区重复写入问题。它不能解决业务层重复请求，也不能让跨分区操作天然原子。

## 事务

Kafka 事务用于保证多个分区写入和消费位移提交的原子性，典型用于 consume-process-produce 链路。

核心概念：

- `transactional.id`：事务生产者身份。
- Transaction Coordinator：管理事务状态。
- `__transaction_state`：事务状态内部 Topic。
- `read_committed`：消费者只读取已提交事务消息。

## Exactly Once 边界

Kafka exactly once 主要保证 Kafka 内部读写链路：从 Kafka 读、处理后写回 Kafka，并在同一事务中提交 offset。只要链路涉及外部数据库、缓存、HTTP 或文件系统，就必须额外设计业务幂等、去重表或事务外盒模式。

## 消费幂等

消费幂等常用方案：

- 使用业务唯一键做数据库唯一约束。
- 在幂等表中记录消息 ID 或事件 ID。
- 使用状态机校验状态流转合法性。
- 下游接口支持幂等 token。
- 对不可重复副作用采用 outbox/inbox 模式。
