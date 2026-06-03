# Trino/Presto

Trino 是分布式 SQL 查询引擎，适合跨数据源交互式查询和湖仓分析。Presto 是其前身生态之一。

## 核心架构

- Coordinator：解析 SQL、生成执行计划、调度 Worker。
- Worker：执行 Task，读取数据源并交换中间结果。
- Connector：连接 Hive、Iceberg、MySQL、Kafka、ClickHouse、ES 等数据源。
- Catalog：数据源配置入口。

## 适合场景

- 数据湖交互式查询。
- 多数据源联邦查询。
- Ad-hoc 分析。
- 替代部分 Hive MR/Tez 慢查询。

## 不适合场景

- 大规模复杂 ETL 长任务。
- 高频小事务写入。
- 强一致 OLTP。

## 性能优化

- 使用列式格式 ORC/Parquet。
- 保证分区裁剪和谓词下推。
- 合理控制 Join 顺序和广播 Join。
- 避免跨源大表 Join。
- 使用动态过滤减少 Probe 侧扫描。
- 控制查询内存和并发。

## 与 Hive/Spark 的区别

- Hive 更偏离线数仓和批处理 SQL。
- Spark 更适合复杂 ETL、机器学习和批流统一计算。
- Trino 更适合低延迟交互式 SQL 和联邦查询。

## 面试重点

Trino 本身不存储数据，核心价值是通过 Connector 连接多种存储，并用 MPP 执行引擎提供交互式 SQL 查询能力。
