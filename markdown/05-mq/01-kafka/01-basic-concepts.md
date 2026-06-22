# 基础概念

## 核心模型

- `Producer`：负责把消息写入 Topic。KafkaProducer 通常是线程安全的，可以被多个线程共享。
- `Consumer`：负责拉取并处理消息。KafkaConsumer 不是线程安全的，不能被多个线程同时调用。
- `Broker`：Kafka 服务节点，负责存储日志、处理读写请求、参与副本同步。
- `Topic`：逻辑消息分类，一个 Topic 由多个 Partition 组成。
- `Partition`：Kafka 的并行、顺序和扩展单元。每个分区是一条追加写日志。
- `Replica`：分区副本。每个分区有一个 Leader 副本和若干 Follower 副本。
- `Offset`：消息在分区内的逻辑位置，单调递增，只在分区内有意义。

## Offset 与消费语义

Kafka 不直接知道业务是否处理成功，只保存消费者提交的消费位移。常见语义取决于“处理消息”和“提交 offset”的顺序：

- 先提交 offset 再处理业务：可能丢消息，属于 at most once。
- 先处理业务再提交 offset：可能重复消费，属于 at least once。
- 生产端幂等、事务写入、事务性 offset 提交配合使用，可以在 Kafka 内实现 exactly once，但外部数据库、HTTP 调用等副作用仍需要业务幂等。

## 适用场景

- 日志采集、行为埋点、指标流、数据管道。
- 大吞吐异步解耦场景。
- 流式计算输入源，例如 Kafka Streams、Flink、Spark Streaming。
- 事件驱动架构中的事件日志。

## 不适合场景

- 强实时请求响应，不应把 Kafka 当 RPC。
- 每条消息都要求复杂路由、优先级调度或秒级以下任意延迟。
- 消息量很小但强依赖管理控制台、复杂投递策略和队列语义的场景，RabbitMQ 可能更合适。
