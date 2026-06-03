# HBase

HBase 是基于 HDFS 的分布式、列族式、宽表 NoSQL 数据库，适合海量稀疏数据和按 RowKey 的低延迟随机读写。

## 核心架构

- HMaster：管理表、Region 分配、故障恢复。
- RegionServer：承载 Region，处理读写请求。
- Region：表按 RowKey 范围切分的分片。
- MemStore：内存写缓冲。
- HFile：落盘后的不可变存储文件。
- WAL：预写日志，用于故障恢复。
- ZooKeeper：协调 Master、RegionServer 状态。

## 写入流程

1. Client 根据 RowKey 定位 RegionServer。
2. 写 WAL，保证故障可恢复。
3. 写 MemStore。
4. MemStore 达到阈值 flush 为 HFile。
5. 后台执行 Compaction 合并 HFile。

## 读取流程

- 先查 MemStore 和 BlockCache。
- 再查 HFile。
- 多版本数据根据时间戳和版本策略过滤。

## 适合场景

- 用户画像宽表。
- 设备/账号维度明细查询。
- 风控特征存储。
- 海量稀疏 KV 数据。

## 不适合场景

- 复杂 SQL 查询。
- 多字段任意组合查询。
- 强事务关系模型。
- 高效聚合分析。

## 相关文档

- [RowKey 设计](rowkey-design.md)
