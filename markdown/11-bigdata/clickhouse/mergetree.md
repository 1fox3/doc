# MergeTree

MergeTree 是 ClickHouse 最重要的表引擎家族，负责列式存储、分区、排序、索引和后台合并。

## 核心结构

- Partition：按分区表达式拆分数据。
- Part：一次写入生成一个或多个数据片段。
- Mark：稀疏索引标记，定位数据块。
- ORDER BY：决定数据在 Part 内的排序方式。
- Primary Key：用于构建稀疏索引，通常与 ORDER BY 相同或是其前缀。

## 写入机制

- 数据批量写入形成 Part。
- Part 内按 ORDER BY 排序。
- 后台 Merge 任务合并多个小 Part。
- 过多小 Part 会影响查询和合并性能。

## 分区键设计

- 常用日期分区，例如 `toYYYYMM(dt)` 或 `toDate(event_time)`。
- 分区不宜过细，否则 Part 数量暴增。
- 查询条件应尽量带分区字段。

## 排序键设计

- 优先放高频过滤字段。
- 再放常用聚合维度。
- 低基数字段放前面通常有利于压缩和过滤。
- 排序键不是唯一约束，不要当 MySQL 主键理解。

## 常见表引擎

- MergeTree：基础引擎。
- ReplacingMergeTree：按版本或最终合并去重，适合 CDC 明细去重。
- SummingMergeTree：按排序键聚合数值列。
- AggregatingMergeTree：存储聚合状态，适合预聚合。
- CollapsingMergeTree：通过 sign 字段折叠数据。

## 面试重点

ClickHouse 快不是因为“有索引”这么简单，而是分区裁剪、排序键、稀疏索引、列式压缩、向量化执行和后台合并共同作用。
