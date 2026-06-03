# InnoDB数据统计

> 专题：MySQL
> 来源：Mysql.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## InnoDB数据统计

### 配置

#### innodb_stats_persistent

#### STATS_PERSISTENT

### 划分

#### 永久性地存储统计数据

- 更新方式
  - innodb_stats_auto_recalc= On|OFF 配置项
  - STATS_AUTO_RECALC=0|1 建表时使用
  - ANALYZE TABLE table
  - 直接更新统计表，并执行 FLUSH TABLE single_table

- 相关表
  - innodb_index_stats
  - innodb_table_stats

#### 非永久性地存储统计数据

- innodb_stats_method
