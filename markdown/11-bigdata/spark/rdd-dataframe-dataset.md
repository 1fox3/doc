# Spark RDD/DataFrame/Dataset

RDD、DataFrame、Dataset 是 Spark 的三个核心抽象。

## RDD

RDD 是弹性分布式数据集，代表分布在集群中的不可变数据集合。

特点：

- 强类型。
- API 底层，控制力强。
- 支持 lineage 容错。
- 优化器能力弱。

适合：自定义复杂计算、非结构化数据处理、需要底层控制的场景。

## DataFrame

DataFrame 是带 schema 的分布式表。

特点：

- 类似关系型表。
- 支持 Catalyst 优化。
- 支持 Tungsten 执行优化。
- API 更接近 SQL。

适合：结构化 ETL、SQL 分析、数仓计算。

## Dataset

Dataset 在 JVM 语言中提供类型安全，同时具备结构化优化能力。

特点：

- 类型安全。
- 支持编译期检查。
- 相比 DataFrame 编码和对象转换成本可能更高。

## Catalyst 优化器

Catalyst 会进行：

- 解析 SQL。
- 生成逻辑计划。
- 规则优化。
- 成本优化。
- 生成物理计划。

## 选择建议

- 优先使用 Spark SQL/DataFrame。
- 只有在需要底层控制时使用 RDD。
- Dataset 根据团队语言和类型安全需求选择。

## 面试重点

RDD 更底层，DataFrame/Dataset 更结构化且可被优化器优化。Spark SQL 性能通常更好，是因为 Catalyst 和 Tungsten 可以做执行计划和内存布局优化。
