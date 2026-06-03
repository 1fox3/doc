# RocketMQ

> 来源：RocketMQ.xmind

## 核心认知

- RocketMQ 以 NameServer、Broker、Producer、Consumer 为核心，适合金融级可靠消息和事务消息场景。
- 理解 CommitLog、ConsumeQueue、IndexFile 可以帮助解释高吞吐和查询能力。

## 面试重点

- 消息发送、存储、刷盘、主从同步、重试、死信、延迟消息、事务消息。
- 顺序消息与普通消息的队列选择、消费锁和失败重试差异。

## 实践检查点

- 能说明同步刷盘/异步刷盘、同步复制/异步复制对性能和可靠性的影响。
- 能设计事务消息的半消息、回查和本地事务状态处理。

## 版本与趋势

- RocketMQ 5.x 引入 Proxy、Pop 消费、轻量队列等能力，云原生和多协议接入能力增强。
- 事务消息、延迟消息、顺序消息仍是 RocketMQ 区分度较高的面试与落地重点。

## 章节目录

- [源码](01-源码.md)
- [NameServer](02-nameserver.md)
- [消息发送](03-消息发送.md)
- [RocketMQ消息存储](04-rocketmq消息存储.md)
- [消息消费](05-消息消费.md)
- [ACL(访问控制列表)](06-acl访问控制列表.md)
- [主从同步机制](07-主从同步机制.md)
- [消息轨迹](08-消息轨迹.md)
- [主从切换](09-主从切换.md)
- [RocketMQ监控](10-rocketmq监控.md)
- [RocketMQ实战](11-rocketmq实战.md)
