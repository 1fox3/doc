# 客户端 Curator 与典型应用

## 原生客户端

ZooKeeper 原生 Java 客户端提供创建、删除、读取、写入、exists、getChildren、setData、ACL 和 Watcher 等 API。使用原生客户端需要自行处理连接状态、会话过期、重试、Watcher 重新注册和异常恢复。

## Curator

Curator 是 ZooKeeper 的高级客户端，封装了连接管理、重试策略、分布式锁、Leader 选举、缓存和节点监听等能力。生产项目优先使用 Curator，减少重复实现和边界错误。

常用组件：

- CuratorFramework：客户端入口。
- RetryPolicy：重试策略，例如 ExponentialBackoffRetry。
- InterProcessMutex：可重入分布式锁。
- LeaderLatch、LeaderSelector：Leader 选举。
- NodeCache、PathChildrenCache、TreeCache：节点缓存和监听。

## 分布式锁

公平锁常用临时顺序节点实现：

- 客户端在锁路径下创建临时顺序节点。
- 获取子节点列表并按序号排序。
- 如果自己是最小节点，则获得锁。
- 否则监听前一个节点删除事件。
- 释放锁时删除自己的临时顺序节点。

关键点：

- 只监听前一个节点，避免羊群效应。
- 客户端崩溃后 Session 过期，临时节点自动删除。
- 需要支持获取锁超时、异常释放和业务幂等。
- 可重入锁需要在客户端维护线程级持有计数。

## Leader 选举

选主可使用临时顺序节点或 Curator LeaderSelector。Leader 需要定期确认自己仍持有领导权，Session 过期或连接长时间不可用时必须停止执行 Leader 专属任务。

## 配置监听

ZooKeeper 可保存小体积配置元数据，并通过 Watcher 通知变更。客户端收到事件后应重新读取配置并重新注册 Watcher。大配置内容应放在配置中心或对象存储，ZooKeeper 只保存版本和索引。

## 状态处理

客户端必须正确处理连接状态：Connected、Disconnected、Reconnected、Lost。Lost 通常意味着 Session 过期，临时节点、锁和 Leader 身份都需要重新确认或重建。
