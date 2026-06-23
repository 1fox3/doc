# 分布式技术

本目录按技术体系划分为 Dubbo 和 ZooKeeper 两条主线。仅保留分布式系统工程实践相关内容，删除脑图来源、复习话术、模板占位和非技术内容。

## 目录

- [Dubbo](01-dubbo/README.md)：RPC 框架内核、服务暴露与引用、协议通信、注册发现、集群容错、线程模型和生产治理。
- [ZooKeeper](02-zookeeper/README.md)：一致性协调、ZNode、Session、Watcher、ACL、Leader 选举、ZAB、Curator 和运维排障。
- [面试重点](03-面试重点.md)：RPC、注册发现、一致性、CAP、幂等、分布式锁和协调模型。
- [排障案例](04-排障案例.md)：RPC 超时、注册异常、ZK 会话抖动、Watcher 风暴和脑裂风险。

## 学习重点

- Dubbo 重点理解调用链路：代理生成、服务暴露、服务引用、注册发现、Directory、Router、Cluster、LoadBalance、Filter、Protocol、Invoker。
- ZooKeeper 重点理解协调模型：小数据强一致、顺序一致性、临时节点、顺序节点、Watcher、会话、ZXID、过半机制和 ZAB。
- 生产落地时重点关注超时、重试、幂等、线程池隔离、连接数、序列化兼容、节点数量、Watcher 数量、磁盘延迟和监控告警。
