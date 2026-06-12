# NameServer

## 职责

- 接收 Broker 注册和心跳。
- 保存 Topic 到 Broker、Queue 的路由信息。
- 为 Producer 和 Consumer 提供路由查询。
- 根据心跳超时剔除不可用 Broker。

## 设计特点

- NameServer 节点之间不通信，部署多个节点提升可用性。
- Broker 向所有 NameServer 注册，客户端也会从多个 NameServer 查询路由。
- 路由信息是最终一致的，短时间内不同 NameServer 看到的路由可能不同。
- NameServer 不在消息读写主链路上，消息发送和消费直接访问 Broker。

## Broker 注册信息

Broker 会注册：

- BrokerName、BrokerId、ClusterName。
- Broker 地址。
- Topic 配置和队列数量。
- 读写权限。
- 心跳时间戳。

## 故障影响

- 少数 NameServer 故障：客户端可切换其他节点，已缓存路由仍可短期使用。
- 全部 NameServer 故障：已有客户端短期还能按缓存路由收发，新增 Topic、Broker 变更和新客户端发现会受影响。
- Broker 故障：NameServer 通过心跳超时剔除路由，客户端刷新路由后避开故障节点。

## 实践建议

- NameServer 至少部署 2 到 3 个节点。
- 客户端配置多个 NameServer 地址。
- 监控 Broker 心跳、路由变更频率和客户端路由刷新异常。
