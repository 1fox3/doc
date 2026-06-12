# EXPLAIN详解

## 核心字段

- `id` 表示查询块执行层级，复杂查询中用于区分子查询和派生表。
- `select_type` 表示查询类型，例如 `SIMPLE`、`PRIMARY`、`SUBQUERY`、`DERIVED`。
- `table` 表示当前访问的表或派生表。
- `type` 表示访问方法，例如 `const`、`ref`、`range`、`index`、`ALL`。
- `possible_keys` 是候选索引，`key` 是最终选择索引，`key_len` 是使用到的索引长度。
- `rows` 是预计扫描行数，`filtered` 是预计过滤比例。
- `Extra` 展示额外操作，如 `Using index`、`Using where`、`Using filesort`、`Using temporary`。

## 常见 Extra

- `Using index`：覆盖索引，不需要回表。
- `Using index condition`：索引下推，先在存储引擎层过滤可用索引列。
- `Using filesort`：无法完全利用索引顺序，需要额外排序。
- `Using temporary`：需要临时表处理分组、去重或排序。
- `Using where`：服务层或引擎层还需要应用过滤条件。

## 推荐用法

```sql
EXPLAIN SELECT * FROM t WHERE a = 1 ORDER BY b LIMIT 10;
EXPLAIN FORMAT=JSON SELECT * FROM t WHERE a = 1 ORDER BY b LIMIT 10;
EXPLAIN ANALYZE SELECT * FROM t WHERE a = 1 ORDER BY b LIMIT 10;
```

## 实践要点

- `EXPLAIN` 是估算计划，MySQL 8.0 可用 `EXPLAIN ANALYZE` 查看实际执行耗时和行数。
- 看到 `Using filesort` 不一定有问题，关键看排序数据量、是否有 LIMIT、是否可用索引顺序优化。
- 看到命中索引也不代表快，需要结合扫描行数、回表次数和排序/临时表成本判断。

## 分析顺序

- 先看表访问顺序，确认驱动表是否能被有效过滤。
- 再看每张表的 `type`、`key`、`rows`，判断访问方法和扫描规模。
- 看 `Extra` 是否出现 `Using temporary`、`Using filesort`、`Using join buffer`。
- 对比 `possible_keys` 和 `key`，判断优化器为什么没选预期索引。
- 使用 `FORMAT=JSON` 查看成本、过滤条件和嵌套循环结构。

## `key_len` 的意义

- `key_len` 表示优化器决定使用的索引字节长度，可反推联合索引用到了哪些前缀列。
- 变长字段、字符集、NULL 标记都会影响 `key_len`。
- `key_len` 不是越长越好，关键是是否覆盖了有效过滤列。

## `EXPLAIN ANALYZE` 注意事项

- 它会真实执行 SQL，线上对写 SQL 或大查询要谨慎。
- 它能展示实际行数和耗时，有助于发现统计信息估算偏差。
- 分析后应结合慢日志中的 `Rows_examined`、`Rows_sent` 和执行耗时判断收益。
