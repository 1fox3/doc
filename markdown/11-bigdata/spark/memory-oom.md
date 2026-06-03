# Spark 内存与 OOM

Spark OOM 是生产中高频问题，通常与数据倾斜、缓存过大、Shuffle、并发任务数和对象膨胀有关。

## 内存区域

- Execution Memory：Shuffle、Join、Sort、Aggregation 使用。
- Storage Memory：Cache/Persist 使用。
- User Memory：用户对象、UDF、数据结构。
- Reserved Memory：系统保留。

## 常见 OOM 场景

- 单个分区数据过大。
- groupByKey 拉取全量 value。
- collect 把大数据拉回 Driver。
- 广播表过大。
- cache 大表且未释放。
- UDF 创建大量对象。
- 数据倾斜导致少数 Task 内存爆掉。

## Driver OOM

常见原因：

- collect/toPandas 大量数据。
- 任务元数据过多。
- 分区数或文件数过多。
- 广播变量过大。

## Executor OOM

常见原因：

- Shuffle 分区过大。
- Join/Aggregation 内存不足。
- 缓存过多。
- 数据倾斜。

## 排查步骤

1. 看 Spark UI 失败 Task 和 Stage。
2. 看是否集中在少数 Task。
3. 看 Shuffle Read/Write 和输入记录数。
4. 看 Driver/Executor 日志。
5. 检查 collect、cache、join、groupByKey 等高危操作。

## 优化方式

- 增加分区数，降低单分区大小。
- 使用 reduceByKey 替代 groupByKey。
- 开启 AQE 和 skew join。
- 小表广播，大表避免全量 shuffle。
- 控制 cache，并及时 unpersist。
- 避免 collect 大数据。

## 面试重点

Spark OOM 不应只回答“加内存”。正确思路是判断 Driver 还是 Executor，定位具体 Stage 和 Task，再结合分区大小、Shuffle、Join、缓存和数据倾斜处理。
