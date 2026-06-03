# MyBatis

> 来源：面试内容汇总/MyBatis.xmind

## 核心认知

- MyBatis 是半自动 ORM，重点是 SQL 映射、Executor、缓存、插件和动态 SQL。
- 它适合 SQL 可控、复杂查询多的场景，但需要团队治理 SQL 质量。

## 面试重点

- 一级缓存、二级缓存、Mapper 代理、Executor、StatementHandler、ResultSetHandler。
- 插件拦截链、动态 SQL、`#{} / ${}` 区别和 SQL 注入风险。

## 实践检查点

- 能实现分页、审计字段、慢 SQL 记录等插件，并说明拦截点选择。
- 能处理 N+1 查询、结果映射错误和缓存脏读问题。

## 版本与趋势

- MyBatis 仍适合 SQL 可控场景，MyBatis-Plus 等增强工具可提升效率但不能替代 SQL 与索引能力。
- 生产问题常集中在动态 SQL 失控、N+1 查询、分页性能、慢 SQL 和 Mapper 映射不一致。

## 章节目录

- [基础](01-基础/README.md)
- [Executor](02-executor.md)
- [插件](03-插件.md)
- [instantiate](04-instantiate.md)
