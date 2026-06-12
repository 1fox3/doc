# Undo日志

## 作用

- undo log 记录行修改前的逻辑信息，用于事务回滚和 MVCC 快照读。
- `INSERT` 的 undo 主要用于回滚插入，事务提交后可较快清理。
- `UPDATE` 和 `DELETE` 的 undo 会形成旧版本链，需等没有 ReadView 依赖后才能 purge。

## MVCC 关系

- 每行记录包含 `DB_TRX_ID` 和 `DB_ROLL_PTR`。
- 快照读根据 ReadView 判断当前版本是否可见，不可见时沿 `DB_ROLL_PTR` 查找 undo 中的历史版本。
- 长事务会阻止 purge 清理旧版本，导致 undo 表空间膨胀和查询变慢。

## 实践风险

- 大批量更新或删除会生成大量 undo，影响磁盘和恢复时间。
- 长时间未提交事务会拖住历史版本，可能使普通查询也变慢。
- 归档删除建议分批提交，降低单事务 undo、redo 和锁压力。

## 常用检查

```sql
SELECT * FROM information_schema.innodb_trx\G
SHOW ENGINE INNODB STATUS\G
SHOW VARIABLES LIKE 'innodb_undo%';
```

## undo 与 purge

- 事务提交后，undo 不一定立即删除，因为可能仍有快照读需要旧版本。
- purge 线程会在确认没有 ReadView 依赖后清理历史版本，并最终释放或复用 undo 空间。
- `history list length` 持续增长通常意味着 purge 跟不上或存在长事务阻塞。

## 大事务影响

- 大更新会产生大量 undo，回滚时也需要按 undo 逐条反向执行，回滚可能比执行更慢。
- undo 膨胀会增加磁盘占用，也会让快照读沿版本链查找更久。
- 大事务还会产生大量 redo 和 binlog，影响复制延迟和崩溃恢复。

## 治理建议

- 归档删除使用小批量循环提交，例如每批 1000 到 10000 行，按主键范围推进。
- 避免在事务中长时间打开游标或执行慢查询。
- 监控长事务开始时间、undo history 长度和 undo 表空间大小。
