# Topic、分区与副本

## 分区设计

分区数决定并行度上限，也影响文件句柄、内存、Controller 元数据和 Rebalance 成本。分区数不是越多越好，应结合吞吐、消费者并行度、Broker 数量和未来扩容预留确定。

## 分区数增加的影响

- 可以提升并行消费能力。
- 不会自动重分布历史数据，旧数据仍在原分区。
- 如果使用 key hash，增加分区后 key 到分区的映射可能改变，影响顺序性。
- 分区过多会增加 Leader 选举、Rebalance 和恢复时间。

## 副本机制

- Leader 负责处理读写请求。
- Follower 从 Leader 拉取数据并追加到本地日志。
- ISR 是与 Leader 保持同步的副本集合。
- AR 是所有分配副本，OSR 是不在 ISR 中的落后副本。

## HW、LEO、LSO

- `LEO`：Log End Offset，副本日志下一条待写入 offset。
- `HW`：High Watermark，消费者默认只能读取到 HW 之前的消息。
- `LSO`：Last Stable Offset，事务场景下消费者 `read_committed` 能读取到的稳定位置。

## 可靠性参数组合

- `replication.factor=3` 是常见生产配置。
- `acks=all` 要求 Leader 等待 ISR 中副本确认。
- `min.insync.replicas=2` 能避免只剩 Leader 时仍对外确认成功。
- `unclean.leader.election.enable=false` 可避免选举落后副本导致数据丢失，但可能牺牲可用性。

## 分区热点

热点通常来自 key 分布不均、单个大客户、单个业务类型流量过大或分区数不足。处理方式包括拆 Topic、增加分区、优化 key、对热点 key 做二级散列，以及在消费端隔离慢分区。
