# Mapping 与数据建模

## Mapping 的作用

Mapping 定义字段类型、分析器、索引方式、doc values、动态字段策略和对象结构。Mapping 决定了能否搜索、如何分词、是否能排序聚合以及索引成本。

字段类型一旦创建后通常不能直接修改。需要变更字段类型时，应新建索引并 reindex。

## 常用字段类型

- `keyword`：精确匹配、过滤、排序、聚合、ID、状态码、标签。
- `text`：全文检索，会经过 analyzer 分词。
- `long`、`double`、`scaled_float`：数值过滤、排序、聚合。
- `date`：时间范围查询、时间序列索引、ILM rollover。
- `boolean`：布尔过滤。
- `ip`：IP 查询和聚合。
- `object`：普通 JSON 对象，会被扁平化索引。
- `nested`：数组对象需要保持对象内部字段关系时使用。
- `join`：父子关系，适合少量强约束场景，查询成本高。
- `dense_vector`：向量检索或混合检索场景。

## Text 与 Keyword

`text` 用于全文搜索，适合 `match`、`multi_match`、短语查询和相关性评分。`keyword` 用于精确值，适合 `term`、`terms`、聚合和排序。

常见建模方式：

```json
{
  "title": {
    "type": "text",
    "analyzer": "ik_max_word",
    "search_analyzer": "ik_smart",
    "fields": {
      "keyword": { "type": "keyword", "ignore_above": 256 }
    }
  }
}
```

## 动态字段

动态 mapping 能降低接入成本，但容易引入字段爆炸、类型误判和 mapping 冲突。

生产建议：

- 关键索引使用显式 mapping。
- 对日志类动态字段设置 `dynamic_templates`。
- 限制字段数量，例如 `index.mapping.total_fields.limit`。
- 对未知对象可使用 `flattened`，避免无限展开字段。

## 文档建模方式

- 扁平结构：查询简单、性能最好，适合大多数场景。
- 反范式冗余：将搜索所需字段冗余到同一文档，换取查询性能。
- nested：适合对象数组中字段必须成组匹配的场景。
- join：适合父子生命周期差异大且不适合冗余的场景，但性能和路由要求更复杂。

Elasticsearch 不擅长跨文档 join。搜索系统建模通常优先反范式，而不是照搬关系型数据库模型。

## Routing

默认路由根据 `_id` 计算目标主分片。自定义 routing 可以让相关文档落到同一分片，减少查询 fan-out 或满足 join 约束。

使用 routing 的风险：

- routing 值分布不均会造成热点分片。
- 查询时忘记带 routing 会查所有分片。
- routing 设计错误后很难无损调整，通常需要重建索引。

## 别名与零停机重建

索引别名用于隐藏物理索引名，支持读写切换和灰度重建。

典型流程：

- 创建新索引 `products_v2`。
- 使用 `_reindex` 或应用双写导入数据。
- 校验文档数、查询结果和性能。
- 原子切换 alias，将 `products_write` 指向新索引。
- 保留旧索引一段时间用于回滚。

## 时间序列建模

日志、指标、行为流水适合按时间滚动索引，并配合 ILM 管理生命周期。

常见策略：

- 使用 data stream 或索引别名加 rollover。
- 根据单分片大小控制 rollover 条件，例如 30 GB 到 50 GB。
- 热阶段写入，温阶段降低副本或迁移节点，冷阶段压缩或 searchable snapshot，最终删除。

## 建模反模式

- 在 `text` 字段上排序或聚合。
- 一个索引混入大量无关业务类型。
- 单文档过大，导致写入、网络传输和 fetch 慢。
- nested 对象数量过多，放大内部 Lucene 文档数量。
- 分片数按天固定过大，形成海量小分片。
