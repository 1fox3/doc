# HBase Compaction 与 Region

HBase 的性能和稳定性很大程度取决于 Region 分布、MemStore flush、HFile 数量和 Compaction。

## Region

Region 是 HBase 表按 RowKey 范围切分后的分片。

- 一个表由多个 Region 组成。
- Region 分布在多个 RegionServer 上。
- Region 过大时会 split。
- Region 分布不均会导致热点。

## Flush

写入先进入 MemStore 和 WAL。当 MemStore 达到阈值时，会 flush 成 HFile。

Flush 太频繁会产生大量小 HFile，增加 Compaction 压力。

## Compaction

Compaction 是合并 HFile 的后台过程。

- Minor Compaction：合并少量小 HFile。
- Major Compaction：合并一个 Store 下所有 HFile，并清理删除标记和过期版本。

## Compaction 影响

- 降低读放大。
- 清理删除和过期数据。
- 但会消耗 CPU、磁盘 IO 和网络资源。
- Major Compaction 过重可能影响线上读写。

## 热点问题

原因：

- RowKey 单调递增。
- 热点用户或热点设备集中写入。
- Region 未预分区。

解决：

- 预分区。
- RowKey 加 salt/hash。
- 热点 key 拆分。
- 调整 Region 大小和 split 策略。

## 面试重点

HBase 写入快是因为先写 WAL 和 MemStore，但后台 flush 和 compaction 如果治理不好，会转化为读放大、写放大和 IO 抖动。
