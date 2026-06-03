# YARN

YARN 是 Hadoop 的资源管理和任务调度系统，用于在集群中统一管理 CPU、内存等资源，并调度 MapReduce、Spark、Flink 等任务。

## 核心角色

- ResourceManager：全局资源管理和调度。
- NodeManager：单节点资源管理、容器启动、资源上报。
- ApplicationMaster：每个应用一个，负责应用内部任务调度和状态协调。
- Container：资源分配单位，包含 CPU、内存等资源描述。

## 任务提交流程

1. Client 提交应用到 ResourceManager。
2. ResourceManager 分配第一个 Container 启动 ApplicationMaster。
3. ApplicationMaster 向 ResourceManager 申请更多 Container。
4. NodeManager 在对应节点启动任务。
5. ApplicationMaster 跟踪任务状态并完成应用。

## 调度器

- FIFO Scheduler：按提交顺序执行，简单但不适合多租户。
- Capacity Scheduler：按队列容量分配资源，适合多部门共享集群。
- Fair Scheduler：尽量让任务公平获得资源。

## 资源治理

- 队列隔离：不同业务线配置不同资源队列。
- 资源上限：限制单队列、单用户最大资源占用。
- 优先级：重要任务优先调度。
- 抢占：低优任务释放资源给高优任务。

## 常见问题

- 任务长时间 ACCEPTED：队列资源不足、AM 资源不足或队列限制。
- Container 被 kill：内存超限、节点异常、磁盘问题。
- 资源利用率低：队列配置不合理、小任务过多、数据倾斜。

## 面试重点

- ResourceManager 管全局资源，不负责每个 Task 的细粒度调度。
- ApplicationMaster 是应用级调度核心。
- YARN 通过 Container 抽象资源，支持多计算框架共存。
