# 消费者与 Rebalance

## 消费者模型

Kafka 消费端以 Consumer Group 为单位进行水平扩展。同一个 group 内，一个分区同一时刻只能分配给一个消费者；不同 group 之间互不影响，各自维护消费进度。

## 消费流程

1. 创建 KafkaConsumer 并配置 `group.id`、反序列化器和拉取参数。
2. 使用 `subscribe` 订阅 Topic，或使用 `assign` 指定分区。
3. 循环调用 `poll` 拉取消息。
4. 执行业务处理。
5. 提交 offset。
6. 关闭消费者时触发离组和资源释放。

## Offset 提交

- 自动提交：`enable.auto.commit=true`，使用简单但容易出现“已提交未处理完成”。
- 同步提交：`commitSync`，失败会重试，链路清晰但影响吞吐。
- 异步提交：`commitAsync`，吞吐较好，但需要处理回调和提交乱序。
- 指定位移：`seek`、`beginningOffsets`、`endOffsets`、`offsetsForTimes` 可用于补偿、回放和按时间恢复。

## Rebalance 触发原因

- group 内消费者数量变化。
- Topic 分区数变化。
- 消费者超过 `session.timeout.ms` 未发送心跳。
- 消费处理时间超过 `max.poll.interval.ms`。
- 使用动态订阅时元数据变化。

## Rebalance 风险

- Rebalance 期间部分分区暂停消费，导致延迟升高。
- 未提交的 offset 可能导致重复消费。
- 频繁 Rebalance 通常说明消费者处理过慢、GC 停顿、网络抖动或实例频繁发布。

## 多线程消费

- 一个线程一个 KafkaConsumer：最简单，线程数通常不超过分区数。
- 单 Consumer 拉取，多工作线程处理：吞吐更高，但 offset 提交必须按分区有序推进，不能在某条消息未完成时提交后续 offset。
- KafkaConsumer 非线程安全，不要多个线程同时调用同一个实例的 `poll`、`commit`、`seek`。

## 实践建议

- 先处理业务，再提交 offset，并为业务处理设计幂等键。
- 对慢下游使用限流、隔离线程池、熔断或暂停分区消费。
- 使用 `ConsumerRebalanceListener` 在分区撤销前提交已完成 offset。
