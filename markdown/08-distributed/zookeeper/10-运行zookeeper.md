# 运行ZooKeeper

> 专题：ZooKeeper
> 来源：ZooKeeper.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

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
