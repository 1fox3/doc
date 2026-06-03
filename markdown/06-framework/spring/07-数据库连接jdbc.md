# 数据库连接JDBC

> 专题：Spring
> 来源：Spring.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## 数据库连接JDBC

### 获取链接：DateSourceUtils.getConnection

#### 在事务中使用用一个数据库连接

### 应用入参：applyStatementSettings

#### 设置最大记录数等

### 调用：doInPrepareStatment

#### update

#### query

### 处理异常：handleWarnings

### 释放资源：releaseConnection

#### ConnetorHolder中连接数减一，并非真正释放连接
