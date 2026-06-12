# 分布式存储：HDFS、对象存储与 HBase

分布式存储负责承载大数据平台的底层数据。HDFS 适合大文件高吞吐读写，对象存储适合云上低成本存储，HBase 适合按 RowKey 的低延迟随机读写。

## HDFS 定位

HDFS 面向大文件、高吞吐、一次写入多次读取的分布式文件系统。

核心角色：

- NameNode：管理命名空间、目录树、文件到 Block 的映射、Block 到 DataNode 的位置。
- DataNode：存储真实数据块，定期向 NameNode 发送心跳和块汇报。
- SecondaryNameNode：辅助 Checkpoint，不是 NameNode 热备。
- JournalNode：HA 模式下保存共享 EditLog。
- ZKFC：基于 ZooKeeper 做 NameNode 主备选举和故障切换。

## HDFS Block 与副本

- 文件会被切分为多个 Block，常见块大小为 128MB 或 256MB。
- 每个 Block 默认 3 副本，副本放置通常跨机架，以平衡可靠性和网络成本。
- Block 较大可以减少 NameNode 元数据压力，并提升顺序读写效率。

## HDFS 写入流程

1. Client 向 NameNode 请求创建文件。
2. NameNode 检查权限和路径，返回可写 DataNode 列表。
3. Client 将数据切成 packet，通过 pipeline 写入多个 DataNode。
4. DataNode 链式复制并逐级 ack。
5. Client 完成所有 Block 后通知 NameNode 关闭文件。

## HDFS 读取流程

1. Client 向 NameNode 获取文件 Block 位置信息。
2. Client 优先选择就近 DataNode 读取。
3. 读取失败时切换到其他副本。
4. NameNode 不参与真实数据传输，只返回元数据。

## HDFS 元数据与高可用

- FsImage：某一时刻完整的文件系统元数据快照。
- EditLog：FsImage 之后的增量变更日志。
- Checkpoint：合并 FsImage 和 EditLog，避免 EditLog 无限增长。
- Active NameNode 处理读写请求，Standby NameNode 同步 EditLog 并保持可切换状态。
- JournalNode 多数派写入和 ZKFC fencing 用于避免脑裂。

## HDFS 小文件问题

每个文件和 Block 都会占用 NameNode 内存元数据。大量小文件会造成 NameNode Heap 压力、RPC 压力和计算任务调度开销。

治理方式：

- 写入端控制滚动文件大小和并发。
- Hive/Spark 定期合并分区文件。
- 使用 CombineInputFormat、SequenceFile、ORC、Parquet 或湖仓表服务。
- 对冷数据使用归档、纠删码或对象存储生命周期策略。

## 对象存储

云上常用 S3、OSS、COS 替代或补充 HDFS。

优势：

- 存储成本低，容量弹性好。
- 运维复杂度低。
- 适合数据湖、归档和冷热分层。

差异与风险：

- rename 成本通常高于 HDFS。
- 元数据列举性能和一致性语义需要关注。
- 与 Hive/Spark/Flink 的提交协议、临时文件和事务语义要适配。
- 权限、审计和跨账号访问需要统一治理。

## HBase 定位

HBase 是基于 HDFS 的分布式列族式宽表 NoSQL 数据库，适合海量稀疏数据和按 RowKey 的低延迟随机读写。

核心角色：

- HMaster：管理表、Region 分配和故障恢复。
- RegionServer：承载 Region，处理读写请求。
- Region：表按 RowKey 范围切分的分片。
- MemStore：内存写缓冲。
- HFile：落盘后的不可变存储文件。
- WAL：预写日志，用于故障恢复。
- ZooKeeper：协调 Master 和 RegionServer 状态。

## HBase 写入与读取

写入流程：

1. Client 根据 RowKey 定位 RegionServer。
2. 写 WAL，保证故障可恢复。
3. 写 MemStore。
4. MemStore 达到阈值后 flush 为 HFile。
5. 后台 Compaction 合并 HFile。

读取流程：

- 先查 MemStore 和 BlockCache。
- 再查 HFile。
- 多版本数据根据时间戳、版本数和 TTL 策略过滤。

## HBase RowKey 设计

RowKey 是 HBase 查询和数据分布的核心。

设计原则：

- 查询优先：RowKey 应匹配最核心的点查和范围扫描路径。
- 离散均匀：避免单调递增导致写热点。
- 长度适中：过长会增加存储、网络和索引成本。
- 保留排序能力：利用字典序支持范围扫描。

常见方案：

- Hash 前缀：对用户 ID、设备 ID 加 hash 前缀打散写入。
- 反转 Key：对手机号、时间戳等单调字段做反转降低热点。
- Salt：加随机或 hash salt 分散 Region。
- 组合 RowKey：例如 `hash(userId)#userId#reverseTs`。
- 预分区：提前按 RowKey 范围拆分 Region，避免初始写热点。

## HBase Compaction 与 Region

- Region 是表按 RowKey 范围切分后的分片，过大时会 split。
- Flush 会把 MemStore 写成 HFile，Flush 过频会产生大量小 HFile。
- Minor Compaction 合并少量小 HFile。
- Major Compaction 合并 Store 下所有 HFile，并清理删除标记和过期版本。

Compaction 能降低读放大，但会消耗 CPU、磁盘 IO 和网络资源。线上需要控制 Major Compaction 时机，避免影响读写延迟。

## 选型建议

- 大规模离线明细和历史归档：HDFS 或对象存储 + ORC/Parquet。
- 多引擎共享数据湖：对象存储/HDFS + Iceberg/Hudi。
- 按用户、设备、账号维度低延迟点查：HBase。
- 多维聚合和报表查询：ClickHouse、Doris、Trino，不应直接用 HBase 承担复杂 OLAP。
