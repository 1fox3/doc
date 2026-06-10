# Executor

> 专题：MyBatis
> 来源：面试内容汇总/MyBatis.xmind

## 补充与实践

- 补充：MyBatis 插件通过拦截 Executor、StatementHandler、ParameterHandler、ResultSetHandler 扩展执行链路。
- 实践：分页、审计、慢 SQL 插件要谨慎处理 SQL 改写和参数绑定，避免破坏执行计划。
- 误区：二级缓存跨 SqlSession，若更新链路复杂或多服务写入，容易产生一致性问题。

## 详细说明

### 是什么

- `Executor` 是 `MyBatis` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `Executor` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `Executor`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `Executor` 展开，属于 `MyBatis` 的复习范围。
- 建议优先掌握：SimpleExecutor, ReuseExecutor, BatchExecutor。
- 二级节点提示了主要拆分角度：每执行一次update或select，就开启一个Statement对象，用完立刻关闭Statment对象, 执行update或select，以sql作为key查找Statement对象，存在就是用，不存在就创建，使用完后，不关闭Statement，放在Map中，共下一次使用, 执行update，将所有的sql都添加到批处理中，它缓存了多个Statment对象，每个Statement对象都是addBatch完毕后，等待逐一执行executeBatch()批处理，与JDBC批处理相同。

### 复习追问

- `SimpleExecutor` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `ReuseExecutor` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `BatchExecutor` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## Executor

### SimpleExecutor

#### 每执行一次update或select，就开启一个Statement对象，用完立刻关闭Statment对象

### ReuseExecutor

#### 执行update或select，以sql作为key查找Statement对象，存在就是用，不存在就创建，使用完后，不关闭Statement，放在Map中，共下一次使用

### BatchExecutor

#### 执行update，将所有的sql都添加到批处理中，它缓存了多个Statment对象，每个Statement对象都是addBatch完毕后，等待逐一执行executeBatch()批处理，与JDBC批处理相同
