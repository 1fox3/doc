# MySQL

MySQL 目录按 InnoDB、索引、优化器、事务、锁、日志和运维排查整理。默认以 MySQL 8.0 和 InnoDB 为主，除非文档明确说明历史特性。

## 学习主线

- 连接层：服务启动、参数加载、认证、连接线程、SQL 解析与优化。
- 存储层：InnoDB 记录格式、数据页、表空间、Buffer Pool、redo log、undo log。
- 查询层：访问方法、连接算法、成本模型、统计信息、规则优化、`EXPLAIN`、`optimizer_trace`。
- 并发层：事务、隔离级别、MVCC、行锁、表锁、间隙锁、死锁排查。
- 工程实践：字符集治理、慢 SQL 分析、索引设计、查询缓存历史问题、常用诊断命令。

## 关键检查点

- 能通过 `EXPLAIN FORMAT=JSON` 判断访问方法、驱动表、索引选择、回表和排序代价。
- 能解释 InnoDB 在 RC/RR 下快照读、当前读、ReadView、undo 版本链和 next-key lock 的差异。
- 能说明 redo log、undo log、binlog 在提交、回滚、崩溃恢复和复制中的职责边界。
- 能用 `SHOW ENGINE INNODB STATUS`、`performance_schema`、慢日志定位锁等待、死锁和慢 SQL。

## 章节目录

### MySQL.xmind

- [服务启动](01-服务启动.md)
- [启动项和系统变量](02-启动项和系统变量.md)
- [字符集和比较规则](03-字符集和比较规则.md)
- [InnoDB记录存储结构](04-innodb记录存储结构.md)
- [InnoDB数据页结构](05-innodb数据页结构.md)
- [B+树索引](06-b树索引.md)
- [B+树索引树的使用](07-b树索引树的使用.md)
- [MySQL数据目录](08-mysql数据目录.md)
- [InnoDB表空间](09-innodb表空间.md)
- [单表访问方法](10-单表访问方法.md)
- [连接的原理](11-连接的原理.md)
- [基于成本的优化](12-基于成本的优化.md)
- [InnoDB数据统计](13-innodb数据统计.md)
- [基于规则的优化](14-基于规则的优化.md)
- [EXPLAIN详解](15-explain详解.md)
- [Optimizer Trace](16-optimizer-trace.md)
- [InnoDB的Buffer Pool](17-innodb的buffer-pool.md)
- [事务](18-事务.md)
- [Redo日志](19-redo日志.md)
- [Undo日志](20-undo日志.md)
- [隔离级别和MVCC](21-隔离级别和mvcc.md)
- [锁](22-锁.md)
- [instantiate](23-instantiate.md)

### 面试内容汇总/MySQL.xmind

- [基本常识](24-基本常识.md)
- [存储引擎(show engines)](25-存储引擎show-engines.md)
- [字符集比较规则](26-字符集比较规则.md)
- [单表访问方法](27-单表访问方法.md)
- [连接的原理](28-连接的原理.md)
- [基于成本的优化](29-基于成本的优化.md)
- [InnoDB的Buffer Pool](30-innodb的buffer-pool.md)
- [Redo日志](31-redo日志.md)
- [Undo日志](32-undo日志.md)
- [隔离级别和MVCC](33-隔离级别和mvcc.md)
- [锁](34-锁.md)
- [基础架构](35-基础架构.md)
- [小技巧](36-小技巧.md)
- [存储引擎](37-存储引擎.md)
- [查询缓存](38-查询缓存.md)
- [事务](39-事务.md)
- [锁](40-锁.md)
- [索引](41-索引.md)
- [instantiate](42-instantiate.md)
