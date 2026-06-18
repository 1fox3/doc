# 隔离级别和MVCC

## 隔离级别

- `READ UNCOMMITTED`：可能读到未提交数据，实际生产很少使用。
- `READ COMMITTED`：每次一致性读生成新的 ReadView，可避免脏读，但可能不可重复读。
- `REPEATABLE READ`：事务第一次一致性读生成 ReadView，后续复用，可避免不可重复读，是 InnoDB 默认隔离级别。
- `SERIALIZABLE`：读写串行化倾向更强，并发能力最低。

## ReadView

- ReadView 记录创建时活跃事务 ID 列表、最小活跃事务 ID、下一个待分配事务 ID 和当前事务 ID。
- 快照读根据行记录 `DB_TRX_ID` 与 ReadView 判断版本是否可见。
- 当前读不使用快照版本，会读取最新已提交记录并加锁，例如 `SELECT ... FOR UPDATE`、`UPDATE`、`DELETE`。

## 幻读处理

- 快照读通过 ReadView 保证同一事务中查询结果的一致性。
- 当前读在 RR 下通过 record lock、gap lock、next-key lock 锁定记录和间隙，阻止符合范围的新记录插入。
- RC 下通常不使用 gap lock 处理普通范围当前读，锁冲突更少，但幻读约束更弱。

## 实践要点

- 只读查询优先使用快照读，避免不必要的 `FOR UPDATE`。
- 高并发写入场景可评估 RC 降低 gap lock 冲突，但要确认业务是否依赖 RR 语义。
- 长事务会使 ReadView 长时间存在，导致 undo 无法清理。

## 可见性判断简化规则

- 如果行版本事务 ID 等于当前事务 ID，当前事务可见自己的修改。
- 如果行版本事务 ID 小于 ReadView 最小活跃事务 ID，说明创建该版本的事务已提交，可见。
- 如果行版本事务 ID 大于等于 ReadView 下一个事务 ID，说明是 ReadView 创建后才出现的版本，不可见。
- 如果行版本事务 ID 在活跃事务列表中，说明创建该版本的事务当时未提交，不可见。
- 其他情况表示创建版本的事务在 ReadView 创建前已提交，可见。

## 示例场景

```sql
-- 事务 A，RR 隔离级别。
START TRANSACTION;
SELECT balance FROM account WHERE id = 1;

-- 事务 B 更新并提交。
UPDATE account SET balance = balance + 100 WHERE id = 1;
COMMIT;

-- 事务 A 再次普通 SELECT，仍看到第一次 ReadView 中可见的版本。
SELECT balance FROM account WHERE id = 1;

-- 当前读会读取最新已提交版本并加锁。
SELECT balance FROM account WHERE id = 1 FOR UPDATE;
```

## RC 与 RR 的工程差异

- RC 下每条语句读到的是语句开始前已提交版本，更贴近很多应用直觉。
- RR 下事务内多次一致性读稳定，但长事务更容易拖住 undo。
- RC 的 gap lock 使用更少，写入冲突可能降低，但范围约束需要业务或唯一索引兜底。
