# Optimizer Trace

## 作用

- `optimizer_trace` 用于观察优化器如何生成候选计划、估算成本并选择最终执行计划。
- 它适合排查“为什么没有走某个索引”“为什么选择这个连接顺序”“为什么使用全表扫描”。

## 使用方式

```sql
SET optimizer_trace = 'enabled=on';
SET optimizer_trace_max_mem_size = 1048576;

SELECT * FROM t WHERE a = 1 AND b > 10;

SELECT trace
FROM information_schema.optimizer_trace\G

SET optimizer_trace = 'enabled=off';
```

## 关注内容

- `join_preparation`：SQL 解析、视图展开、子查询准备。
- `join_optimization`：条件处理、访问路径评估、索引选择、连接顺序选择。
- `rows_estimation`：扫描行数和过滤率估算。
- `considered_execution_plans`：候选计划及其成本。

## 实践要点

- Trace 内容较大，线上只应在单会话短时间开启。
- 结合 `EXPLAIN FORMAT=JSON` 一起看，前者解释选择过程，后者展示最终计划。
- 如果优化器估算明显偏差，优先检查统计信息、数据倾斜、直方图和条件是否可索引。

## 典型排查问题

- 预期索引没有被选择：查看 `range_analysis` 中各索引的扫描区间、估算行数和成本。
- 连接顺序异常：查看 `considered_execution_plans` 中不同 join order 的累积成本。
- 子查询性能差：查看子查询是否被半连接、物化或保持相关执行。
- 排序代价高：查看优化器是否评估过可用于排序的索引，以及为什么放弃。

## 使用注意

- `optimizer_trace` 是会话级开关，不要全局长期开启。
- 对包含敏感 SQL 的环境，trace 可能记录原始语句和条件值，需要注意权限和留存。
- 如果 trace 被截断，调大 `optimizer_trace_max_mem_size` 后重新执行目标 SQL。

## 建议输出流程

```sql
SET optimizer_trace = 'enabled=on';
EXPLAIN FORMAT=JSON SELECT * FROM t WHERE a = 1 ORDER BY b LIMIT 10;
SELECT trace FROM information_schema.optimizer_trace\G
SET optimizer_trace = 'enabled=off';
```
