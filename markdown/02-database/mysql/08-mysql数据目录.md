# MySQL数据目录

## 数据目录内容

- `datadir` 保存实例元数据、数据库目录、表空间文件、redo log、undo 表空间、临时文件和系统库。
- MySQL 8.0 将数据字典存储在 InnoDB 中，不再依赖旧版本大量 `.frm` 文件。
- 独立表空间开启时，每张 InnoDB 表通常有对应 `.ibd` 文件。

## 关键文件

- `ibdata1` 可能保存系统表空间、数据字典、change buffer 和部分 undo 数据，取决于版本和配置。
- `#innodb_redo` 或旧版本 `ib_logfile*` 保存 redo log。
- undo 表空间保存事务回滚和 MVCC 所需的旧版本信息。
- `auto.cnf` 保存实例 UUID，复制拓扑中不应多个实例共用同一 UUID。

## 实践要点

- 不要直接复制运行中的数据目录作为备份，容易得到不一致数据；应使用物理热备或逻辑备份工具。
- 迁移数据目录要保证文件权限、SELinux/AppArmor、`datadir`、socket 和日志路径一致。
- 磁盘空间排查重点看 binlog、临时表、undo 膨胀、表空间碎片和错误日志。

```sql
SHOW VARIABLES LIKE 'datadir';
SHOW VARIABLES LIKE 'innodb_file_per_table';
SHOW BINARY LOGS;
```

## 空间占用来源

- binlog 未及时清理会持续占用磁盘，尤其是大事务、批量导入和行格式复制场景。
- 临时表或大排序可能写入临时目录，`tmpdir` 所在磁盘也需要监控。
- undo 表空间可能因长事务无法 purge 而增长。
- 独立表空间删除大量数据后文件不一定变小，需要重建表才能释放给文件系统。

## 迁移注意事项

- 冷迁移必须确保 MySQL 完全停止，并复制完整数据目录、redo、undo、系统表空间和配置。
- 物理热备需要使用支持 InnoDB crash-consistent 的工具，并执行 prepare 阶段。
- 不同 MySQL 大版本之间不能简单复制数据目录升级或降级，必须遵循官方升级路径。
- 复制拓扑中克隆实例后要处理 `server_uuid`，避免主从识别冲突。
