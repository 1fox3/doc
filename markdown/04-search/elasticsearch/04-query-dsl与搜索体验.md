# Query DSL 与搜索体验

## Query 与 Filter

Query context 会计算 `_score`，适合全文检索和相关性排序。Filter context 不计算分数，适合结构化过滤，通常更容易缓存。

设计查询时应把必须精确过滤的条件放到 `filter`，把需要评分的条件放到 `must` 或 `should`。

## Bool Query

`bool` 是最常用的组合查询。

- `must`：必须匹配，参与评分。
- `filter`：必须匹配，不参与评分。
- `should`：可选匹配，可提升分数，也可通过 `minimum_should_match` 控制至少命中数量。
- `must_not`：必须不匹配，不参与评分。

## 常见查询

- `term`：精确词项查询，适合 `keyword`、数值、布尔、日期。
- `terms`：多个精确值。
- `range`：范围查询。
- `exists`：字段存在性。
- `match`：全文查询，会分析输入文本。
- `match_phrase`：短语查询，考虑位置顺序。
- `multi_match`：多字段全文查询。
- `prefix`、`wildcard`、`regexp`：模式匹配，可能成本较高。

## Multi Match

`multi_match` 常用于一个关键词查多个字段。

- `best_fields`：取最佳字段匹配，适合标题和正文择优。
- `most_fields`：多个字段得分叠加，适合同一文本多 analyzer。
- `cross_fields`：把多个字段视作一个整体，适合姓名、地址等字段拆分。
- `phrase`：多字段短语匹配。
- `phrase_prefix`：短语前缀匹配，常用于输入联想但要控制开销。

字段 boost 应基于评估数据调整，例如 `title^3`、`brand^2`，不要只凭感觉无限放大。

## 分页

浅分页使用 `from + size` 即可。深分页昂贵，因为每个分片都要返回 `from + size` 的候选集，协调节点再全局排序并丢弃前 `from` 条。

深分页方案：

- `search_after`：适合实时向后翻页，需要稳定排序字段。
- PIT：Point In Time，配合 `search_after` 保持一致视图。
- scroll：适合后台批处理导出，不适合用户实时翻页。
- composite aggregation：适合聚合桶的分页。

## 搜索过程

一次分布式搜索通常包含 query 和 fetch 两个阶段。

- Query 阶段：协调节点把请求发到相关分片，每个分片返回 top doc ID 和排序值。
- Fetch 阶段：协调节点确定全局 top N 后，到对应分片拉取 `_source` 或 stored fields。

这也是深分页昂贵的原因：query 阶段候选集会随 `from` 增大而放大。

## 查询模板

Mustache search template 可将 DSL 参数化，适合固定查询结构和动态参数组合。复杂业务不要把所有逻辑塞进模板，应保持应用层可测试和可观测。

## 脚本查询

Painless 是默认脚本语言。脚本可用于排序、过滤、评分和字段计算，但会增加 CPU 成本。

使用建议：

- 优先通过索引时预计算字段替代查询时脚本。
- 避免在大结果集上执行 `script_score`。
- 参数使用 `params`，避免动态拼接脚本导致编译缓存失效。

## 结果质量评估

搜索体验不能只看单次查询效果，应建立评估闭环：

- 离线标注集：计算 NDCG、MRR、Precision、Recall。
- 在线指标：点击率、转化率、零结果率、首屏满意度。
- 查询日志：分析无结果词、低点击词、拼写错误、同义词缺失。
- A/B 实验：验证 analyzer、boost、排序特征和重排策略。
