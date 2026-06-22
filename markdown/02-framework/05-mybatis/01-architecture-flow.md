# 核心架构与执行流程

## 核心对象

- `SqlSessionFactory`：创建 `SqlSession`，通常一个数据源对应一个工厂。
- `SqlSession`：执行 SQL、获取 Mapper、管理一级缓存和事务边界。
- `Configuration`：保存 MyBatis 全局配置、Mapper、MappedStatement、TypeHandler、插件等。
- `MappedStatement`：一条 SQL 映射的元数据，包含 SQL 类型、参数映射、结果映射、缓存配置等。
- `Executor`：执行器，负责查询、更新、缓存和事务协作。
- `StatementHandler`：创建 JDBC Statement 并执行 SQL。
- `ParameterHandler`：为 PreparedStatement 设置参数。
- `ResultSetHandler`：把 ResultSet 映射为 Java 对象。

## Mapper 代理

Mapper 接口没有实现类，MyBatis 通过 JDK 动态代理创建代理对象。调用接口方法时，代理会根据接口全限定名和方法名定位 `MappedStatement`。

Mapper XML 中的 `namespace` 应等于 Mapper 接口全限定名，SQL 的 `id` 应与接口方法名对应。同一个 namespace 下 SQL id 不能重复。

## Executor 类型

- `SimpleExecutor`：每次执行都创建新的 Statement。
- `ReuseExecutor`：复用相同 SQL 的 Statement。
- `BatchExecutor`：批量执行更新语句，适合批量插入或更新。

Executor 外层可能被 `CachingExecutor` 包装，用于处理二级缓存逻辑。

## 执行流程

1. Mapper 方法调用进入代理。
2. `MapperMethod` 解析方法签名和 SQL 命令类型。
3. `SqlSession` 调用查询或更新方法。
4. Executor 根据 `MappedStatement` 和参数执行。
5. `StatementHandler` 生成最终 SQL。
6. `ParameterHandler` 绑定参数。
7. JDBC 执行。
8. `ResultSetHandler` 处理结果映射。

## TypeHandler

`TypeHandler` 负责 Java 类型与 JDBC 类型之间的转换。常见场景包括枚举映射、JSON 字段、时间类型、自定义状态对象等。

当参数可能为 `null`，且数据库或驱动无法推断 JDBC 类型时，应显式指定 `jdbcType`。复杂对象或非标准类型建议注册自定义 TypeHandler。
