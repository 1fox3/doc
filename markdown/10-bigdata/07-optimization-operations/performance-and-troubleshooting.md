# 性能优化与线上排障

大数据性能问题通常不是单点问题，而是数据分布、文件组织、资源调度、SQL 计划、状态大小、下游写入和治理策略共同作用的结果。

## 优化原则

- 少读数据：分区裁剪、列裁剪、谓词下推和文件级统计信息。
- 少 Shuffle：预过滤、预聚合、广播小表、合理 Join 顺序。
- 少小文件：控制写入并发、批次和 rolling policy，定期 compaction。
- 避免热点：合理 key、分区、分桶、RowKey 和 Kafka 分区策略。
- 让查询模式驱动表设计：分区、排序键、分桶和主键模型必须服务真实查询。
- 先定位瓶颈再优化，不要盲目加资源。

## 数据倾斜

数据倾斜表现为少数 Task 或 SubTask 处理数据远多于其他任务，导致整体拖尾。

常见场景：

- `group by` 热点 key。
- Join 某些 key 数据量极大。
- 空值、默认值或 unknown 集中。
- 分区字段选择不合理。
- Kafka 分区 key 不均衡。
- HBase RowKey 单调递增导致 Region 热点。

定位方法：

- 查看 Spark/Flink UI 中 Task 输入数据量、执行时间和 Shuffle Read/Write。
- 查看 Reduce 或 SubTask 是否明显拖尾。
- 统计 key 分布 TopN。
- 检查空值、未知值、默认值比例。
- 对比 Kafka 分区 Lag 和写入速率。

处理方案：

- 过滤无效 key，例如 null、unknown、测试数据。
- 热点 key 单独处理，拆成独立任务或特殊逻辑。
- 加随机前缀打散，先局部聚合，再去前缀二次聚合。
- 小表使用 Broadcast Join，避免大 Shuffle。
- 开启 Spark AQE Skew Join。
- 重新设计分区键、分桶键、RowKey 或 Kafka key。

## 小文件治理

小文件会增加 NameNode、Metastore、Catalog 和计算引擎规划压力，也会导致任务 Split 过多、调度开销高、查询性能下降。

产生原因：

- 上游并发写入过高，每个并发生成小文件。
- Flink Checkpoint 或滚动策略过频。
- Hive 动态分区过多。
- Kafka 分区过多或批次太小。
- 频繁小批量导入湖仓表、ClickHouse 或 Doris。

影响：

- NameNode 元数据内存压力大。
- 查询需要打开大量文件，IO 开销高。
- Hive/Spark 任务数量过多。
- 湖仓 manifest、metadata 膨胀。
- ClickHouse/Doris compaction 压力上升。

治理方案：

- 写入端控制并发、批次和滚动文件大小。
- Spark 使用 `coalesce` 或 `repartition` 控制输出文件数。
- Hive 使用 `insert overwrite` 合并分区。
- Iceberg/Hudi 使用表服务合并小文件。
- Flink FileSink 配置合理 rolling policy。
- ClickHouse/Doris 尽量批量导入，避免高频小批次。

## SQL 慢查询

常见原因：

- 未命中分区裁剪。
- 对过滤字段使用函数或类型转换。
- `select *` 导致扫描过多列。
- Join 顺序和 Join 策略错误。
- 大表 Join 大表产生巨大 Shuffle。
- 数据倾斜。
- 小文件或小 Part 过多。
- 统计信息缺失导致优化器计划不准。

排查步骤：

1. 查看执行计划，确认分区裁剪、列裁剪和谓词下推是否生效。
2. 查看扫描数据量、输入文件数和输出行数。
3. 查看 Shuffle Read/Write、Stage 耗时和 Task 分布。
4. 检查 Join 类型、Join 顺序和广播阈值。
5. 检查表分区、排序键、分桶、统计信息和小文件数量。

## 实时链路延迟

可能原因：

- Kafka 积压。
- Flink 反压。
- Checkpoint 超时或堆积。
- Watermark 推进慢。
- 维表查询慢。
- 下游 Sink 写入慢。
- 调度或队列资源不足。

排查方式：

- 看 Kafka consumer lag、分区 Lag 和 Topic 写入速率。
- 看 Flink backpressure、busy time、idle time 和 checkpoint duration。
- 看状态大小、RocksDB IO 和 GC。
- 看下游 ClickHouse、Doris、HBase、数据库写入 QPS 和错误。
- 检查最近发布、DDL 变更、数据量突增和下游限流。

## 任务失败

常见原因：

- 数据格式异常。
- Schema 变更。
- 权限不足。
- 资源不足。
- 外部系统不可用。
- 状态序列化不兼容。
- 代码发布引入逻辑错误。

排查方法：

- 先看第一条异常，而不是最后的失败汇总。
- 对比最近发布、配置变更和上游 DDL。
- 检查失败是否集中在某个分区、字段、key 或文件。
- 对实时任务检查是否从 Checkpoint/Savepoint 恢复失败。
- 对离线任务检查输入分区是否缺失或格式不一致。

## 指标异常

可能原因：

- 上游数据缺失或延迟。
- 去重逻辑变化。
- 维表未更新或维表 Join 失败。
- 实时与离线时间窗口不一致。
- 口径变更未同步。
- 测试数据、机器人流量或内部账号未过滤。

排查方式：

- 从 ADS 反查 DWS、DWD、ODS。
- 对比实时和离线链路的输入、窗口、过滤条件和去重 key。
- 检查分区产出、行数、空值率、枚举值和 TopN。
- 对核心指标建立分层对账规则。

## OLAP 查询慢

ClickHouse/Doris 常见原因：

- 分区未裁剪。
- 排序键或分桶设计不匹配查询。
- 扫描列太多。
- 小 Part、小 Tablet 或小 Segment 过多。
- 大 Join、高基数聚合或大结果排序。
- 后台 Merge/Compaction 压力大。

处理方式：

- 按时间和核心过滤条件设计分区、排序键或分桶。
- 使用物化视图、聚合表或宽表预计算高频指标。
- 控制导入批次，降低小文件和小 Part。
- 限制无时间范围查询和大结果导出。
- 对高并发报表做缓存、预热或查询队列隔离。

## 排障流程

1. 先止血：降级、暂停下游、切换离线结果、扩容、限流或回滚。
2. 定范围：确认是单任务、单表、单分区、单租户还是全链路问题。
3. 看变更：代码发布、配置、DDL、权限、上游流量和下游容量。
4. 查链路：Source、Kafka、Compute、Storage、Serving、Quality 逐层定位。
5. 做修复：补数、重跑、回滚、修复脏数据、重建索引或重新提交任务。
6. 补机制：监控、质量规则、血缘影响分析、容量预警和变更流程。

## 生产监控清单

- Kafka：Lag、写入速率、消费速率、分区倾斜。
- Flink：反压、Checkpoint、状态大小、重启次数、Watermark 延迟。
- Spark/Hive：任务耗时、扫描量、Shuffle、失败率、队列等待时间。
- HDFS/对象存储：文件数、小文件比例、存储增长、读写错误。
- Lakehouse：快照数、manifest 数、小文件数、compaction 状态。
- OLAP：慢查询、扫描字节数、导入失败、Part/Tablet 数、Compaction/Merge。
- Governance：质量规则失败、SLA 延迟、权限审计、成本异常。
