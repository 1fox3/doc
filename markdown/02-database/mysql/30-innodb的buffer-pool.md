# InnoDB的Buffer Pool

> 专题：MySQL
> 来源：面试内容汇总/Mysql.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## InnoDB的Buffer Pool

### 配置

#### innodb_buffer_pool_size

- 缓冲区大小

#### innodb_buffer_pool_instance

- 缓冲区实例个数

#### innodb_buffer_pool_chunk_size

- 每次申请内存空间大小

### 划分

#### free链表

#### flush链表

### 冷热数据划分

#### young区域- 热数据

#### old区域-冷数据

### 刷新脏页数据到磁盘

#### 从LRU链表的冷数据中刷新一部分页面到磁盘

#### 从flush链表中刷新一部分到磁盘
