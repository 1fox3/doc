# Hive

Hive 是构建在 Hadoop 生态上的数据仓库工具，通过 SQL 方式处理 HDFS 上的大规模数据。

## 核心架构

- HiveServer2：对外提供 JDBC/ODBC 查询服务。
- Driver：解析 SQL、生成执行计划、提交任务。
- Metastore：存储库、表、分区、字段、位置等元数据。
- Execution Engine：可使用 MapReduce、Tez、Spark 等执行引擎。
- Storage：通常是 HDFS、对象存储或湖仓表格式。

## 表类型

- 内部表：Hive 管理数据生命周期，删表会删除数据。
- 外部表：Hive 只管理元数据，删表通常不删除底层数据。
- 分区表：按日期、业务线等字段拆目录，提高裁剪效率。
- 分桶表：按字段 hash 到固定 bucket，利于采样和 Join 优化。

## 文件格式

- TextFile：简单但性能差。
- ORC：Hive 常用列式格式，支持压缩、索引和谓词下推。
- Parquet：生态通用列式格式，Spark/Presto/Trino 常用。
- Avro：适合 schema 演进和行式交换。

## 常见场景

- 离线数仓 ETL。
- 日志分析和报表统计。
- 用户画像和宽表构建。
- 大规模明细数据归档查询。

## 面试重点

- Metastore 的作用。
- 分区和分桶的区别。
- 小文件治理。
- Hive SQL 执行流程。
- Map Join、Bucket Join、Sort Merge Bucket Join。
- ORC/Parquet 的优势。

## 相关文档

- [Hive SQL 优化](sql-optimization.md)
