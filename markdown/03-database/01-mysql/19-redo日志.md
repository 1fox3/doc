# Redo日志

## 作用

- redo log 记录 InnoDB 对页的物理修改，用于崩溃恢复。
- InnoDB 采用 WAL 机制，事务提交时可以先保证 redo 持久化，再延后刷脏页。
- redo log 只属于 InnoDB，和服务层 binlog 职责不同。

## 写入流程

- 修改数据页时先生成 redo record，写入 redo log buffer。
- 提交时根据 `innodb_flush_log_at_trx_commit` 决定是否写入和 fsync redo 文件。
- checkpoint 推进后，早于 checkpoint 的 redo 可被覆盖或释放。

## 关键参数

- `innodb_flush_log_at_trx_commit=1`：每次提交写 redo 并 fsync，持久性最好。
- `innodb_flush_log_at_trx_commit=2`：每次提交写入 OS cache，约每秒 fsync，可能丢失约 1 秒事务。
- `innodb_flush_log_at_trx_commit=0`：约每秒写入并 fsync，崩溃丢失风险更高。
- `innodb_redo_log_capacity` 控制 MySQL 8.0 redo 总容量，容量过小会导致频繁 checkpoint。

## 和 binlog 的关系

- redo 保证 InnoDB 崩溃恢复，binlog 用于复制和时间点恢复。
- 开启 binlog 时，事务提交通过两阶段提交协调 redo 和 binlog，避免主库崩溃后复制状态不一致。

```sql
SHOW VARIABLES LIKE 'innodb_flush_log_at_trx_commit';
SHOW VARIABLES LIKE 'sync_binlog';
SHOW ENGINE INNODB STATUS\G
```

## WAL 和 checkpoint

- WAL 的核心是先写日志，再写数据页。
- checkpoint 表示某个 LSN 之前的脏页已经安全刷盘，恢复时只需重放 checkpoint 之后的 redo。
- redo 可用空间不足时，InnoDB 必须推进 checkpoint，可能导致前台写入等待刷脏页。
- redo 容量越大，写入峰值承载更好，但崩溃恢复可能需要扫描更多日志。

## 两阶段提交细节

- prepare 阶段：InnoDB 写 redo 并标记事务为 prepared。
- Server 层写 binlog。
- commit 阶段：InnoDB 将 redo 标记为 committed。
- 崩溃恢复时，如果 redo prepared 但没有对应 binlog，则回滚；如果 binlog 存在，则提交，保证复制和主库一致。

## 故障取舍

- `innodb_flush_log_at_trx_commit=1` 搭配 `sync_binlog=1` 是强持久组合，但 fsync 压力更大。
- 对极端写入性能场景可放宽刷盘策略，但必须接受崩溃丢失事务的风险。
- 云盘或 RAID 控制器缓存策略会影响 fsync 真实可靠性，不能只看数据库参数。
