# 映射、参数与动态 SQL

## 参数绑定

MyBatis 支持单参数、多参数、Map、对象和 `@Param` 注解绑定。

多参数方法建议使用 `@Param` 指定参数名，避免依赖编译参数名或默认 `param1`、`param2`。

## #{} 与 ${}

- `#{}` 使用 PreparedStatement 参数占位符，会进行预编译和参数绑定，可防止 SQL 注入。
- `${}` 是字符串替换，会把内容直接拼进 SQL，存在 SQL 注入风险。

`${}` 只应在无法使用占位符的位置使用，例如动态表名、列名、排序字段。使用时必须对输入做白名单校验。

## ResultMap

`resultMap` 用于声明复杂结果映射，适合字段名与属性名不一致、嵌套对象、一对多、一对一、构造器映射和枚举映射。

`resultType` 适合简单映射。复杂查询应优先使用 `resultMap`，避免隐式映射导致字段缺失或类型转换错误。

## 动态 SQL

常用动态标签：

- `if`：条件片段。
- `choose`、`when`、`otherwise`：分支选择。
- `where`：自动处理开头多余的 `AND` 或 `OR`。
- `set`：更新语句中自动处理多余逗号。
- `trim`：自定义前缀、后缀和裁剪规则。
- `foreach`：遍历集合，常用于 `IN` 条件和批量插入。
- `bind`：绑定临时变量。

## 分页

物理分页应在 SQL 层使用数据库分页语法，如 MySQL `limit offset,size`。大偏移分页会导致扫描成本高，可使用基于游标或最后一条记录条件的 seek pagination。

分页插件通常拦截 StatementHandler 或 Executor，改写 SQL 并追加 count 查询。需要注意复杂 SQL、group by、union 和多数据源方言兼容。

## 主键生成

常见方式：

- 数据库自增主键：使用 `useGeneratedKeys=true` 和 `keyProperty`。
- 序列：Oracle、PostgreSQL 可使用 sequence 或 `selectKey`。
- 应用生成：雪花算法、UUID、业务号段等。

批量插入时不同数据库和驱动对生成主键返回支持不同，需要单独验证。
