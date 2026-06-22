# ZAB Leader 选举与一致性

## ZXID

ZXID 是 ZooKeeper 事务 ID，保证全局递增和顺序。高位通常表示 epoch，低位表示该 epoch 内事务序号。Leader 变更后 epoch 增加，用于区分不同 Leader 任期。

## ZAB 协议

ZAB 是 ZooKeeper 的原子广播协议，负责写请求复制、顺序一致性和崩溃恢复。

工作模式：

- 崩溃恢复：选出 Leader，并确保新 Leader 拥有被多数派确认的最新事务。
- 消息广播：Leader 接收写请求，将事务 proposal 广播给 Follower，多数派 ack 后提交。

## 写请求流程

- Client 将写请求发送到任意 Server。
- Follower 会把写请求转发给 Leader。
- Leader 生成事务 proposal 和 ZXID。
- Follower 写入事务日志并返回 ack。
- Leader 收到多数派 ack 后提交事务。
- Leader 通知 Follower commit，客户端收到成功响应。

## Leader 选举

Leader 选举通常比较 epoch、ZXID 和 server id。拥有更新数据的节点优先成为 Leader；数据进度相同则 server id 更大的节点优先。

选举要求多数派参与，因此集群通常部署奇数个节点。3 节点最多容忍 1 个节点故障，5 节点最多容忍 2 个节点故障。

## 过半机制

ZooKeeper 写入需要多数派确认。过半机制保证任意两个多数派集合必然有交集，从而避免两个 Leader 同时提交互相冲突的事务。

## 读一致性

默认读请求可由当前连接的 Server 直接返回，因此可能读到稍旧数据。需要更强读一致性时，可以在读前调用 `sync`，让当前 Server 与 Leader 同步到较新状态后再读。

## 脑裂与少数派

网络分区时，只有多数派分区能继续对外提供写服务。少数派节点不能提交写请求，避免脑裂。客户端连接到少数派时会出现不可用或重连，需要客户端具备重试和状态恢复逻辑。
