# OLAP 查询与数据服务：ClickHouse、Doris、Trino、HBase

OLAP 和数据服务层负责把数仓或湖仓加工后的数据提供给 BI 报表、实时看板、运营分析、用户画像、风控特征和在线接口。

## OLAP Serving 的常见形态

- 明细分析：用户行为、日志、交易明细的多维筛选和聚合。
- 预聚合报表：固定指标、固定维度、高并发查询。
- 联邦查询：跨 Hive、Iceberg、MySQL、Kafka 等数据源临时分析。
- 宽表服务：面向报表或 API 的大宽表查询。
- KV/宽表点查：按用户、设备、账号获取画像或特征。

## ClickHouse

ClickHouse 是高性能列式 OLAP 数据库，适合大宽表、明细分析、报表、日志分析和用户行为分析。

快的原因：

- 列式存储，只读取查询需要的列。
- 向量化执行，提高 CPU 利用率。
- 列式压缩，减少 IO。
- 稀疏索引，通过排序键跳过无关数据块。
- 分区裁剪，减少扫描范围。
- 并行执行，充分利用多核和分布式资源。

适合场景：

- 实时报表。
- 用户行为分析。
- 日志检索和聚合。
- 大宽表多维分析。
- 替代部分 Hive 离线查询和 MySQL 报表查询。

不适合场景：

- 高频小事务更新。
- OLTP 强一致交易。
- 多表复杂事务。
- 低延迟高并发点查不是主要优势。

## MergeTree 表设计

MergeTree 是 ClickHouse 最重要的表引擎家族。

核心结构：

- Partition：按分区表达式拆分数据。
- Part：一次写入生成一个或多个数据片段。
- Mark：稀疏索引标记，定位数据块。
- ORDER BY：决定 Part 内数据排序方式。
- Primary Key：用于构建稀疏索引，通常与 ORDER BY 相同或是其前缀，不保证唯一。

表引擎：

- MergeTree：基础引擎。
- ReplacingMergeTree：按版本或最终合并去重，适合 CDC 明细去重。
- SummingMergeTree：按排序键聚合数值列。
- AggregatingMergeTree：存储聚合状态，适合预聚合。
- CollapsingMergeTree：通过 sign 字段折叠数据。

设计原则：

- 分区键常用日期，例如 `toYYYYMM(dt)` 或 `toDate(event_time)`。
- 分区不宜过细，否则 Part 数量暴增。
- ORDER BY 优先放高频过滤字段，再放常用聚合维度。
- 低基数字段放前面通常有利于压缩和过滤。
- 避免频繁小批量写入，减少小 Part 和后台 Merge 压力。

## ClickHouse 查询优化

- 查询必须带时间范围或分区条件。
- 避免 `select *`。
- 避免对过滤字段使用复杂函数导致索引失效。
- 高基数字段 `group by` 要谨慎。
- Join 前尽量过滤和裁剪列。
- 使用物化视图预聚合高频固定指标。
- 对有局部性的字段使用 minmax、set、bloom_filter、tokenbf_v1 等跳数索引。

慢查询常见原因：

- 分区未裁剪。
- ORDER BY 设计不匹配查询。
- 扫描列太多。
- 小 Part 过多。
- 大 Join 或高基数聚合。
- 后台 Merge 压力大。

## Apache Doris

Doris 是高性能实时分析数据库，适合报表分析、用户行为分析、实时数仓 ADS 层和多维 OLAP 查询。

核心架构：

- FE：Frontend，负责元数据、SQL 解析、优化、调度和集群管理。
- BE：Backend，负责数据存储、计算执行和副本管理。
- Tablet：数据分片单位。
- Stream Load、Routine Load、Broker Load：常见导入方式。

数据模型：

- Duplicate Key：明细模型，保留重复数据，适合日志明细。
- Aggregate Key：聚合模型，导入时按 key 聚合指标。
- Unique Key：唯一模型，适合主键更新场景。
- Primary Key：更适合高频更新和部分列更新的新模型。

设计重点：

- 分区通常按日期，便于冷热管理和分区裁剪。
- 分桶按高频过滤或 Join 字段 hash，避免数据倾斜。
- Key 模型根据明细、聚合、更新需求选择。
- 副本数根据可用性、查询并发和成本设置。

Doris 相比 ClickHouse 更强调实时导入、MPP 查询、MySQL 协议兼容和易用性；ClickHouse 在列式压缩、单表明细分析和生态成熟度上有优势。

## Trino/Presto

Trino 是分布式 SQL 查询引擎，适合跨数据源交互式查询和湖仓分析。它本身不存储数据，核心价值是通过 Connector 连接多种存储，并用 MPP 执行引擎提供交互式 SQL 查询能力。

核心架构：

- Coordinator：解析 SQL、生成执行计划、调度 Worker。
- Worker：执行 Task，读取数据源并交换中间结果。
- Connector：连接 Hive、Iceberg、MySQL、Kafka、ClickHouse、ES 等数据源。
- Catalog：数据源配置入口。

适合场景：

- 数据湖交互式查询。
- 多数据源联邦查询。
- Ad-hoc 分析。
- 替代部分 Hive MR/Tez 慢查询。

不适合场景：

- 大规模复杂 ETL 长任务。
- 高频小事务写入。
- 强一致 OLTP。

优化方式：

- 使用 ORC/Parquet 等列式格式。
- 保证分区裁剪和谓词下推。
- 合理控制 Join 顺序和广播 Join。
- 避免跨源大表 Join。
- 使用动态过滤减少 Probe 侧扫描。
- 控制查询内存、并发和资源组。

## HBase 作为 Serving 层

HBase 不适合复杂 OLAP，但适合按 RowKey 的低延迟点查和范围扫描。

适合场景：

- 用户画像宽表。
- 设备、账号、用户维度明细查询。
- 风控特征存储。
- 海量稀疏 KV 数据。

不适合场景：

- 多字段任意组合查询。
- 复杂 SQL Join 和聚合。
- 报表多维分析。

如果需要多条件检索或聚合，应考虑 ES、ClickHouse、Doris 或冗余多张 HBase 索引表。

## 选型建议

- 高频固定报表、实时 ADS：Doris 或 ClickHouse。
- 明细宽表多维分析：ClickHouse。
- 实时导入、更新和 BI 易用性：Doris。
- 跨源临时分析和湖仓查询：Trino。
- 按主键点查和特征服务：HBase 或 Redis。
- 强事务在线业务：MySQL、PostgreSQL 等 OLTP 数据库，不应使用 OLAP 引擎承载。

## 数据服务实践

- ADS 表必须围绕查询模式设计，而不是简单复制 DWD 明细。
- 写入批次、分区、排序键、分桶和主键模型要共同设计。
- 对高频报表优先预聚合，避免每次扫描明细。
- 查询服务要限制无时间范围扫描、大结果导出和高并发重查询。
- OLAP 表和指标口径要与数仓血缘、质量和权限系统打通。
