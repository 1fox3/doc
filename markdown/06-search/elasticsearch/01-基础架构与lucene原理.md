# 基础架构与 Lucene 原理

## Elasticsearch 是什么

Elasticsearch 是构建在 Apache Lucene 之上的分布式搜索与分析引擎。Lucene 负责单机索引和检索能力，Elasticsearch 在其上提供 REST API、分片副本、集群管理、近实时搜索、聚合分析、安全和生态集成。

典型使用场景包括商品搜索、站内搜索、日志检索、指标分析、风控查询、可观测性平台和知识库检索。

## 基础概念

- index：逻辑索引，类似一类文档的集合。
- document：写入和检索的最小 JSON 数据单元。
- field：文档字段，不同字段可有不同 mapping 和 analyzer。
- shard：Lucene 索引实例，分为 primary shard 和 replica shard。
- segment：Lucene 的不可变索引段，新增文档会产生新段，后台 merge 合并旧段。
- term：索引和检索的词项单位。
- token：分析过程中的词条，包含文本、位置、偏移量等信息。

Elasticsearch 7 移除了多 type 设计，8.x 中 `_type` 已不再作为建模方式。旧资料中的 `_uid = _type#_id` 属于历史实现，现代版本主要关注 `_id`、`_source`、`_seq_no`、`_primary_term` 等元数据。

## 倒排索引

倒排索引将 term 映射到包含该 term 的文档列表，并可记录词频、位置、偏移量等信息。它适合快速回答“哪些文档包含这个词”。

全文搜索通常依赖倒排索引；排序、聚合和脚本访问字段值更多依赖 doc values。

## Doc Values

Doc values 是面向列的磁盘数据结构，按字段存储每个文档的值。它主要服务排序、聚合和脚本访问。

使用建议：

- 对需要排序和聚合的字段使用 `keyword`、数值、日期、布尔等支持 doc values 的类型。
- 不要在 `text` 字段上直接聚合，除非明确启用 fielddata 并能承受堆内存压力。
- 多字段建模常用 `name` 作为 `text` 搜索，`name.keyword` 作为精确匹配、排序和聚合。

## Segment 与不可变性

Lucene segment 写入后不可变。新增文档写入新 segment，删除和更新不会原地修改旧 segment，而是记录删除标记并写入新版本文档。

这种设计带来的结果：

- 搜索可并发读取不可变 segment，减少锁开销。
- 更新本质上是删除旧文档再新增新文档。
- 删除空间不会立即释放，需要后台 merge 后回收。
- segment 过多会增加搜索开销，merge 会消耗 IO 和 CPU。

## Norms 与词项向量

norms 存储字段长度等归一化信息，用于相关性评分。对不需要评分的字段可以关闭 norms，减少存储。

term vectors 是面向单文档的词项信息，可用于高亮、相似文档、调试分析，但会增加索引体积，默认不应随意开启。

## 近实时搜索

Elasticsearch 写入成功后并不立即对搜索可见。文档先进入内存 buffer 和 translog，`refresh` 后生成可搜索 segment，默认 `refresh_interval` 通常为 1 秒。

近实时意味着：

- `GET /index/_doc/id` 可实时读取最新版本。
- `_search` 只能看到最近一次 refresh 后的内容。
- 强制 `refresh=true` 会降低写入吞吐，批量写入场景应谨慎使用。

## 版本边界

- Zen Discovery 是 7 之前的发现和选举机制；7+ 使用新的集群协调子系统，配置重点变为 `discovery.seed_hosts` 和 `cluster.initial_master_nodes`。
- Tribe node 已废弃，跨集群查询使用 Cross Cluster Search。
- River 已废弃，数据接入主要使用 Beats、Logstash、Ingest Pipeline、Connector、应用写入或 CDC。
- Elasticsearch 8.x 默认启用安全能力，生产环境需要规划 TLS、用户、角色和 API key。
