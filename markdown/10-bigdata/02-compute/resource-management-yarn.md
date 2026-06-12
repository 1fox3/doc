# 资源管理：YARN 与多租户调度

YARN 是 Hadoop 生态中的资源管理和任务调度系统，用于统一管理 CPU、内存等资源，并调度 MapReduce、Spark、Flink 等应用。

## 核心角色

- ResourceManager：全局资源管理和调度。
- NodeManager：单节点资源管理、容器启动、资源上报和日志管理。
- ApplicationMaster：每个应用一个，负责应用内部任务调度和状态协调。
- Container：资源分配单位，包含 CPU、内存等资源描述。

## 任务提交流程

1. Client 提交应用到 ResourceManager。
2. ResourceManager 分配第一个 Container 启动 ApplicationMaster。
3. ApplicationMaster 向 ResourceManager 申请更多 Container。
4. NodeManager 在对应节点启动任务。
5. ApplicationMaster 跟踪任务状态并完成应用。

ResourceManager 管全局资源，不负责每个 Task 的细粒度调度；ApplicationMaster 是应用级调度核心。

## 调度器

- FIFO Scheduler：按提交顺序执行，简单但不适合多租户。
- Capacity Scheduler：按队列容量分配资源，适合多部门共享集群。
- Fair Scheduler：尽量让任务公平获得资源。

## 多租户资源治理

- 队列隔离：不同业务线、环境、优先级使用不同队列。
- 资源上限：限制单队列、单用户最大资源占用。
- 最小保障：核心链路队列保留基础资源。
- 优先级：重要任务优先调度。
- 抢占：低优任务释放资源给高优任务。
- ACL：限制用户提交、查看和管理队列的权限。

## 常见问题

任务长时间 ACCEPTED：

- 队列资源不足。
- AM 资源不足。
- 队列最大应用数或用户资源限制。
- 节点标签、资源类型或队列权限不匹配。

Container 被 kill：

- 物理内存或虚拟内存超限。
- 节点磁盘异常。
- NodeManager 健康检查失败。
- 外部依赖导致任务超时。

资源利用率低：

- 队列容量配置不合理。
- 小任务过多，调度开销高。
- 数据倾斜导致少数任务拖尾。
- Executor/Container 规格过大，资源碎片严重。

## 与 Spark/Flink 的关系

- Spark on YARN 由 Driver 或 ApplicationMaster 协调 Executor 申请。
- Flink on YARN 由 Flink 集群组件运行在 YARN Container 中。
- YARN 管资源，Spark/Flink 管应用内部 DAG、Task 和状态。

## 工程实践

- 离线、实时、Ad-hoc、补数任务使用不同队列。
- 补数和历史重算要限流，避免影响核心实时链路。
- 为核心任务设置最小保障和告警。
- 采集队列维度的 CPU、内存、等待时间、失败率和利用率。
- 对异常大资源任务建立审批或自动诊断机制。
