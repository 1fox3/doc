# 湖仓表格式：Iceberg、Hudi 与 Delta Lake

湖仓表格式用于让 HDFS 或对象存储上的文件具备表管理、事务、快照、Schema 演进、分区演进和多引擎访问能力。

## 为什么需要湖仓表格式

直接用 Hive 外部表管理数据湖会遇到这些问题：

- 文件级事务能力弱，任务失败容易留下脏文件。
- 分区目录和 Metastore 元数据容易不一致。
- Schema 变更和分区演进困难。
- 多引擎并发读写缺少统一隔离语义。
- 小文件和文件级统计信息治理能力不足。
- 无法方便支持时间旅行、回滚和增量消费。

湖仓表格式通过元数据层和快照机制，让文件湖具备接近数据仓库表的管理能力。

## Iceberg

Iceberg 是开放湖仓表格式，强调开放标准、多引擎兼容、快照、Schema 演进和分区演进。

核心能力：

- ACID 事务：通过快照提交保证原子性。
- Snapshot：每次提交生成新快照，支持时间旅行和回滚。
- Schema Evolution：支持字段新增、删除、重命名和类型演进。
- Partition Evolution：支持分区策略演进，不需要重写全表。
- Hidden Partition：查询无需显式感知物理分区字段。

元数据结构：

- Catalog：管理表位置和当前元数据指针。
- Metadata File：记录表 schema、分区、快照等。
- Manifest List：记录本次快照涉及的 manifest。
- Manifest File：记录数据文件和统计信息。
- Data File：真实 Parquet、ORC 或 Avro 数据文件。

适合场景：

- 多引擎共享数据湖，Spark、Flink、Trino、Hive 共同访问。
- 大规模离线和近实时数仓。
- 长期数据资产需要 schema 和分区演进。
- 需要时间旅行、回滚和快照隔离的场景。

## Hudi

Hudi 重点解决数据湖中的 upsert、增量消费、近实时入湖和小文件管理问题。

表类型：

- Copy On Write：写入时生成新的列式文件，读性能好，写放大较高。
- Merge On Read：增量写入 log 文件，读时合并 base file 和 log，写入延迟低。

核心概念：

- Record Key：记录唯一键。
- Precombine Field：同一 key 多条记录时选择最新记录。
- Partition Path：分区路径。
- Timeline：记录 commit、clean、compaction 等操作。
- Index：定位记录所在文件，支持 upsert。

写入模式：

- Insert：只新增。
- Upsert：按主键更新或插入。
- Bulk Insert：大批量初始化导入。
- Delete：删除记录。

适合场景：

- CDC 入湖。
- 需要增量查询的离线或准实时链路。
- 用户画像、订单状态、维表快照。
- 需要处理更新和删除的数据湖。

## Delta Lake

Delta Lake 在 Databricks 和 Spark 生态中成熟，强调 ACID、Schema Enforcement、Time Travel 和 Spark 集成体验。

适合场景：

- Databricks 生态。
- Spark 为主的数据湖。
- 需要事务、时间旅行和较好开发体验的湖仓链路。

## Iceberg、Hudi、Delta Lake 对比

| 维度 | Iceberg | Hudi | Delta Lake |
| --- | --- | --- | --- |
| 核心优势 | 开放、多引擎、快照、演进 | Upsert、增量、近实时入湖 | Spark/Databricks 生态 |
| 更新能力 | 支持，取决于引擎实现 | 强 | 强 |
| 增量消费 | 支持，生态持续完善 | 成熟 | 支持 |
| 分区演进 | 强 | 一般 | 一般 |
| 多引擎兼容 | 强 | 较强 | 取决于生态和版本 |
| 典型场景 | 长期湖仓、多引擎共享 | CDC 入湖、频繁更新 | Spark 主导的数据湖 |

## 表服务与优化

湖仓表长期运行后需要表服务治理：

- Compaction：合并小文件，降低读放大。
- Clustering：按查询字段重排文件，提升裁剪和压缩效果。
- Snapshot Expiration：清理过旧快照，控制元数据成本。
- Orphan File Cleanup：清理失败任务遗留文件。
- Manifest Rewrite：合并或重写元数据文件，减少规划开销。

## 选型维度

- 是否高频 upsert 和 delete。
- 是否需要多引擎读写。
- 是否需要增量消费。
- 查询引擎主要是 Spark、Flink、Trino 还是 Hive。
- Catalog、权限和数据治理生态是否成熟。
- 团队对表服务、Compaction、升级和故障恢复的运维经验。

## 工程实践

- 不要把湖仓表格式当成计算引擎，它只管理表和文件元数据。
- 关键表要设计主键、分区、文件大小、写入并发和 compaction 策略。
- 流式写入要关注小文件、提交频率和 Checkpoint 间隔。
- 多引擎同时写同一张表前，要确认隔离语义和兼容矩阵。
- 表快照和元数据也有成本，需要生命周期治理。
