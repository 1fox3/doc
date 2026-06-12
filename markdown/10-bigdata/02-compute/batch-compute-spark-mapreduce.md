# 批计算：MapReduce 与 Spark

批计算用于处理有边界的大规模数据，常见场景包括离线 ETL、T+1 报表、历史重算、宽表构建、模型特征加工和大规模数据修复。

## MapReduce 模型

MapReduce 将计算拆成 Map、Shuffle、Reduce 三个核心阶段。

执行流程：

1. InputFormat 将输入数据切分为 Split。
2. MapTask 读取 Split 并输出 key-value。
3. Map 端按分区、排序、溢写生成中间文件。
4. Reduce 端拉取各 Map 输出，这一步称为 Shuffle。
5. Reduce 按 key 聚合处理并输出结果。

MapReduce 原生 API 已较少直接编写，但它的分区、排序、Shuffle 和容错思想仍是理解 Hive、Spark 的基础。

## MapReduce Shuffle

- Partition：决定 key 进入哪个 Reduce。
- Sort：Map 端和 Reduce 端都会按 key 排序。
- Spill：Map 输出缓冲区达到阈值后溢写磁盘。
- Merge：多个溢写文件合并。
- Fetch：Reduce 从多个 Map 节点拉取数据。

性能瓶颈通常来自网络 IO、磁盘 IO、Reduce 数据倾斜、小文件和序列化成本。

## Spark 定位

Spark 是通用大数据计算引擎，适合批处理、交互式分析、机器学习和部分流式处理场景。相比 MapReduce，Spark 能将中间计算保存在内存或更高效的 Shuffle 文件中，并通过 DAG 优化减少不必要的阶段。

核心角色：

- Driver：运行用户程序，生成 DAG，调度任务。
- Executor：执行 Task，缓存数据，返回结果。
- DAG：由依赖关系构成的有向无环图。
- Stage：遇到宽依赖 Shuffle 时切分 Stage。
- Task：最小执行单元，对应一个分区上的计算。

## RDD、DataFrame、Dataset

- RDD：底层弹性分布式数据集，控制力强，支持 lineage 容错，但优化器能力弱。
- DataFrame：带 Schema 的分布式表，支持 Catalyst 和 Tungsten 优化，适合结构化 ETL 和 SQL 分析。
- Dataset：在 JVM 语言中提供类型安全，同时具备结构化优化能力，但对象编码和转换可能带来额外成本。

生产中通常优先使用 Spark SQL/DataFrame，只有在需要底层控制或处理特殊非结构化逻辑时使用 RDD。

## Spark 执行流程

1. 用户代码或 SQL 构建逻辑计划。
2. Catalyst 进行解析、规则优化、成本优化和物理计划生成。
3. DAGScheduler 根据宽依赖切分 Stage。
4. TaskScheduler 将 Task 分发到 Executor。
5. Executor 执行计算、读写 Shuffle、缓存数据并返回结果。

## Spark Shuffle

Shuffle 是跨分区、跨节点重分布数据的过程，常见于 `groupByKey`、`reduceByKey`、`join`、`distinct`、`repartition`、全局排序等操作。

产生原因：

- 相同 key 的数据需要汇聚到同一分区。
- Join 两侧数据需要按 key 重新分布。
- 全局排序或去重需要跨分区协调。

优化策略：

- 优先使用 `reduceByKey`、`aggregateByKey`，避免 `groupByKey` 拉取全量 value。
- Join 小表时使用 Broadcast Join。
- 合理设置 `spark.sql.shuffle.partitions`。
- 开启 AQE，让 Spark 自动合并小分区、处理倾斜 Join。
- 对热点 key 做打散、预聚合或单独处理。
- 使用高效列式格式、压缩和 Kryo 序列化。

## Spark 内存与 OOM

Spark OOM 通常与数据倾斜、缓存过大、Shuffle、并发任务数、对象膨胀和 Driver 拉取大数据有关。

内存区域：

- Execution Memory：Shuffle、Join、Sort、Aggregation 使用。
- Storage Memory：Cache/Persist 使用。
- User Memory：用户对象、UDF、临时数据结构。
- Reserved Memory：系统保留。

常见 OOM 场景：

- 单个分区数据过大。
- `collect` 或 `toPandas` 把大量数据拉回 Driver。
- 广播表过大。
- 缓存大表且未释放。
- UDF 创建大量对象。
- Join 或聚合发生严重数据倾斜。

排查步骤：

1. 判断是 Driver OOM 还是 Executor OOM。
2. 查看 Spark UI 中失败的 Stage 和 Task。
3. 检查是否少数 Task 输入数据量或 Shuffle Read 明显偏大。
4. 检查代码中的 `collect`、`cache`、`join`、`groupByKey`、UDF 等高风险操作。
5. 结合 Executor 日志确认具体内存区域和异常栈。

## 批计算工程实践

- 表扫描必须尽量命中分区裁剪和列裁剪。
- 大 Join 前先过滤、投影和预聚合。
- 输出文件大小要可控，避免一个任务产出过多小文件。
- 重要离线任务要支持幂等重跑和分区级回滚。
- 对核心任务记录输入分区、输出行数、扫描量、耗时和资源使用。
- 对历史重算和补数任务设置资源队列和限流，避免冲垮在线数据服务。
