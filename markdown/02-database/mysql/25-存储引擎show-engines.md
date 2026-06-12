# 存储引擎(show engines)

## 查看方式

```sql
SHOW ENGINES;
SHOW VARIABLES LIKE 'default_storage_engine';
SHOW TABLE STATUS WHERE Name = 't_user';
```

## 常见引擎

- InnoDB：默认引擎，支持事务、行锁、MVCC、外键、崩溃恢复。
- MyISAM：非事务引擎，表锁，不支持崩溃安全事务，现代业务不建议作为主引擎。
- MEMORY：数据存储在内存中，适合临时数据，实例重启后数据丢失。
- CSV：以 CSV 文件存储，适合简单交换，不适合高性能查询。
- ARCHIVE：面向归档插入和压缩存储，查询和更新能力有限。
- BLACKHOLE：写入丢弃，特殊复制或测试场景使用。
- FEDERATED：访问远程 MySQL 表，运维和性能风险较高。

## 选择原则

- 业务表默认选择 InnoDB。
- 只有在临时表、归档、测试或兼容历史系统时才考虑其他引擎。
- 混用存储引擎会带来事务语义、锁行为、备份恢复和复制一致性差异。

## `SHOW ENGINES` 字段

- `Engine` 表示存储引擎名称。
- `Support` 表示是否支持，`DEFAULT` 表示当前默认引擎。
- `Comment` 简述引擎能力。
- `Transactions` 表示是否支持事务。
- `XA` 表示是否支持 XA 事务。
- `Savepoints` 表示是否支持保存点。

## 建表指定引擎

```sql
CREATE TABLE t_order (
  id bigint PRIMARY KEY,
  amount decimal(10, 2) NOT NULL
) ENGINE=InnoDB;

ALTER TABLE t_order ENGINE=InnoDB;
```

## 兼容性注意

- 从 MyISAM 迁移到 InnoDB 后，锁粒度、事务行为、索引组织和空间占用都会变化。
- MEMORY 表受内存限制，数据丢失语义必须被业务接受。
- 非 InnoDB 表不一定能被 InnoDB 事务回滚，混用时要格外小心。
