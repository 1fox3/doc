# Hive SQL 优化

Hive SQL 优化目标是减少扫描数据量、减少 Shuffle、降低小文件和数据倾斜影响。

## 分区裁剪

- 查询条件必须带上分区字段。
- 避免对分区字段使用函数导致无法裁剪。
- 常见分区字段：dt、hour、region、biz_type。

## 列裁剪和谓词下推

- 使用 ORC/Parquet 等列式格式，只读取需要的列。
- where 条件尽量提前过滤。
- 避免 `select *`。

## Join 优化

- Map Join：小表加载到内存，大表 Map 端直接 Join，避免 Reduce Shuffle。
- Bucket Join：两表按 Join key 分桶，减少 Shuffle。
- Sort Merge Bucket Join：分桶且排序后可高效 Join。
- 大表 Join 大表：关注 key 分布和倾斜。

## 数据倾斜

- 现象：少数 Reduce 执行极慢。
- 原因：热点 key、空值 key、业务分布不均。
- 解决：热点 key 单独处理、随机前缀打散、两阶段聚合、过滤无效 key。

## 小文件治理

- 小文件会增加 NameNode 压力和任务启动开销。
- 写入阶段控制 Reducer 数量。
- 定期 compaction 或 insert overwrite 合并。
- 使用 ORC/Parquet 并设置合理文件大小。

## 参数方向

- 开启并行执行。
- 开启 CBO 成本优化。
- 配置自动 Map Join 阈值。
- 配置输出文件合并。

## 面试回答模板

Hive SQL 慢时，我会先看执行计划，确认是否命中分区裁剪和列裁剪；再看 Join 是否产生大 Shuffle；然后检查是否有数据倾斜和小文件；最后结合 ORC/Parquet、Map Join、两阶段聚合和文件合并进行优化。
