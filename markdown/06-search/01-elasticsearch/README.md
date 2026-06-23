# Elasticsearch

Elasticsearch 是基于 Lucene 的分布式搜索与分析引擎，核心能力来自倒排索引、列式 doc values、分片副本、近实时刷新、相关性评分和聚合分析。它适合全文检索、日志分析、指标检索、商品搜索、风控查询和轻量向量/混合检索，但不适合作为强事务数据库。

## 核心脉络

- Lucene 基础：倒排索引、term、token、segment、doc values、norms、merge。
- 数据建模：mapping、text/keyword、nested、join、反范式、时间序列索引。
- 查询体验：Query DSL、bool、filter、BM25、function score、suggest、同义词。
- 写入链路：routing、primary/replica、refresh、flush、translog、segment merge。
- 分布式架构：节点角色、主节点选举、分片分配、集群状态、跨集群搜索。
- 性能运维：分片规划、bulk、缓存、断路器、慢查询、ILM、快照恢复。

## 章节目录

- [基础架构与 Lucene 原理](01-基础架构与lucene原理.md)
- [Mapping 与数据建模](02-mapping与数据建模.md)
- [分析器与相关性](03-分析器与相关性.md)
- [Query DSL 与搜索体验](04-query-dsl与搜索体验.md)
- [写入链路与一致性](05-写入链路与一致性.md)
- [分布式集群与高可用](06-分布式集群与高可用.md)
- [聚合分析与数据管道](07-聚合分析与数据管道.md)
- [性能优化与运维管理](08-性能优化与运维管理.md)
- [面试重点](09-面试重点.md)
- [排障案例](10-排障案例.md)

## 实践检查

- 能解释 `text` 和 `keyword` 的区别，并能为搜索、排序、聚合分别设计字段。
- 能说明为什么 Elasticsearch 是近实时搜索，以及 `refresh`、`flush`、`translog` 的关系。
- 能解释深分页为什么昂贵，并根据场景选择 `search_after`、PIT、scroll。
- 能针对写多、读多、聚合多场景分别调整分片数、refresh interval、bulk、routing 和缓存。
- 能通过 `_cat`、`_cluster/health`、`_nodes/hot_threads`、profile、slow log 和 task API 定位问题。
