# 大数据面试重点与案例

## 技术主线

- 数据链路通常是采集、存储、计算、建模、服务、治理和运维。
- 批处理关注吞吐、成本和准确性，流处理关注延迟、状态、一致性和乱序。
- 湖仓关注开放表格式、ACID、Schema 演进、Time Travel、元数据和多引擎读写。

## Spark 高频题

- RDD 是弹性分布式数据集，DataFrame/Dataset 通过 Catalyst 和 Tungsten 做优化。
- Shuffle 是性能关键，宽依赖会触发 Shuffle，容易带来磁盘、网络和内存压力。
- 数据倾斜常用加盐、两阶段聚合、广播小表、拆分热点 key、调整分区解决。
- 缓存要结合复用次数和内存成本，盲目 cache 会挤压执行内存。

## Flink 高频题

- Checkpoint 保证状态一致性，Savepoint 用于升级和迁移。
- Exactly-once 依赖状态快照和 Sink 两阶段提交或幂等写。
- Watermark 处理事件时间乱序，窗口触发和迟到数据处理要结合业务延迟。
- 状态后端、TTL、反压、Checkpoint 超时是生产排障重点。

## 数仓与湖仓

- ODS/DWD/DWS/ADS 分层要说明职责：原始、明细、汇总、应用服务。
- 维度建模关注事实表、维度表、粒度、退化维、缓慢变化维和指标口径。
- Iceberg/Hudi/Delta 解决表级事务、增量读、Schema 演进和小文件治理。

## OLAP

- ClickHouse 适合高吞吐列式分析，依赖分区、排序键、稀疏索引和 MergeTree。
- Doris 适合实时数仓和交互分析，关注 tablet、副本、物化视图和导入链路。
- Trino 适合联邦查询，性能依赖数据源、谓词下推、Join 策略和集群资源。

## 排障案例

### 数据倾斜

- 现象：少数 task 长尾，整体作业等待。
- 排查：Stage task 时间、shuffle read/write、热点 key 分布。
- 处理：热点 key 拆分、加盐、广播小表、预聚合、调整分区。

### 小文件过多

- 影响：NameNode/元数据压力、查询 planning 慢、读取效率低。
- 处理：合并小文件、合理分区、控制并发写入、使用 compaction。

### Flink 延迟升高

- 排查：反压、Checkpoint 时间、状态大小、下游 Sink、Kafka lag。
- 处理：扩并行度、优化状态、异步 IO、限流下游、调整 Checkpoint 参数。

### 指标对不上

- 排查：口径、时间窗口、去重逻辑、迟到数据、维表版本、任务补数。
- 处理：指标字典、血缘、数据质量校验、统一口径服务。
