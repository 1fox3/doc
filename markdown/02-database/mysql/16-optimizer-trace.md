# Optimizer Trace

> 专题：MySQL
> 来源：Mysql.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## Optimizer Trace

### 开启

#### SET optimizer_trace=“enabled=on”

### 查询执行计划生成过程

#### information_schema.OPTIMIZER_TRACE

- QUERY
  - 我们输入的查询语句

- TRACE
  - 表示优化过程的JSON格式的文本

- MISSING)BYTES_BEYOND_MAX_MEM_SIZE
  - 被忽略的文本字节数

- INSUFFICENT_PRIVILEGES
  - 是否有权限查看执行计划的生成过程

### 3个阶段

#### prepare阶段

#### optimize阶段

#### execute阶段
