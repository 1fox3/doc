# Apache Doris

Apache Doris 是高性能实时分析数据库，适合报表分析、用户行为分析、实时数仓 ADS 层和多维 OLAP 查询。

## 核心架构

- FE：Frontend，负责元数据、SQL 解析、优化、调度和集群管理。
- BE：Backend，负责数据存储、计算执行和副本管理。
- Tablet：数据分片单位。
- Stream Load/Routine Load/Broker Load：常见导入方式。

## 数据模型

- Duplicate Key：明细模型，保留重复数据，适合日志明细。
- Aggregate Key：聚合模型，导入时按 key 聚合指标。
- Unique Key：唯一模型，适合主键更新场景。
- Primary Key：更适合高频更新和部分列更新的新模型。

## 为什么适合实时数仓

- 支持高并发低延迟 OLAP 查询。
- 支持 Kafka Routine Load 实时导入。
- 支持物化视图、分区、分桶和向量化执行。
- SQL 兼容性较好，易服务 BI 和报表。

## 设计重点

- 分区：通常按日期分区，便于冷热管理和分区裁剪。
- 分桶：按高频过滤或 Join 字段 hash 分桶，避免数据倾斜。
- Key 模型：根据明细、聚合、更新需求选择。
- 副本：根据可用性和成本设置副本数。

## 常见问题

- 导入失败：字段类型不匹配、脏数据、版本堆积、内存限制。
- 查询慢：分区未裁剪、分桶不合理、大宽表扫描、高基数聚合。
- Compaction 压力：小批量写入过多或更新频繁。

## Doris 与 ClickHouse

- Doris 更强调实时导入、MPP 查询、易用性和 MySQL 协议兼容。
- ClickHouse 在列式压缩、单表明细分析和生态成熟度上有优势。
- 选型要看写入频率、查询并发、更新需求、运维能力和团队熟悉度。
