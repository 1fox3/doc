# Elasticsearch

> 来源：ES.xmind, 面试内容汇总/ES.xmind

## 核心认知

- Elasticsearch 的核心是倒排索引、分片副本、近实时搜索和 Lucene 段文件。
- 搜索质量依赖 mapping、分词器、相关性评分、查询 DSL 与业务排序策略的共同设计。

## 面试重点

- 倒排索引、doc values、segment、refresh、flush、merge、translog。
- mapping 设计、text/keyword、分词器、bool query、聚合、分页和深分页。
- 分片规划、写入链路、搜索链路、节点角色、集群健康状态。

## 实践检查点

- 能解释为什么深分页昂贵，以及 `search_after`、scroll、PIT 的适用场景。
- 能针对写多读多场景分别调整 refresh interval、bulk、routing、分片数。

## 版本与趋势

- Elasticsearch 8.x 默认安全能力更完整，向量检索、混合检索、运行时字段和 ILM 是近年重点。
- 搜索系统需要同时治理写入、查询、索引生命周期、分片容量和相关性评估。

## 章节目录

### ES.xmind

- [Elasticsearch历史](01-elasticsearch历史.md)
- [DSL进阶](02-dsl进阶.md)
- [不只是文本搜索](03-不只是文本搜索.md)
- [数据建模与分析](04-数据建模与分析.md)
- [改善用户搜索体验](05-改善用户搜索体验.md)
- [分布式索引架构](06-分布式索引架构.md)
- [底层索引控制](07-底层索引控制.md)
- [管理ES](08-管理es.md)
- [数据转换与联盟搜索](09-数据转换与联盟搜索.md)
- [提升性能](10-提升性能.md)
- [ES Stack 5.0](11-es-stack-50.md)
- [instantiate](12-instantiate.md)
### 面试内容汇总/ES.xmind

- [总体架构(从下往上)](13-总体架构从下往上.md)
- [启动](14-启动.md)
- [分析器](15-分析器.md)
- [数据结构](16-数据结构.md)
- [索引](17-索引.md)
- [_uid与_id](18-uid与-id.md)
- [文档修改方式](19-文档修改方式.md)
- [评分](20-评分.md)
- [搜索过程](21-搜索过程.md)
- [并发控制](22-并发控制.md)
- [节点](23-节点.md)
- [主节点选举](24-主节点选举.md)
- [节点类型](25-节点类型.md)
- [数据转换与联盟搜索](26-数据转换与联盟搜索.md)
- [索引更新](27-索引更新.md)
- [事务日志](28-事务日志.md)
- [instantiate](29-instantiate.md)
