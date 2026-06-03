# 大数据方向知识库

本目录补充后端找工作常见的大数据能力栈，重点覆盖离线存储、批处理、实时计算、OLAP 分析、数仓建模和数据链路治理。

## 适合岗位

- Java 后端开发：掌握 HDFS、Hive、Kafka、Flink、ClickHouse 的基本原理和工程使用即可明显加分。
- 数据平台后端：需要理解任务调度、元数据、血缘、数据质量、权限、资源队列和多租户治理。
- 大数据开发：需要深入 Spark/Flink/Hive SQL 优化、数仓建模、实时链路和存储选型。
- 推荐/广告/搜索/风控后端：重点关注日志采集、用户行为流、实时特征、离线画像和 OLAP 查询。

## 学习优先级

1. HDFS、YARN、MapReduce：理解 Hadoop 基础设施。
2. Hive：掌握离线数仓 SQL、分区分桶、小文件治理和 SQL 优化。
3. Kafka + Flink：掌握实时数据流、状态、Checkpoint、Exactly Once。
4. Spark：掌握批处理、Shuffle、内存模型和 Spark SQL 优化。
5. HBase、ClickHouse：理解宽表 KV 和 OLAP 列式分析场景。
6. 数仓建模、CDC、湖仓：能讲清 ODS/DWD/DWS/ADS、维度建模和数据同步链路。

## 面试表达模板

- 这个组件解决什么问题？
- 架构里有哪些核心角色？
- 写入和读取链路是什么？
- 如何保证可靠性和一致性？
- 常见性能瓶颈是什么？
- 线上如何排障和优化？
- 在项目中如何落地？

## 目录

- [Hadoop 总览](hadoop/README.md)
- [HDFS](hadoop/hdfs.md)
- [YARN](hadoop/yarn.md)
- [MapReduce](hadoop/mapreduce.md)
- [Hive](hive/README.md)
- [Hive SQL 优化](hive/sql-optimization.md)
- [Spark](spark/README.md)
- [Spark Shuffle](spark/shuffle.md)
- [Flink](flink/README.md)
- [Flink Checkpoint](flink/checkpoint.md)
- [Flink Exactly Once](flink/exactly-once.md)
- [HBase](hbase/README.md)
- [HBase RowKey 设计](hbase/rowkey-design.md)
- [ClickHouse](clickhouse/README.md)
- [MergeTree](clickhouse/mergetree.md)
- [数仓建模](data-warehouse/README.md)
- [ODS/DWD/DWS/ADS](data-warehouse/ods-dwd-dws-ads.md)
- [数据链路与湖仓](data-pipeline/README.md)
- [实时数仓](data-warehouse/realtime-warehouse.md)
- [Apache Doris](olap/doris.md)
- [Trino/Presto](olap/trino.md)
- [Apache Iceberg](lakehouse/iceberg.md)
- [Apache Hudi](lakehouse/hudi.md)
- [Flink CDC](data-pipeline/flink-cdc.md)
- [数据倾斜治理](optimization/data-skew.md)
- [小文件治理](optimization/small-files.md)
- [任务调度系统](platform/scheduler.md)
- [元数据与血缘](governance/metadata-lineage.md)
- [数据质量](governance/data-quality.md)
- [数据安全与权限](governance/security.md)
- [资源与成本治理](platform/resource-cost.md)
- [大数据项目面试模板](project-experience.md)
- [大数据基础概念](fundamentals/basic-concepts.md)
- [批处理与流处理](fundamentals/batch-vs-stream.md)
- [数据格式与压缩](fundamentals/file-format-compression.md)
- [Hive 分区与分桶](hive/partition-bucket.md)
- [Hive Metastore](hive/metastore.md)
- [Spark RDD/DataFrame/Dataset](spark/rdd-dataframe-dataset.md)
- [Spark 内存与 OOM](spark/memory-oom.md)
- [Flink Window 与 Watermark](flink/window-watermark.md)
- [Flink State Backend](flink/state-backend.md)
- [HBase Compaction 与 Region](hbase/compaction-region.md)
- [ClickHouse 查询优化](clickhouse/query-optimization.md)
- [数据采集与日志链路](data-pipeline/log-collection.md)
- [数据同步工具](data-pipeline/sync-tools.md)
- [指标体系与口径治理](data-warehouse/metrics.md)
- [维度建模与拉链表](data-warehouse/dimensional-modeling.md)
- [湖仓选型对比](lakehouse/table-format-comparison.md)
- [大数据线上排障手册](operations/troubleshooting.md)
- [大数据学习路线](learning-path.md)
