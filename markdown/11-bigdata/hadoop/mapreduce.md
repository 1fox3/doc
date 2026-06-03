# MapReduce

MapReduce 是经典离线批处理模型，将计算拆成 Map、Shuffle、Reduce 三个核心阶段。

## 执行流程

1. InputFormat 将输入数据切分为 Split。
2. MapTask 读取 Split 并输出 key-value。
3. Map 端按分区、排序、溢写生成中间文件。
4. Reduce 端拉取各 Map 输出，这一步称为 Shuffle。
5. Reduce 按 key 聚合处理并输出结果。

## Shuffle 机制

- Partition：决定 key 进入哪个 Reduce。
- Sort：Map 端和 Reduce 端都会按 key 排序。
- Spill：Map 输出缓冲区达到阈值后溢写磁盘。
- Merge：多个溢写文件合并。
- Fetch：Reduce 从多个 Map 节点拉取数据。

## 性能瓶颈

- Shuffle 大量网络和磁盘 IO。
- Reduce 数据倾斜导致少数任务拖慢整体作业。
- 小文件导致 Split 过多，任务启动开销大。
- 序列化和压缩配置不合理。

## 优化手段

- 使用 Combiner 减少 Map 输出。
- 合理设置 Reduce 数量。
- 对倾斜 key 做打散、预聚合或单独处理。
- 启用中间结果压缩。
- 使用 CombineInputFormat 合并小文件。

## 当前定位

MapReduce 原生 API 已较少直接编写，但它的 Shuffle、分区、排序、容错思想仍是理解 Hive、Spark 的基础。
