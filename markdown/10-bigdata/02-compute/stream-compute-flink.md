# 流计算：Flink 状态、窗口与一致性

Flink 是面向有状态流处理的分布式计算引擎，适合实时数仓、风控、监控告警、实时特征、事件驱动应用和低延迟数据同步。

## 核心角色

- JobManager：负责任务调度、Checkpoint 协调和故障恢复。
- TaskManager：执行算子任务，管理 Slot。
- Slot：资源调度单位。
- Operator：流处理算子。
- State：有状态计算保存的历史数据。
- Checkpoint：一致性快照，用于故障恢复。
- Watermark：事件时间进度标记，用于处理乱序数据。

## 时间语义

- Processing Time：机器处理时间，实现简单、延迟低，但结果受处理速度和机器时间影响。
- Event Time：事件发生时间，适合乱序数据和业务时间窗口。
- Ingestion Time：数据进入 Flink 的时间，使用较少。

实时指标通常应优先使用 Event Time，否则补发、延迟和乱序会导致窗口结果不稳定。

## Window

流是无界的，Window 用于把无界流切成有限范围。

常见窗口：

- Tumbling Window：滚动窗口，固定长度，不重叠。
- Sliding Window：滑动窗口，固定长度，按步长滑动，可重叠。
- Session Window：会话窗口，根据事件间隔动态切分。
- Global Window：全局窗口，需要自定义 Trigger。

## Watermark、乱序与迟到

Watermark 是事件时间进度标记，表示系统认为早于该时间的数据基本已经到齐。

常见策略：

- Watermark 通常是“当前观测到的最大事件时间减去允许乱序时间”。
- Allowed Lateness 允许窗口关闭后一段时间继续接收迟到数据。
- Side Output 用于输出严重迟到数据，便于后续补偿或审计。
- 空闲分区需要配置 idleness，否则某些 Kafka 分区无数据会拖慢全局 Watermark。

Watermark 推进太慢会导致窗口迟迟不触发，推进太快会增加迟到丢弃和修正成本。

## State 类型

- ValueState：保存单个值。
- ListState：保存列表。
- MapState：保存 Map。
- ReducingState/AggregatingState：保存聚合结果。
- BroadcastState：保存广播配置、规则或维表快照。

状态设计要关注 key 粒度、TTL、序列化兼容、状态大小和恢复成本。

## State Backend

HashMapStateBackend：

- 状态存储在 JVM 堆内。
- 访问速度快。
- 适合小状态和低延迟任务。
- 大状态容易造成 GC 压力。

EmbeddedRocksDBStateBackend：

- 状态存储在 RocksDB。
- 支持大状态。
- 读写需要序列化和本地磁盘 IO。
- 调优复杂度更高，关注 block cache、write buffer、compaction 和本地磁盘。

Changelog State Backend 可减少大状态 Checkpoint 成本，但需要评估版本成熟度和运维复杂度。

## Checkpoint 原理

Checkpoint 通过周期性生成分布式一致性快照，在故障后恢复状态和消费位置。

流程：

1. JobManager 周期性触发 Checkpoint。
2. Source 接收 Checkpoint Barrier，并将 Barrier 注入数据流。
3. Barrier 随数据流经过各个算子。
4. 算子收到所有上游 Barrier 后对状态做快照。
5. 所有算子完成快照后，Checkpoint 成功。

对齐 Checkpoint 会等待多输入算子的所有 Barrier 到齐。非对齐 Checkpoint 会把输入缓冲中的数据也纳入快照，适合反压严重场景。

## Checkpoint 配置

- 间隔不能过短，否则影响吞吐并增加外部存储压力。
- 超时时间要结合状态大小、对象存储性能和反压情况设置。
- 最小间隔用于避免 Checkpoint 堆积。
- 并发数通常设置为 1，降低恢复复杂度。
- Externalized Checkpoint 用于作业取消后保留快照。

常见失败原因包括状态过大、反压、外部存储慢、状态序列化错误、权限问题和下游 Sink 阻塞。

## Exactly Once

Flink 内部状态 Exactly Once 不等于端到端 Exactly Once。端到端一致性需要 Source、Flink 状态和 Sink 共同配合。

层次：

- 状态 Exactly Once：Flink 内部状态通过 Checkpoint 保证一致恢复。
- Source Exactly Once：Source 需要可重放并能保存消费位置，例如 Kafka offset。
- Sink Exactly Once：Sink 需要事务、幂等或两阶段提交能力。

两阶段提交 Sink 流程：

1. 开启事务并写入临时结果。
2. Checkpoint 触发时预提交事务。
3. Checkpoint 成功后正式提交事务。
4. Checkpoint 失败或任务失败时回滚事务。

常见 Sink 语义：

- Kafka：事务 Producer 支持 Exactly Once。
- 文件系统：先写临时文件，Checkpoint 成功后提交文件。
- 数据库：通常通过主键幂等、事务表、批次号和去重保证最终一致。
- ClickHouse/ES：严格 Exactly Once 较难，常依赖幂等写入、ReplacingMergeTree、版本字段或业务去重。

## 反压与稳定性

常见原因：

- 下游 Sink 写入慢。
- Checkpoint Barrier 对齐耗时长。
- 某些 key 状态过大或热点严重。
- 外部维表查询慢。
- Kafka 分区和 Flink 并行度不匹配。

处理方式：

- 优先定位瓶颈算子和下游系统，而不是盲目加并行度。
- 对维表 Join 使用异步 IO、缓存、广播维表或 Temporal Join。
- 对热点 key 做拆分、预聚合或单独链路。
- 控制 Sink 批次、连接池、重试和失败队列。
- 配置状态 TTL，避免状态无限增长。

## 流计算工程实践

- Source 数据要具备业务唯一键和事件时间。
- Kafka Topic 分区数要与吞吐和并行度匹配。
- 所有有状态任务都要定义状态 TTL 和恢复策略。
- 重要 Sink 要具备幂等、事务或可补偿能力。
- 保留 Savepoint 和任务版本，支持升级、回滚和重放。
- 监控 Lag、反压、Checkpoint duration、失败重启、状态大小和下游写入延迟。
