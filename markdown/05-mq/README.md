# MQ

本目录按产品线重组为 Kafka、RocketMQ 和 RabbitMQ 三个部分，仅保留消息中间件技术相关内容。

## 目录

- [Kafka](01-kafka/README.md)：分区日志、生产消费、副本 ISR、存储、KRaft、幂等事务和排障。
- [RocketMQ](02-rocketmq/README.md)：NameServer、发送、存储、消费、重试死信、延迟、顺序、事务、高可用和 5.x。
- [RabbitMQ](03-rabbitmq/README.md)：AMQP、Exchange/Queue/Binding、确认机制、QoS、持久化、死信延迟、队列类型和集群。
- [面试重点](04-面试重点.md)：MQ 通用语义、Kafka、RocketMQ、RabbitMQ 高频问题。
- [排障案例](05-排障案例.md)：消息丢失、重复、堆积、顺序错乱、延迟抖动等场景。

## 选型关注

- 高吞吐事件流、日志采集、流处理输入优先考虑 Kafka。
- 业务消息、事务消息、顺序消息、延迟消息和消费重试治理优先考虑 RocketMQ。
- 复杂路由、任务队列、灵活确认、死信和中小规模业务解耦优先考虑 RabbitMQ。

## 通用设计原则

- 消息系统通常只能提供至少一次投递，业务侧必须设计幂等。
- 可靠性要同时覆盖生产确认、Broker 持久化/复制、消费确认和失败补偿。
- 顺序性一般只在某个分区、队列或业务分组内成立。
- 消息堆积排查要同时看生产速率、消费耗时、分区/队列热点、下游依赖和 Broker 资源。
