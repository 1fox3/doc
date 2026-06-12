# 缓存与事务

## 一级缓存

一级缓存是 `SqlSession` 级别缓存，默认开启。同一个 SqlSession 中，相同 statement 和参数的查询可能命中缓存。

一级缓存会在 update、commit、rollback、close 或显式 clearCache 时清理。和 Spring 集成时，SqlSession 生命周期通常绑定到事务，没有事务时每次 Mapper 调用可能使用不同 SqlSession。

## 二级缓存

二级缓存是 namespace 级别缓存，需要显式开启。多个 SqlSession 可共享同一 namespace 的缓存数据。

二级缓存适合读多写少、数据变化不频繁、能接受一定一致性延迟的场景。不适合强一致、高频更新、跨 namespace 关联复杂的数据。

## 缓存风险

- 多表关联查询只归属于一个 namespace，其他表更新不会自动清理该缓存。
- 本地缓存可能造成同事务内重复查询看到旧对象。
- 二级缓存对象需要可序列化或可安全共享。
- 与外部缓存结合时需要明确失效策略。

生产系统更常用 Redis、Caffeine 等显式缓存方案，并由业务代码控制 key、TTL 和失效逻辑。

## MyBatis 事务

MyBatis 原生事务由 `Transaction` 抽象控制，常见实现有 JDBC 事务和 Managed 事务。

与 Spring 集成后，事务边界通常由 Spring `DataSourceTransactionManager` 管理，MyBatis 通过 `SqlSessionTemplate` 参与同一连接和事务上下文。

## Spring 集成

`SqlSessionTemplate` 是线程安全的 SqlSession 代理，负责把 Mapper 调用绑定到当前 Spring 事务。如果没有 Spring 事务，每次数据库操作通常独立获取和关闭 SqlSession。

事务问题排查应关注：

- Mapper 使用的数据源是否和事务管理器一致。
- 方法是否经过 Spring 事务代理。
- 异常是否被吞掉。
- 批处理是否及时 flush。
- 多数据源是否正确选择事务管理器。
