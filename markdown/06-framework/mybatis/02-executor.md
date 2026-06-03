# Executor

> 专题：MyBatis
> 来源：面试内容汇总/MyBatis.xmind

## 补充与实践

- 补充：MyBatis 插件通过拦截 Executor、StatementHandler、ParameterHandler、ResultSetHandler 扩展执行链路。
- 实践：分页、审计、慢 SQL 插件要谨慎处理 SQL 改写和参数绑定，避免破坏执行计划。
- 误区：二级缓存跨 SqlSession，若更新链路复杂或多服务写入，容易产生一致性问题。

## 脑图内容

## Executor

### SimpleExecutor

#### 每执行一次update或select，就开启一个Statement对象，用完立刻关闭Statment对象

### ReuseExecutor

#### 执行update或select，以sql作为key查找Statement对象，存在就是用，不存在就创建，使用完后，不关闭Statement，放在Map中，共下一次使用

### BatchExecutor

#### 执行update，将所有的sql都添加到批处理中，它缓存了多个Statment对象，每个Statement对象都是addBatch完毕后，等待逐一执行executeBatch()批处理，与JDBC批处理相同
