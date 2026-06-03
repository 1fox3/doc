# EXPLAIN详解

> 专题：MySQL
> 来源：Mysql.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## EXPLAIN详解

### 结果结构

#### id

- 在一个大的查询中，每个SELECT关键字都对应一个唯一的id

#### select_type

- SELECT关键字对应的查询类型

#### table

- 表名

#### partitions

- 匹配的分区信息

#### type

- 针对单表的访问方法

#### possible_keys

- 可能使用到的索引

#### key

- 实际使用的索引

#### key_len

- 实际使用的索引长度

#### ref

- 当使用索引列等值查询时，与索引列进行等值匹配的对象

#### rows

- 预估的需要读取的记录条数

#### filtered

- 针对预估的需要读取的记录，经过搜索条件过滤后剩余记录条数的百分比

#### Extra

- 一些额外信息

### JSON格式的执行计划

#### EXPLAIN FORMAT=JSON sql

### SHOW WARRINGS

#### Level

#### Code

#### Message

- Code为1003时，Message里的内容为查询优化器重写之后的语句
