# 事务管理

## 事务抽象

Spring 通过 `PlatformTransactionManager` 抽象不同事务资源。JDBC 常用 `DataSourceTransactionManager`，JPA 常用 `JpaTransactionManager`，分布式事务需要额外事务协调器。

声明式事务由 `@Transactional` 加 AOP 实现，拦截器在方法执行前开启或加入事务，在方法返回后提交，在异常时按规则回滚。

## 传播行为

- `REQUIRED`：有事务则加入，没有则新建，默认行为。
- `REQUIRES_NEW`：挂起当前事务并新建事务。
- `NESTED`：在当前事务内创建保存点，依赖 JDBC Savepoint。
- `SUPPORTS`：有事务则加入，没有则非事务执行。
- `NOT_SUPPORTED`：挂起当前事务，非事务执行。
- `MANDATORY`：必须存在事务，否则抛异常。
- `NEVER`：必须不存在事务，否则抛异常。

## 隔离级别

- `READ_UNCOMMITTED`：可能脏读、不可重复读、幻读。
- `READ_COMMITTED`：避免脏读，常见于 Oracle、PostgreSQL 默认级别。
- `REPEATABLE_READ`：避免脏读和不可重复读，MySQL InnoDB 默认级别。
- `SERIALIZABLE`：最强隔离，冲突和锁等待成本最高。

隔离级别最终由数据库实现决定。Spring 只是把隔离级别设置到连接或事务资源上。

## 回滚规则

默认情况下，运行时异常和 `Error` 会触发回滚，受检异常不会触发回滚。可通过 `rollbackFor`、`noRollbackFor` 明确配置。

## 常见失效场景

- 同类内部自调用绕过代理。
- 方法不是 `public`，导致代理无法按预期拦截。
- 异常被捕获后没有继续抛出。
- 数据库表不支持事务，如 MySQL MyISAM。
- 事务管理器配置错误或多数据源绑定错误。
- `@Transactional` 标在非 Spring Bean 上。

## 编程式事务

`TransactionTemplate` 适合需要精确控制事务边界的场景，例如部分代码需要独立提交、捕获异常后仍要决定提交或回滚、循环批处理需要拆分事务。
