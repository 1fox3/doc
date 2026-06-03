# Leader选举

> 专题：ZooKeeper
> 来源：面试内容汇总/ZooKeeper.xmind

## 补充与实践

- 补充：ZooKeeper 强在小数据协调和顺序一致性，不适合高频大数据读写。
- 实践：分布式锁使用临时顺序节点并监听前一个节点，避免所有客户端监听同一节点造成羊群效应。
- 排障：连接抖动时重点检查 GC 停顿、网络延迟、磁盘 IO 和 session timeout 配置。

## 脑图内容

## Leader选举

### 节点状态

#### LOOKING

#### FOLLOWING

#### LEADING

#### OBSERVING

### 选举方式

#### LeaderElection

#### AuthFastLeaderElection

#### FastLeaderElection(最新默认)

### 群首选举

#### 投票信息（vote）

- 服务器表示符（sid）

- 最近执行的事务的zxid信息

#### 优先选举zxid大的，其次是sid大的
