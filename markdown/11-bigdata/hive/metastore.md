# Hive Metastore

Hive Metastore 是 Hive 的元数据服务，保存库、表、字段、分区、存储位置、文件格式等信息。

## 保存什么

- Database 信息。
- Table 信息。
- Column 字段和类型。
- Partition 分区信息。
- StorageDescriptor：路径、格式、压缩、SerDe。
- 权限和统计信息。

## 为什么重要

计算引擎并不直接从 HDFS 目录猜测表结构，而是通过 Metastore 获取表元数据。

很多组件都会访问 Metastore：

- Hive
- Spark SQL
- Presto/Trino
- Flink SQL
- Impala

## 常见部署

- 元数据存储在 MySQL/PostgreSQL。
- Metastore Service 对外提供 Thrift 接口。
- 多计算引擎共享同一个 Metastore。

## 常见问题

- 分区太多导致 Metastore 查询慢。
- 元数据库连接池不足。
- 表结构变更未同步。
- 多引擎写元数据不一致。
- 权限和 Catalog 治理混乱。

## 与湖仓 Catalog

Iceberg/Hudi/Delta Lake 通常也需要 Catalog 管理表元数据。Hive Metastore 可以作为 Iceberg Catalog 的一种实现，但现代架构也会使用 REST Catalog、Glue、Nessie 等。

## 面试重点

Metastore 是数据湖/数仓的“表目录”。没有它，计算引擎很难知道数据在哪里、字段是什么、分区有哪些。
