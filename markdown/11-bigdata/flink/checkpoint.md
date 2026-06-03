# Flink Checkpoint

Checkpoint 是 Flink 容错机制的核心，通过周期性生成分布式一致性快照，在故障后恢复状态和消费位置。

## 核心原理

- JobManager 周期性触发 Checkpoint。
- Source 接收 Checkpoint Barrier，并将 Barrier 注入数据流。
- Barrier 随数据流经过各个算子。
- 算子收到所有上游 Barrier 后对状态做快照。
- 所有算子完成快照后，Checkpoint 成功。

## Barrier 对齐

- 对齐 Checkpoint：多输入算子等待所有输入流的 Barrier 到齐，保证一致性。
- 非对齐 Checkpoint：将输入缓冲中的数据也纳入快照，适合反压严重场景。

## State Backend

- HashMapStateBackend：状态在 JVM 堆内，适合小状态、低延迟。
- EmbeddedRocksDBStateBackend：状态在 RocksDB，适合大状态，但读写有序列化和磁盘成本。
- Changelog State Backend：减少大状态 Checkpoint 成本。

## Checkpoint 配置

- 间隔：不能过短，否则影响吞吐。
- 超时时间：状态大或外部存储慢时需要调大。
- 最小间隔：避免 Checkpoint 堆积。
- 并发数：通常设置为 1，降低复杂度。
- Externalized Checkpoint：作业取消后保留快照。

## 常见问题

- Checkpoint 超时：状态过大、反压、外部存储慢、Barrier 对齐慢。
- Checkpoint 失败：状态序列化错误、权限问题、存储不可用。
- 恢复慢：状态大、RocksDB 文件多、网络或对象存储慢。

## 面试重点

Checkpoint 不是简单定时保存数据，它是基于 Barrier 的分布式一致性快照，配合 Source offset 和 Sink 事务能力，才能支撑端到端一致性。
