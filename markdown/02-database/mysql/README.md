# MySQL

> 来源：Mysql.xmind, 面试内容汇总/Mysql.xmind

## 核心认知

- MySQL 学习主线是存储引擎、索引、事务、锁、日志和优化器。InnoDB 是重点。
- SQL 性能问题通常由数据分布、索引选择、执行计划、锁等待或事务边界引起。

## 面试重点

- B+Tree 索引、聚簇索引、覆盖索引、最左前缀、索引下推、回表。
- MVCC、ReadView、隔离级别、当前读/快照读、间隙锁和临键锁。
- redo log、undo log、binlog、两阶段提交、主从复制和 crash recovery。

## 实践检查点

- 能用 `EXPLAIN` 分析 type、key、rows、Extra，并给出索引或 SQL 改写方案。
- 能说明慢 SQL 治理流程：定位、复现、看执行计划、改索引/SQL、压测验证。

## 版本与趋势

- MySQL 8.0 是当前主流版本，窗口函数、CTE、直方图、Invisible Index、Instant DDL 等能力值得掌握。
- 生产治理重点从单 SQL 优化扩展到容量规划、慢查询治理、备份恢复、主从延迟和在线变更。

## 章节目录

### Mysql.xmind

- [服务启动](01-服务启动.md)
- [启动项和系统变量](02-启动项和系统变量.md)
- [字符集和比较规则](03-字符集和比较规则.md)
- [InnoDB记录存储结构](04-innodb记录存储结构.md)
- [InnoDB数据页结构](05-innodb数据页结构.md)
- [B+树索引](06-b树索引.md)
- [B+树索引树的使用](07-b树索引树的使用.md)
- [Mysql数据目录](08-mysql数据目录.md)
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
### 面试内容汇总/Mysql.xmind

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
