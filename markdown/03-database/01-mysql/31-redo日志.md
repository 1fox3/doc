# Redo日志

## 核心职责

- redo log 记录页级物理变更，用于崩溃恢复。
- redo log 让事务提交不必同步刷脏页，从而提升写入性能。
- redo log 是循环写，checkpoint 决定哪些日志可以复用。

## 提交流程

- 事务修改数据页，生成 redo 并写入 redo log buffer。
- 提交时 redo 根据刷盘策略落盘。
- 开启 binlog 时，通过两阶段提交保证 redo 和 binlog 一致。

## 配置关注

- `innodb_flush_log_at_trx_commit=1` 持久性最强。
- `sync_binlog=1` 可降低 binlog 丢失风险。
- redo 容量过小会导致写入抖动，过大则可能增加崩溃恢复时间。

```sql
SHOW VARIABLES LIKE 'innodb_redo_log_capacity';
SHOW VARIABLES LIKE 'innodb_flush_log_at_trx_commit';
SHOW VARIABLES LIKE 'sync_binlog';
```

## redo 写入位置

- redo 先写入 redo log buffer。
- 后台线程或事务提交会将 redo log buffer 写入 redo 文件。
- fsync 决定是否真正要求操作系统把日志持久化到存储设备。
- 参数不同会影响“事务提交返回”和“日志真正持久”的时间点。

## 观察指标

- `SHOW ENGINE INNODB STATUS` 中的 Log sequence number 表示当前 LSN。
- Log flushed up to 表示已经刷到 redo 文件的位置。
- Pages flushed up to 或 checkpoint 相关信息反映 checkpoint 推进。
- LSN 增长速度可以粗略反映写入压力。

## 常见问题

- redo 空间压力大时，写入线程可能等待 checkpoint。
- 大事务会占用 redo 空间，提交和恢复成本都更高。
- 刷盘策略放宽后，数据库正常关闭通常不丢数据，但操作系统崩溃或断电风险会增加。
