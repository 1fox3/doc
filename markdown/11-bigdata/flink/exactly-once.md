# Flink Exactly Once

Flink 的 Exactly Once 指在故障恢复后，状态计算结果不重复、不丢失。端到端 Exactly Once 还要求 Source 和 Sink 配合。

## 层次区分

- 状态 Exactly Once：Flink 内部状态通过 Checkpoint 保证一致恢复。
- Source Exactly Once：Source 需要可重放并能保存消费位置，例如 Kafka offset。
- Sink Exactly Once：Sink 需要事务、幂等或两阶段提交能力。

## Kafka Source

- Checkpoint 成功时提交 offset。
- 故障恢复时从 Checkpoint 中的 offset 继续消费。
- 如果处理成功但 Checkpoint 未完成，恢复后可能重新消费，但状态会回滚到一致点。

## 两阶段提交 Sink

1. 开启事务并写入临时结果。
2. Checkpoint 触发时预提交事务。
3. Checkpoint 成功后正式提交事务。
4. Checkpoint 失败或任务失败时回滚事务。

## 常见 Sink 方案

- Kafka：事务 Producer 支持 Exactly Once。
- 数据库：可通过幂等主键、事务表、批次号保证最终一致。
- 文件系统：先写临时文件，Checkpoint 成功后提交文件。
- ClickHouse/ES：通常依赖幂等写入或去重策略，严格 Exactly Once 较难。

## 常见误区

- Flink 开启 Checkpoint 不等于端到端 Exactly Once。
- Exactly Once 不代表外部系统看不到中间状态，取决于 Sink 提交语义。
- 幂等写入常比强事务更实用，但需要业务主键和去重策略。

## 面试回答模板

Flink 内部通过 Barrier 和 Checkpoint 保证状态一致性；Source 通过保存 offset 支持重放；Sink 通过两阶段提交或幂等写入保证外部结果一致。因此端到端 Exactly Once 是 Source、Flink 状态和 Sink 三者共同完成的。
