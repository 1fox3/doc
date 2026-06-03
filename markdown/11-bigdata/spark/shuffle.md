# Spark Shuffle

Shuffle 是 Spark 中跨分区、跨节点重分布数据的过程，常见于 groupByKey、reduceByKey、join、distinct、repartition 等操作。

## 为什么产生 Shuffle

- 相同 key 的数据需要汇聚到同一个分区。
- Join 两侧数据需要按 key 重新分布。
- 全局排序或去重需要跨分区协调。

## 执行机制

- Map 端将输出按 Reduce 分区写入本地 Shuffle 文件。
- Reduce 端从多个 Executor 拉取属于自己的数据块。
- 拉取后进行聚合、排序或 Join。

## 性能问题

- 网络 IO 大。
- 磁盘 IO 大。
- 序列化成本高。
- 数据倾斜导致部分 Task 极慢。
- 分区数不合理导致小任务过多或单任务过大。

## 优化策略

- 优先使用 reduceByKey/aggregateByKey，避免 groupByKey。
- Join 小表时使用 Broadcast Join。
- 合理设置 `spark.sql.shuffle.partitions`。
- 开启 AQE，让 Spark 自动合并小分区、处理倾斜 Join。
- 对热点 key 做打散或单独处理。
- 使用 Kryo 序列化和高效列式格式。

## 数据倾斜处理

- 过滤异常 key。
- 热点 key 单独计算。
- 随机前缀打散，两阶段聚合。
- Broadcast Join 替代 Shuffle Join。
- AQE skew join 自动优化。

## 面试重点

回答 Spark Shuffle 时，要讲清“为什么产生、怎么写、怎么拉、为什么慢、如何优化”。不要只背宽依赖和窄依赖定义。
