# Undo日志

## 核心职责

- 支持事务回滚，将数据恢复到修改前状态。
- 支持 MVCC，为快照读提供历史版本。
- 支持一致性读，使读写并发时读操作不必阻塞写操作。

## 版本链

- 行记录中的 `DB_ROLL_PTR` 指向 undo 记录。
- 多次更新会形成从新到旧的版本链。
- ReadView 判断当前版本不可见时，会沿版本链查找可见版本。

## 清理机制

- purge 线程在确认没有事务依赖旧版本后清理 undo。
- 长事务会阻塞 purge，导致历史版本堆积。
- 大批量 DML 应分批提交，降低 undo 表空间和恢复压力。

```sql
SELECT trx_id, trx_started, trx_query FROM information_schema.innodb_trx;
SHOW ENGINE INNODB STATUS\G
```

## 批量删除示例

```sql
-- 每次删除一小批，应用侧循环执行并提交。
DELETE FROM event_log
WHERE id >= 1000000 AND id < 1010000
  AND created_at < '2025-01-01';
```

## 故障现象

- 磁盘空间持续增长，但业务表数据量没有明显增加。
- 普通快照查询变慢，尤其是需要访问被频繁更新的记录。
- `SHOW ENGINE INNODB STATUS` 中 history list length 长时间不下降。
- 从库回放大事务慢，复制延迟明显增加。

## 排查顺序

- 查找最早开始且未提交的事务。
- 判断该事务是否来自应用连接池、定时任务、备份工具或人工会话。
- 评估能否安全提交或回滚该事务。
- 长事务结束后继续观察 purge 是否追上以及 undo 空间是否可复用。
