# ZNode Session Watcher ACL

## ZNode 类型

- 持久节点：创建后一直存在，直到显式删除。
- 临时节点：与 Session 绑定，Session 过期后自动删除，不能拥有子节点。
- 顺序节点：创建时追加单调递增序号，常用于选主和公平锁。
- 临时顺序节点：同时具备临时和顺序特性，是分布式锁常用节点类型。

## 节点元数据

ZNode 包含数据和状态信息，例如 `czxid`、`mzxid`、`ctime`、`mtime`、`version`、`cversion`、`aversion`、`ephemeralOwner`、`dataLength`、`numChildren`。

版本号可用于 CAS 更新，避免并发写覆盖。更新或删除时带上期望版本，不匹配则失败。

## Session

Session 是客户端与 ZooKeeper 集群之间的逻辑会话。客户端会和某个 Server 保持 TCP 连接，并定期心跳。连接断开后，客户端可在会话超时时间内重连到其他 Server。

关键区别：

- 连接断开：网络连接暂时不可用，Session 可能仍有效，临时节点不会立即删除。
- 会话过期：超过 session timeout 未恢复，Server 判定 Session 失效，临时节点被删除，客户端必须重新创建会话和临时节点。

## Watcher

Watcher 是事件通知机制，用于监听节点创建、删除、数据变化和子节点变化。

特点：

- 一次性触发，收到事件后需要重新注册。
- 只通知发生了变化，不携带完整最新数据，客户端需要主动读取。
- 事件通知可能合并，不能假设每次变化都有一条独立事件。
- 大量 Watcher 会增加服务端内存、网络和事件分发压力。

## 羊群效应

如果大量客户端都监听同一个节点，一次变化会唤醒所有客户端，造成瞬时流量冲击。分布式锁应让每个客户端只监听前一个顺序节点，而不是监听锁根节点。

## ACL

ACL 控制节点访问权限，由 scheme、id、permission 组成。

常见 scheme：

- `world`：开放访问，常见为 `world:anyone`。
- `auth`：已认证用户。
- `digest`：用户名密码摘要。
- `ip`：基于 IP 地址。
- `sasl`：基于 Kerberos 等 SASL 认证。

权限包括 CREATE、READ、WRITE、DELETE、ADMIN。生产环境不应默认开放敏感路径，关键元数据应限制写权限并开启认证。
