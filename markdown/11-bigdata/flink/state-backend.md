# Flink State Backend

State Backend 决定 Flink 状态如何存储、访问和做 Checkpoint。

## 为什么需要状态

很多流计算不是单条事件独立处理，而是需要记住历史：

- 去重。
- 窗口聚合。
- Join。
- 规则匹配。
- 用户会话。

## 状态类型

- ValueState：保存单个值。
- ListState：保存列表。
- MapState：保存 Map。
- ReducingState/AggregatingState：保存聚合结果。
- BroadcastState：广播配置或规则。

## Backend 类型

### HashMapStateBackend

- 状态存储在 JVM 堆内。
- 访问速度快。
- 适合小状态和低延迟任务。
- 大状态容易 GC 压力大。

### EmbeddedRocksDBStateBackend

- 状态存储在 RocksDB。
- 支持大状态。
- 读写需要序列化和本地磁盘 IO。
- 调优复杂度更高。

## TTL

状态 TTL 用于清理长期不用的状态，避免状态无限增长。

注意：TTL 清理不一定实时发生，具体取决于访问、快照和后台清理策略。

## 常见问题

- 状态过大导致 Checkpoint 慢。
- RocksDB 写放大导致磁盘 IO 高。
- TTL 设置不合理导致状态泄漏或结果不准确。
- 状态序列化变更导致恢复失败。

## 面试重点

小状态、低延迟优先 HashMap；大状态优先 RocksDB。状态设计要关注 key 粒度、TTL、序列化兼容和 Checkpoint 成本。
