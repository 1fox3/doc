# MyBatis

MyBatis 是半自动 ORM 框架，核心是把 Java 方法调用映射为 SQL 执行，并把结果集映射回 Java 对象。它不隐藏 SQL，适合复杂查询、强 SQL 控制和需要精细优化的业务场景。

## 技术专题

- [核心架构与执行流程](01-architecture-flow.md)
- [映射、参数与动态 SQL](02-mapping-dynamic-sql.md)
- [缓存与事务](03-cache-transaction.md)
- [插件机制与生产实践](04-plugin-practice.md)

## 核心链路

1. Mapper 接口方法被代理对象拦截。
2. 根据接口方法定位 `MappedStatement`。
3. 解析参数并生成 `BoundSql`。
4. Executor 调度查询或更新。
5. StatementHandler 创建并预编译 SQL。
6. ParameterHandler 设置参数。
7. JDBC 执行 SQL。
8. ResultSetHandler 映射结果集。

## 适用边界

- 适合 SQL 复杂、查询性能要求高、需要显式控制 SQL 的系统。
- 不适合希望完全屏蔽 SQL、以对象关系自动同步为主的场景。
- 动态 SQL、分页、批处理和缓存需要明确治理，否则容易出现性能和一致性问题。
