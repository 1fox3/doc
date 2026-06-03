# 数据链路与湖仓

数据链路关注数据从业务系统、日志、消息队列进入数仓或湖仓，并最终服务分析、检索、推荐和风控的全过程。

## 常见链路

- 业务库 CDC -> Kafka -> Flink -> Hudi/Iceberg/ClickHouse。
- 日志采集 -> Kafka -> Flink/Spark -> Hive/ClickHouse/ES。
- MySQL -> DataX/Sqoop -> Hive 离线同步。
- Kafka -> Flink -> Redis/HBase，用于实时特征。

## CDC

- CDC 是 Change Data Capture，捕获数据库变更。
- MySQL 常基于 binlog，例如 Canal、Debezium、Flink CDC。
- 需要处理全量同步、增量同步、断点续传、DDL 变更和乱序。

## Lambda 与 Kappa

- Lambda：离线链路 + 实时链路，两套计算结果合并，稳定但复杂。
- Kappa：只保留流式链路，通过重放消息修正结果，架构简单但依赖消息保留和流计算能力。

## 湖仓表格式

- Hudi：强调 upsert、增量查询和近实时入湖。
- Iceberg：强调开放表格式、快照、Schema 演进和多引擎兼容。
- Delta Lake：Databricks 生态成熟，支持 ACID 和流批统一。

## 数据治理

- 元数据：表、字段、分区、负责人、生命周期。
- 血缘：字段和任务依赖关系。
- 质量：空值、重复、波动、枚举、主键唯一。
- 权限：库表、列级、行级和脱敏策略。
- 成本：存储生命周期、计算资源、冷热分层。

## 面试重点

- CDC 如何保证不丢不重？
- Flink 写湖仓如何保证一致性？
- Hudi、Iceberg、Delta Lake 区别？
- 实时数仓如何分层？
- 数据质量和血缘如何建设？

## 项目表达

可以描述一个实时数仓链路：MySQL binlog 通过 Flink CDC 进入 Kafka，Flink 做清洗和维表关联后写入 Iceberg DWD；DWS 通过 Flink SQL 做实时聚合；ADS 写入 ClickHouse 支撑报表查询，同时用数据质量任务监控延迟、重复和指标波动。
