# 大数据学习路线

如果你没有大数据基础，建议按“概念 -> 存储 -> 计算 -> 数仓 -> 实时 -> OLAP -> 治理 -> 项目”学习。

## 第一阶段：建立概念

- OLTP 与 OLAP。
- 离线与实时。
- 批处理与流处理。
- 存储与计算分离。
- 数据湖、数仓、湖仓。

建议阅读：

- [大数据基础概念](fundamentals/basic-concepts.md)
- [批处理与流处理](fundamentals/batch-vs-stream.md)

## 第二阶段：Hadoop 基础

- HDFS 架构和读写流程。
- YARN 资源调度。
- MapReduce Shuffle。

建议阅读：

- [HDFS](hadoop/hdfs.md)
- [YARN](hadoop/yarn.md)
- [MapReduce](hadoop/mapreduce.md)

## 第三阶段：Hive 和数仓

- Hive 架构。
- 分区分桶。
- SQL 优化。
- ODS/DWD/DWS/ADS。
- 指标口径。

## 第四阶段：Spark 和 Flink

- Spark Shuffle、内存、SQL 优化。
- Flink Window、Watermark、State、Checkpoint、Exactly Once。

## 第五阶段：查询与服务

- ClickHouse/Doris。
- HBase。
- Trino。

## 第六阶段：治理和项目

- 调度系统。
- 元数据血缘。
- 数据质量。
- 权限安全。
- 成本治理。
- 项目面试表达。

## 找工作建议

Java 后端不需要一开始掌握所有大数据组件，但要能讲清一条完整链路：数据从哪里来，如何进入 Kafka，如何用 Flink/Spark 处理，如何进入湖仓或 OLAP，如何保证质量、延迟和一致性。
