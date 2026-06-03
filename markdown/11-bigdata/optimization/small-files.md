# 小文件治理

小文件会增加 NameNode/Metastore 压力，也会导致计算任务 Split 过多、调度开销高、查询性能下降。

## 产生原因

- 上游并发写入过高，每个并发生成小文件。
- Flink/Spark checkpoint 或滚动策略过频。
- Hive 动态分区过多。
- Kafka 分区过多或批次太小。
- 频繁小批量导入湖仓表。

## 影响

- NameNode 元数据内存压力大。
- 查询需要打开大量文件，IO 开销高。
- Hive/Spark 任务数量过多。
- 湖仓表 manifest/metadata 膨胀。
- ClickHouse/Doris compaction 压力上升。

## 治理方案

- 写入端控制并发和滚动文件大小。
- 定期 compaction 合并小文件。
- Hive 使用 insert overwrite 合并分区。
- Spark 使用 coalesce/repartition 控制输出文件数。
- Iceberg/Hudi 使用表服务合并文件。
- Flink FileSink 配置合理 rolling policy。

## 面试重点

小文件治理要从源头和后处理两端做：源头控制写入并发、批次和滚动策略；后处理通过 compaction、分区合并和生命周期治理降低长期成本。
