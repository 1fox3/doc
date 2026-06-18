# InnoDB表空间

## 表空间类型

- 系统表空间保存 InnoDB 系统数据，历史版本中还可能保存用户表和 undo 信息。
- 独立表空间由 `innodb_file_per_table` 控制，每张表的数据和索引通常存储在独立 `.ibd` 文件中。
- undo 表空间保存事务回滚和 MVCC 旧版本，临时表空间保存内部临时表和用户临时表数据。
- 通用表空间可让多张表共享一个表空间文件，但运维复杂度高，使用前需要明确收益。

## 段、区、页

- 表空间由页组成，默认页大小为 16KB。
- 区是连续页集合，默认 1MB，用于减少频繁离散分配。
- 段用于管理 B+Tree 的叶子页、非叶子页等逻辑空间。

## 空间回收

- 删除记录通常只标记可复用空间，不一定缩小 `.ibd` 文件。
- `OPTIMIZE TABLE` 或重建表可整理碎片并回收独立表空间文件空间，但会消耗 I/O 并可能加元数据锁。
- 大表空间治理优先评估归档、分区、在线 DDL 工具和业务低峰窗口。

## 常用检查

```sql
SHOW VARIABLES LIKE 'innodb_file_per_table';
SELECT table_schema, table_name, data_length, index_length
FROM information_schema.tables
WHERE engine = 'InnoDB';
```

## 独立表空间的优缺点

- 优点是单表数据和索引存放在独立 `.ibd` 文件中，便于按表观察空间占用和重建回收空间。
- 优点是删除表时可以直接释放对应 `.ibd` 文件空间。
- 缺点是大量表会带来更多文件管理开销。
- 缺点是表空间碎片仍然需要重建表才能明显回收。

## 表空间膨胀处理

- 先确认是否真的是表数据膨胀，而不是 binlog、undo、临时文件或错误日志占用。
- 对可归档数据优先业务归档和分区清理，避免单次大删除。
- 删除大量数据后，如果需要归还磁盘空间，可评估 `OPTIMIZE TABLE`、`ALTER TABLE ... ENGINE=InnoDB` 或在线变更工具。
- 对核心大表重建前必须评估 MDL、复制延迟、磁盘临时空间和回滚方案。

## 相关参数

- `innodb_page_size` 初始化实例时确定，常规实例不建议修改默认 16KB。
- `innodb_file_per_table` 决定新建表是否使用独立表空间。
- `innodb_temp_data_file_path` 影响临时表空间文件配置。
