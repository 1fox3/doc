# 运行ZooKeeper

> 专题：ZooKeeper
> 来源：ZooKeeper.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 是什么

- `运行ZooKeeper` 是 `ZooKeeper` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `运行ZooKeeper` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `运行ZooKeeper`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `运行ZooKeeper` 展开，属于 `ZooKeeper` 的复习范围。
- 建议优先掌握：配置ZooKeeper服务器, 配置ZooKeeper集群, 重配置。
- 二级节点提示了主要拆分角度：基本配置, 存储配置, 网络配置, 集群配置, 认证和授权, 非安全配置, 日志, group.x=n[:n], dynamicConfigFile, server.id=host:n:n[:role];[client_address:]client_port。
- 三级节点通常对应具体细节、API、机制或易错点：clientPort, dataDir, dataLogDir, tickTime, preAllocSize, snapCount, autopurge.snapRetainCount, autopurge.purgeInterval, fsync.warningthresholdms, weight.x=n。

### 复习追问

- `配置ZooKeeper服务器` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `配置ZooKeeper集群` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `重配置` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## 运行ZooKeeper

### 配置ZooKeeper服务器

#### 基本配置

- clientPort
  - 默认2181

- dataDir

- dataLogDir

- tickTime

#### 存储配置

- preAllocSize
  - 预分配的事务日志文件的大小
  - 默认64MB

- snapCount
  - 每次快照之间的事务数
  - 默认10万

- autopurge.snapRetainCount
  - 清理数据操作时，需要保留在快照数量和对应事务日志文件数量
  - 默认3

- autopurge.purgeInterval
  - 对快照和日志进行垃圾回收清理操作的时间间隔小时数

- fsync.warningthresholdms
  - 触发告警的存储同步时间阈值，单位毫秒

- weight.x=n
  - 权重

- traceFile
  - 持续跟踪ZooKeeper的操作，并将操作记录到跟踪日志中
  - 跟踪日志文件名：traceFile.year.month.day

#### 网络配置

- globalOutstandingLimit
  - 待处理请求的最大值
  - 默认1000

- maxClientCnxns
  - 允许每个IP地址的并发socket连接的最大数量
  - 默认60

- clientPortAddress
  - 限制客户端连接到指定的接受信息的地址上

- minSessionTimeout
  - 最小会话超时时间，单位毫秒

- maxSessionTimeout
  - 最大会话超时时间，单位毫秒

#### 集群配置

- initLimit
  - 追随者最初连接到群首的超时值，单位为tick值得倍数

- syncLimit
  - 对于追随者与群首进行sync操作时的超时值，单位为tick值的倍数

- leaderServers
  - 群首是否为客户端提供服务

- server.x=[hostname]:n:n[:observer]
  - 端口号
    - 事务发送
    - 群首选举

- cnxTimeout
  - 在群首打开一个新的连接的超时值

- electionAlg
  - 选举算法

#### 认证和授权

#### 非安全配置

- forceSync
  - 控制是否将数据同步到存储设备上

- jute.maxbuffer
  - 一个请求或响应的最大值，单位字节

- skipACL
  - 跳过所有ACL检查

- readonlymode.enabled
  - true则开启服务器只读模式功能

#### 日志

### 配置ZooKeeper集群

#### group.x=n[:n]

#### weight.x=n

### 重配置

#### dynamicConfigFile

#### server.id=host:n:n[:role];[client_address:]client_port

#### reconfig操作

- -remove

- -add

- -file

- -members

#### 只有仲裁模式才支持重配置功能

### 配额管理

#### znode节点数量和节点数据大小配置

#### /zookeeper/quota节点就是管理配额的节点

#### zookeeper_limits（告警触发界别）

- count=n
  - 节点数量

- bytes=m
  - 节点数据大小

#### zookeeper_stats（当先子树节点和数据大小统计）

- count=n
  - 节点数量

- bytes=m
  - 节点数据大小

### 多租赁配置

### 文件系统布局和格式

### 四字母命令

#### ruok

- 提供服务器的状态信息

#### stat

- 提供服务器的状态信息和当前活动的连接情况

#### srvr

- 类似stat

#### dump

- 提供会话信息

#### conf

- 列出启动时所使用的基本配置参数

#### envi

- 列出java环境参数

#### mntr

- 提供了比stat更详细的服务器统计数据

#### wchs

- 服务器所跟踪的监视点的简短摘要信息

#### wchc

- 服务器所跟踪的监视点的详细信息，并根据会话分组

#### wchp

- 服务器所跟踪的监视点的详细信息，并根据znode节点路径分组

#### cons，crst

- cons列出该服务器上每个连接的详细统计信息，crst重置这些连接信息中的技术器为0
