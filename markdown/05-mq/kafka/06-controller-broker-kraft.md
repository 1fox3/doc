# Controller、Broker 与 KRaft

## Broker 请求处理

Broker 处理生产、拉取、元数据、offset、事务等请求。典型链路包括网络线程接收请求、请求队列分发、I/O 线程处理、响应队列返回结果。

## Controller 职责

- 管理 Broker 上下线。
- 管理 Topic、分区和副本元数据。
- 触发 Leader 选举。
- 处理分区重分配和副本状态变化。
- 维护集群元数据一致性。

## ZooKeeper 架构

早期 Kafka 使用 ZooKeeper 保存集群元数据、Controller 选举和 Broker 注册信息。缺点是双系统运维复杂，元数据规模增大后 Controller 与 ZooKeeper 压力明显。

## KRaft 架构

Kafka 3.x 引入 KRaft 模式，使用 Kafka 自身的 Raft 元数据日志替代 ZooKeeper。KRaft 中 Controller 节点组成 Controller Quorum，通过元数据日志复制保证一致性。

## KRaft 关注点

- 新集群优先使用 KRaft，旧集群迁移需要按官方版本路径规划。
- Controller 节点数量通常配置为奇数。
- Broker 和 Controller 可以共进程，也可以隔离部署；大集群建议隔离角色。
- 运维监控要关注 Controller quorum 状态、元数据日志同步和 Controller 切换频率。

## 延时操作与时间轮

Kafka 内部大量请求并非立即完成，例如等待 ISR 确认的生产请求、等待新数据的拉取请求。Broker 使用延时操作和时间轮机制管理超时与唤醒，避免为大量等待请求创建独立线程。
