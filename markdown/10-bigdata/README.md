# 大数据技术知识库

本目录按技术能力域重新组织大数据内容，仅保留架构、机制、工程设计、治理、优化和排障相关内容。原先按组件分散的 Hadoop、Hive、Spark、Flink、HBase、ClickHouse、Doris、Trino、湖仓、采集、治理等文档已合并为主题文档，减少重复并补充生产实践。

## 目录结构

- `00-foundation`：大数据基础架构、批流模式、存储计算分离、数据格式与压缩。
- `01-storage`：HDFS、对象存储、HBase、Hive Metastore、分区分桶和表组织。
- `02-compute`：MapReduce、Spark、Flink、YARN 和资源管理。
- `03-ingestion`：日志采集、数据同步、CDC、一致性和下游写入。
- `04-warehouse-lakehouse`：数仓分层、维度建模、指标体系、实时数仓、Iceberg、Hudi、Delta Lake。
- `05-olap-serving`：ClickHouse、Doris、Trino、HBase Serving 和 OLAP 表设计。
- `06-governance-platform`：元数据、血缘、数据质量、权限安全、调度和成本治理。
- `07-optimization-operations`：数据倾斜、小文件、慢查询、实时延迟、指标异常和线上排障。

## 推荐阅读顺序

1. [大数据架构与基础概念](00-foundation/architecture-and-concepts.md)
2. [数据格式与压缩](00-foundation/file-format-and-compression.md)
3. [分布式存储：HDFS、对象存储与 HBase](01-storage/distributed-storage.md)
4. [Hive Metastore 与表组织](01-storage/hive-metastore-and-table-layout.md)
5. [批计算：MapReduce 与 Spark](02-compute/batch-compute-spark-mapreduce.md)
6. [流计算：Flink 状态、窗口与一致性](02-compute/stream-compute-flink.md)
7. [资源管理：YARN 与多租户调度](02-compute/resource-management-yarn.md)
8. [数据采集、同步与 CDC](03-ingestion/data-ingestion-and-cdc.md)
9. [数仓分层、维度建模与指标体系](04-warehouse-lakehouse/data-warehouse-modeling.md)
10. [湖仓表格式：Iceberg、Hudi 与 Delta Lake](04-warehouse-lakehouse/lakehouse-table-formats.md)
11. [OLAP 查询与数据服务：ClickHouse、Doris、Trino、HBase](05-olap-serving/olap-engines-and-serving.md)
12. [数据治理与平台能力](06-governance-platform/governance-and-platform.md)
13. [性能优化与线上排障](07-optimization-operations/performance-and-troubleshooting.md)
14. [面试重点与案例](08-interview-and-cases.md)

## 按技术组件阅读

- Hadoop/HDFS：阅读 [分布式存储：HDFS、对象存储与 HBase](01-storage/distributed-storage.md) 和 [资源管理：YARN 与多租户调度](02-compute/resource-management-yarn.md)。
- YARN：阅读 [资源管理：YARN 与多租户调度](02-compute/resource-management-yarn.md)。
- MapReduce：阅读 [批计算：MapReduce 与 Spark](02-compute/batch-compute-spark-mapreduce.md)。
- Hive：阅读 [Hive Metastore 与表组织](01-storage/hive-metastore-and-table-layout.md) 和 [数仓分层、维度建模与指标体系](04-warehouse-lakehouse/data-warehouse-modeling.md)。
- Spark：阅读 [批计算：MapReduce 与 Spark](02-compute/batch-compute-spark-mapreduce.md) 和 [性能优化与线上排障](07-optimization-operations/performance-and-troubleshooting.md)。
- Flink：阅读 [流计算：Flink 状态、窗口与一致性](02-compute/stream-compute-flink.md)、[数据采集、同步与 CDC](03-ingestion/data-ingestion-and-cdc.md) 和 [数仓分层、维度建模与指标体系](04-warehouse-lakehouse/data-warehouse-modeling.md)。
- HBase：阅读 [分布式存储：HDFS、对象存储与 HBase](01-storage/distributed-storage.md) 和 [OLAP 查询与数据服务：ClickHouse、Doris、Trino、HBase](05-olap-serving/olap-engines-and-serving.md)。
- ClickHouse：阅读 [OLAP 查询与数据服务：ClickHouse、Doris、Trino、HBase](05-olap-serving/olap-engines-and-serving.md) 和 [性能优化与线上排障](07-optimization-operations/performance-and-troubleshooting.md)。
- Doris：阅读 [OLAP 查询与数据服务：ClickHouse、Doris、Trino、HBase](05-olap-serving/olap-engines-and-serving.md)。
- Trino/Presto：阅读 [OLAP 查询与数据服务：ClickHouse、Doris、Trino、HBase](05-olap-serving/olap-engines-and-serving.md) 和 [湖仓表格式：Iceberg、Hudi 与 Delta Lake](04-warehouse-lakehouse/lakehouse-table-formats.md)。
- Iceberg/Hudi/Delta Lake：阅读 [湖仓表格式：Iceberg、Hudi 与 Delta Lake](04-warehouse-lakehouse/lakehouse-table-formats.md)。
- Flink CDC/Canal/Debezium/DataX：阅读 [数据采集、同步与 CDC](03-ingestion/data-ingestion-and-cdc.md)。
- Kafka 在大数据链路中的使用：阅读 [数据采集、同步与 CDC](03-ingestion/data-ingestion-and-cdc.md) 和 [流计算：Flink 状态、窗口与一致性](02-compute/stream-compute-flink.md)。
- 调度、元数据、血缘、质量、权限：阅读 [数据治理与平台能力](06-governance-platform/governance-and-platform.md)。
- 面试复习和项目表达：阅读 [面试重点与案例](08-interview-and-cases.md)。

## 技术主线

一条完整的数据链路通常包括：业务库 CDC 或日志采集进入 Kafka，Flink 做实时清洗、去重、维表 Join 和聚合，Iceberg/Hudi/Hive 保存 ODS/DWD/DWS 数据资产，Spark/Hive/Trino 承担离线加工和交互式分析，ClickHouse/Doris/HBase/Redis 服务 ADS 查询和在线特征，元数据、血缘、质量、权限、调度和成本治理贯穿全链路。
