# Mapper中的SQL id能否重复

> 专题：MyBatis
> 来源：面试内容汇总/MyBatis.xmind

## 补充与实践

- 补充：MyBatis 插件通过拦截 Executor、StatementHandler、ParameterHandler、ResultSetHandler 扩展执行链路。
- 实践：分页、审计、慢 SQL 插件要谨慎处理 SQL 改写和参数绑定，避免破坏执行计划。
- 误区：二级缓存跨 SqlSession，若更新链路复杂或多服务写入，容易产生一致性问题。

## 脑图内容

## Mapper中的SQL id能否重复

### 配置了namespace，id可重复

### 没有配置namespace，id不可重复

### 只要namespace+id唯一就好
