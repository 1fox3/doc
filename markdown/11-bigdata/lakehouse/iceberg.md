# Apache Iceberg

Iceberg 是开放湖仓表格式，解决 Hive 表在大规模数据湖中的元数据、事务、Schema 演进和多引擎一致性问题。

## 核心能力

- ACID 事务：通过快照提交保证原子性。
- Snapshot：每次提交生成新快照，支持时间旅行和回滚。
- Schema Evolution：支持字段新增、删除、重命名和类型演进。
- Partition Evolution：支持分区策略演进，不需要重写全表。
- Hidden Partition：查询无需显式感知物理分区字段。

## 元数据结构

- Catalog：管理表位置和当前元数据指针。
- Metadata File：记录表 schema、分区、快照等。
- Manifest List：记录本次快照涉及的 manifest。
- Manifest File：记录数据文件和统计信息。
- Data File：真实 Parquet/ORC/Avro 数据文件。

## 查询优化

- 分区裁剪。
- 文件级统计信息裁剪。
- 列式格式谓词下推。
- Snapshot 隔离减少读写冲突。

## 适合场景

- 多引擎共享数据湖：Spark、Flink、Trino、Hive。
- 大规模离线和近实时数仓。
- 需要 schema/分区演进的长期数据资产。
- 需要时间旅行和回滚的场景。

## 面试重点

Iceberg 不是计算引擎，也不是存储系统，它是表格式。它通过元数据和快照机制，让对象存储/HDFS 上的数据具备接近数仓表的管理能力。
