# Hive Metastore 与表组织

Hive 不只是 SQL 工具，更重要的是通过 Metastore、分区、分桶和文件格式把 HDFS 或对象存储上的文件组织成可被多引擎访问的表。

## Hive 架构

- HiveServer2：对外提供 JDBC/ODBC 查询服务。
- Driver：解析 SQL，生成执行计划并提交任务。
- Metastore：存储库、表、字段、分区、路径、格式、统计信息和权限等元数据。
- Execution Engine：可使用 MapReduce、Tez、Spark 等执行引擎。
- Storage：通常是 HDFS、对象存储或湖仓表格式。

## Metastore 保存什么

- Database 信息。
- Table 信息。
- Column 字段和类型。
- Partition 分区信息。
- StorageDescriptor：路径、格式、压缩和 SerDe。
- 表统计信息、权限信息和生命周期信息。

计算引擎不会从目录自动猜测表结构，而是通过 Metastore 获取表定义、数据位置和分区列表。Hive、Spark SQL、Trino、Flink SQL、Impala 等都可以共享 Metastore。

## 内部表与外部表

- 内部表：Hive 管理数据生命周期，删表通常删除底层数据。
- 外部表：Hive 只管理元数据，删表通常不删除底层数据。

数据湖、ODS 原始层、跨引擎共享数据通常更适合外部表或湖仓表。临时计算结果和受 Hive 管控的中间表可使用内部表。

## 分区设计

分区本质是目录级拆分，常见目录形态为 `dt=2026-06-03/hour=10`。

优势：

- 查询时通过分区裁剪减少扫描数据。
- 便于按时间生命周期管理。
- 便于增量写入、补数和重跑。

常见分区字段：日期、小时、地区、业务线、租户。

常见误区：

- 分区过粗导致每次扫描过多数据。
- 分区过细导致小文件和 Metastore 压力。
- 查询不带分区条件导致全表扫描。
- 对分区字段使用函数导致无法裁剪。

## 分桶设计

分桶是按字段 hash 后写入固定数量文件，用于优化 Join、采样和数据分布。

- 分区解决“读哪些目录”。
- 分桶解决“目录内数据如何组织”。
- 分区字段通常是低基数时间或业务字段。
- 分桶字段通常是 Join key 或高基数字段。

分桶收益依赖上下游一致的分桶字段、bucket 数和执行引擎支持。没有配套查询模式时，分桶会增加写入和维护复杂度。

## 文件格式

- TextFile：简单但性能差，不适合核心数仓表。
- ORC：Hive 生态常用列式格式，支持压缩、索引、谓词下推和统计信息。
- Parquet：Spark、Trino、Flink、Iceberg 常用，生态通用性强。
- Avro：适合 Schema 演进和行式交换，常用于数据交换和 CDC。

## Hive SQL 优化

优化目标是减少扫描数据量、减少 Shuffle、降低小文件和倾斜影响。

关键手段：

- 查询条件必须包含分区字段，保证分区裁剪。
- 避免 `select *`，让列裁剪生效。
- 使用 ORC/Parquet，利用谓词下推和统计信息。
- 小表 Join 大表时使用 Map Join 或 Broadcast Join。
- 大表 Join 大表时关注 Join key 分布和倾斜。
- 控制动态分区数量和 Reducer 数量，避免输出大量小文件。
- 开启 CBO、统计信息和并行执行。

## Metastore 常见问题

- 分区太多导致分区查询和任务提交慢。
- 元数据库连接池不足或慢 SQL 影响所有查询引擎。
- 表结构变更未同步导致上下游失败。
- 多引擎同时写元数据造成一致性问题。
- 权限、Catalog 和表生命周期治理混乱。

## 与湖仓 Catalog 的关系

Iceberg、Hudi、Delta Lake 通常也需要 Catalog 管理表元数据。Hive Metastore 可以作为 Iceberg Catalog 的一种实现，但现代架构也会使用 REST Catalog、Glue、Nessie 等。

湖仓表格式把事务、快照、Schema 演进和分区演进能力前移到表格式层，减少直接操作 Hive 分区目录带来的不一致问题。
