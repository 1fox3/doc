# 数据采集、同步与 CDC

数据采集和同步负责把业务库、日志、文件、消息队列中的数据稳定进入数仓、湖仓或分析数据库，是大数据链路的入口。

## 数据来源

- 业务库：MySQL、PostgreSQL、Oracle、SQL Server 等。
- 行为日志：前端埋点、App 埋点、服务端业务日志。
- 网关日志：Nginx、API Gateway、RPC 访问日志。
- 消息队列：Kafka、Pulsar、RocketMQ。
- 文件系统：CSV、JSON、Parquet、业务导出文件。
- 监控数据：指标、Trace、审计日志和系统事件。

## 同步方式

- 全量同步：定期完整导入，适合小表、初始化或低频更新数据。
- 增量同步：按更新时间、递增 ID 或日志位点同步。
- CDC：基于数据库日志捕获变更，例如 MySQL binlog、PostgreSQL WAL。
- 批流一体同步：全量快照和增量日志无缝衔接，常用于实时数仓和入湖。

## 常见工具

- DataX：离线批量同步工具，常用于 MySQL 到 Hive、ClickHouse、Doris。
- Sqoop：Hadoop 生态老牌关系库同步工具，现代项目中使用减少。
- Canal：解析 MySQL binlog，常用于缓存更新、消息同步和简单 CDC。
- Debezium：通用 CDC 平台，支持多种数据库，常与 Kafka Connect 配合。
- Flink CDC：以 Flink Source 方式接入全量和增量数据，适合实时计算和湖仓写入。
- Filebeat/Flume/Logstash：常用于日志采集。

## 日志采集链路

典型链路：

1. 应用输出 JSON 日志到本地文件或标准输出。
2. Filebeat、Flume 或 Logstash 采集并发送到 Kafka。
3. Flink 消费 Kafka 做解析、过滤、补充字段和脏数据分流。
4. 明细写入 HDFS、Iceberg 或 Hudi，聚合结果写入 ClickHouse 或 Doris。
5. 质量任务检查延迟、丢失、重复和字段合法性。

关键设计：

- 日志格式要统一，并包含事件时间、业务主键、traceId、应用、环境和版本。
- Kafka Topic 需要按业务域、数据敏感级别和消费模式规划。
- 分区 key 要兼顾顺序性、负载均衡和下游计算并行度。
- 脏数据进入侧输出或错误 Topic，不能直接丢弃。
- 采集端要有限速、重试、断点续传和本地缓冲策略。

## Flink CDC 流程

1. 全量阶段：并行读取表快照数据。
2. 增量阶段：读取 binlog、WAL 等变更日志。
3. 切换阶段：保证全量快照和增量日志无缝衔接。
4. 位点管理：通过 Checkpoint 记录快照进度和日志位点。
5. 下游写入：写 Kafka、湖仓、Doris、ClickHouse、ES 或数据库。

关键能力：

- Snapshot 读取。
- Binlog/WAL 增量订阅。
- Checkpoint 位点恢复。
- Exactly Once Source 语义。
- DDL 变更同步。

## CDC 难点

- 全量阶段对源库压力大。
- 大表快照耗时长，容易跨越 binlog 保留时间。
- 全量和增量切换需要保证不丢不重。
- DDL 变更可能导致下游 Schema 不兼容。
- 删除事件必须保留语义，否则下游会出现脏数据。
- 主键缺失会影响去重、更新和幂等写入。
- 源库时区、字符集、字段类型和精度可能与下游不一致。

## 数据一致性设计

同步链路要明确语义：

- At Most Once：可能丢数据，一般不适合核心链路。
- At Least Once：不丢但可能重复，需要下游幂等或去重。
- Exactly Once：需要 Source 位点、计算状态和 Sink 提交语义共同配合。

常见工程手段：

- 业务主键或全局唯一事件 ID。
- 下游主键幂等写入。
- 批次号、版本号或操作时间字段。
- CDC 事件保留 `op`、`before`、`after`、`ts_ms` 等元信息。
- Checkpoint 成功后再提交消费位点或 Sink 事务。

## 下游写入策略

- Hive/湖仓：按分区写入，控制小文件，使用 Iceberg/Hudi 提供 upsert、事务和快照能力。
- ClickHouse：尽量批量写入，避免小批次造成 Part 过多；更新场景可用 ReplacingMergeTree 或版本字段。
- Doris：根据明细、聚合、更新需求选择 Duplicate Key、Aggregate Key、Unique Key 或 Primary Key。
- HBase/Redis：适合主键点写和在线特征，必须控制热点 key 和 TTL。
- Kafka：作为中间 Topic 时要定义 Schema、Key、分区策略和保留周期。

## 生产监控

- Source 端抽取延迟、快照进度、binlog 位点和源库 QPS。
- Kafka Lag、Topic 写入速率、分区倾斜和积压大小。
- Flink 反压、Checkpoint duration、失败重启和状态大小。
- Sink 写入 QPS、失败率、重试次数和幂等冲突。
- 端到端延迟、数据量波动、空值率、主键重复和 schema 变更事件。

## 工程实践

- 大表全量同步要分片、限速，并避开源库高峰期。
- 源库 binlog/WAL 保留周期要覆盖最长恢复时间。
- DDL 变更要有发布流程、兼容策略和回滚方案。
- 所有核心同步任务都要支持断点续传和幂等重跑。
- 日志和 CDC 原始数据要保留一段时间，便于补偿和重放。
