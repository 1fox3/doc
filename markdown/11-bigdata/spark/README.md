# Spark

Spark 是通用大数据计算引擎，适合批处理、交互式分析、机器学习和部分流式处理场景。

## 核心概念

- Driver：运行用户程序，生成 DAG，调度任务。
- Executor：执行 Task，缓存数据，返回结果。
- RDD：弹性分布式数据集，Spark 的底层抽象。
- DataFrame/Dataset：结构化 API，支持 Catalyst 优化。
- DAG：由依赖关系构成的有向无环图。
- Stage：遇到宽依赖 Shuffle 时切分 Stage。
- Task：最小执行单元，对应分区上的计算。

## RDD、DataFrame、Dataset

- RDD：类型灵活，控制力强，优化能力弱。
- DataFrame：结构化数据，优化器可优化，性能通常更好。
- Dataset：类型安全，兼顾结构化优化和强类型能力。

## 执行流程

1. 用户代码构建逻辑计划。
2. Catalyst 优化生成物理计划。
3. DAGScheduler 切分 Stage。
4. TaskScheduler 分发 Task 到 Executor。
5. Executor 执行并返回结果。

## 重点能力

- Spark SQL 优化。
- Shuffle 调优。
- Cache/Persist/Checkpoint。
- 广播变量和累加器。
- AQE 自适应执行。

## 常见面试问题

- 宽依赖和窄依赖区别。
- Spark 为什么比 MapReduce 快？
- Shuffle 过程和优化方式。
- Cache、Persist、Checkpoint 区别。
- Spark OOM 如何排查？

## 相关文档

- [Spark Shuffle](shuffle.md)
