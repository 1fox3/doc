# HDFS

HDFS 是 Hadoop Distributed File System，面向大文件、高吞吐、一次写入多次读取的分布式文件系统。

## 核心架构

- NameNode：管理文件系统命名空间、目录树、文件到 Block 的映射、Block 到 DataNode 的位置。
- DataNode：存储真实数据块，定期向 NameNode 发送心跳和块汇报。
- SecondaryNameNode：负责辅助 Checkpoint，不是 NameNode 的热备。
- JournalNode：HA 模式下保存共享 EditLog。
- ZKFC：基于 ZooKeeper 做 NameNode 主备选举和故障切换。

## Block 机制

- HDFS 文件会被切分为多个 Block，常见块大小是 128MB 或 256MB。
- 每个 Block 默认 3 副本，副本放置通常跨机架，兼顾可靠性和网络成本。
- Block 大可以减少 NameNode 元数据压力，也适合顺序读写。

## 写入流程

1. Client 向 NameNode 请求创建文件。
2. NameNode 检查权限和路径，返回可写 DataNode 列表。
3. Client 将数据切成 packet，通过 pipeline 写入多个 DataNode。
4. DataNode 按链式复制写入并逐级 ack。
5. Client 完成所有 Block 后通知 NameNode 关闭文件。

## 读取流程

1. Client 向 NameNode 获取文件 Block 位置信息。
2. Client 优先选择就近 DataNode 读取。
3. 读取失败时切换到其他副本。
4. NameNode 不参与真实数据传输，只返回元数据。

## 元数据机制

- FsImage：某一时刻完整的文件系统元数据快照。
- EditLog：FsImage 之后的增量变更日志。
- Checkpoint：合并 FsImage 和 EditLog，避免 EditLog 无限增长。

## 高可用

- Active NameNode 处理读写请求。
- Standby NameNode 同步 EditLog 并维护接近实时的元数据状态。
- JournalNode 保存共享日志，通常要求多数派写入成功。
- ZKFC 负责健康检查、主备选举和 fencing，避免脑裂。

## 小文件问题

- 每个文件和 Block 都会占用 NameNode 内存元数据。
- 大量小文件会导致 NameNode 内存压力、RPC 压力和任务调度开销。
- 解决方案：SequenceFile、HAR、CombineInputFormat、合并入 Hive 分区、使用对象存储或湖仓表格式治理。

## 容错机制

- 心跳：判断 DataNode 是否存活。
- 块汇报：同步 DataNode 上的 Block 列表。
- 副本恢复：副本数低于阈值时自动复制。
- 安全模式：NameNode 启动后等待足够 Block 汇报，期间限制写操作。

## 新特性与趋势

- Federation：多个 NameNode 管理不同命名空间，缓解单 NameNode 元数据瓶颈。
- Erasure Coding：纠删码降低存储成本，适合冷数据。
- 对象存储替代：云上常用 S3/OSS/COS 替代 HDFS，但一致性、rename 成本和元数据能力不同。

## 面试重点

- SecondaryNameNode 不是热备。
- NameNode 内存决定可管理文件数量上限。
- HDFS 适合大文件顺序读写，不适合低延迟随机读写和大量小文件。
- HDFS HA 依赖 JournalNode、ZooKeeper 和 fencing。

## 项目表达

可以这样说：日志原始数据先落 HDFS 的 ODS 层，按日期和业务线分区；小文件通过定时合并治理；冷热数据用不同副本策略或纠删码降低成本；NameNode 监控关注 Heap、RPC 延迟、Block 数量和 Under Replicated Blocks。
