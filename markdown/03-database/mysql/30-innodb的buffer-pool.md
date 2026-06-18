# InnoDB的Buffer Pool

## 缓存内容

- 数据页和索引页。
- undo 页和插入缓冲相关页。
- 自适应哈希索引和锁信息等内存结构。

## LRU 管理

- Buffer Pool 使用改进 LRU，分为 young 和 old 两段。
- 新读入页先进入 old 区，短时间内再次访问才更可能晋升，避免大扫描污染热点数据。
- 脏页进入 Flush 链表，由后台线程根据 checkpoint 和脏页比例刷盘。

## 性能关注

- 命中率低可能意味着内存不足、热点数据过大或扫描型查询污染缓存。
- 脏页过多可能导致查询线程参与刷盘，表现为抖动。
- redo 容量过小会迫使更频繁 checkpoint，增加刷盘压力。

```sql
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_read%';
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_pages%';
SHOW ENGINE INNODB STATUS\G
```

## 关键状态指标

- `Innodb_buffer_pool_read_requests` 表示逻辑读请求。
- `Innodb_buffer_pool_reads` 表示需要从磁盘读取的次数。
- `Innodb_buffer_pool_pages_dirty` 表示脏页数量。
- `Innodb_buffer_pool_wait_free` 如果持续增长，说明申请空闲页时发生等待。

## 问题判断

- 逻辑读很高但磁盘读低，说明主要命中内存，瓶颈可能在 CPU 或 SQL 执行效率。
- 磁盘读持续高，说明工作集超过缓存或存在大扫描。
- 脏页高且写入抖动，检查刷盘能力、redo checkpoint 和存储延迟。
- Buffer Pool 不是越大越好，过大可能挤压 OS、连接线程和其他进程内存。
