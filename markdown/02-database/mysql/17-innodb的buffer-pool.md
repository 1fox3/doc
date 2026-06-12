# InnoDB的Buffer Pool

## 作用

- Buffer Pool 是 InnoDB 的核心内存缓存，缓存数据页、索引页、undo 页、自适应哈希索引等数据结构。
- 读请求优先访问 Buffer Pool，未命中时从磁盘读取页并放入缓存。
- 写请求通常先修改内存页形成脏页，再由后台线程刷盘，通过 redo log 保证崩溃恢复。

## 管理机制

- 页以控制块和缓存页形式管理，缓存页按 LRU 链表、Free 链表和 Flush 链表组织。
- InnoDB 使用改进 LRU，将链表分为 young 和 old 区，减少全表扫描污染热点页。
- 脏页刷盘受 redo log 压力、脏页比例、checkpoint 推进和后台刷盘线程影响。

## 关键参数

- `innodb_buffer_pool_size`：Buffer Pool 总大小，专用数据库服务器通常配置为物理内存的 60% 到 75%。
- `innodb_buffer_pool_instances`：大 Buffer Pool 可拆分多个实例降低互斥竞争。
- `innodb_old_blocks_pct`、`innodb_old_blocks_time`：控制 LRU old 区比例和晋升策略。
- `innodb_flush_neighbors`：SSD 场景通常关闭邻近页刷盘。

## 监控和排查

```sql
SHOW ENGINE INNODB STATUS\G
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool%';
SHOW VARIABLES LIKE 'innodb_buffer_pool%';
```

关注命中率、脏页比例、Free pages、Pages made young、redo checkpoint age 和磁盘 I/O 延迟。

## 读写路径

- 读页时先在 Buffer Pool 查找页号，命中则直接返回内存页。
- 未命中时从磁盘读取 16KB 页放入 Buffer Pool，必要时淘汰冷页。
- 修改记录时先修改 Buffer Pool 中的页，并把页标记为脏页。
- 脏页不会每次提交都刷盘，而是由后台线程按 checkpoint、脏页比例和 I/O 能力异步刷新。

## LRU 污染问题

- 全表扫描或大范围索引扫描会读取大量冷页。
- 如果冷页直接进入 LRU 热端，会挤出热点业务页，导致后续热点查询频繁磁盘读。
- InnoDB 将新读入页放入 old 区，只有在一定时间后再次访问才晋升，降低扫描污染。
- 对报表类大查询，应考虑只读副本、限流、分批和覆盖索引，避免冲击主库缓存。

## 调优思路

- 命中率低但内存充足时，可增大 `innodb_buffer_pool_size`。
- 脏页刷盘抖动时，检查 redo 容量、`innodb_io_capacity`、磁盘延迟和 checkpoint age。
- 大量 `Free buffers` 很低不一定是问题，Buffer Pool 正常会尽量用满；关键看是否频繁等待 free page。
- 多实例混部时，不要让多个实例 Buffer Pool 总和接近物理内存，避免 OS swap。
