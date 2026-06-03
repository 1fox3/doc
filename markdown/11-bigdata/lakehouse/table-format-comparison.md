# 湖仓选型对比

湖仓表格式用于让 HDFS/对象存储上的文件具备表管理、事务、快照和多引擎访问能力。

## Iceberg

优势：

- 表格式开放，设计清晰。
- 多引擎兼容好。
- Snapshot、Schema Evolution、Partition Evolution 能力强。
- 隐藏分区降低使用复杂度。

适合：多引擎数据湖、长期数据资产、复杂表演进。

## Hudi

优势：

- Upsert 能力强。
- 增量查询成熟。
- 适合 CDC 入湖。
- 表服务能力丰富。

适合：近实时入湖、更新删除多、增量消费链路。

## Delta Lake

优势：

- Databricks/Spark 生态强。
- ACID、Schema Enforcement、Time Travel 成熟。
- 与 Spark 集成体验好。

适合：Databricks 生态或 Spark 为主的数据湖。

## 选型维度

- 是否高频 upsert。
- 是否需要多引擎读写。
- 是否需要增量消费。
- 是否依赖 Spark/Trino/Flink。
- Catalog 和权限生态。
- 团队运维经验。

## 面试重点

湖仓表格式解决的是文件湖缺少事务、元数据、快照、演进和多引擎一致性的问题。Iceberg、Hudi、Delta Lake 的差异主要在 upsert、增量、开放性和生态集成。
