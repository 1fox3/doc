# RocketMQ 5.x 要点

## Proxy

RocketMQ 5.x 引入 Proxy 接入层，客户端可通过 Proxy 访问集群，降低客户端与 Broker 拓扑的耦合。Proxy 也为多语言、gRPC 和云原生接入提供基础。

## 消费模型

- PushConsumer：面向持续消费，框架封装拉取与回调。
- SimpleConsumer：应用主动接收、确认和控制不可见时间，适合更明确的消费控制。
- Pop 消费：通过消息不可见时间减少传统队列锁和重试复杂度。

## MessageGroup

MessageGroup 用于表达同一分组消息的顺序关系，是 5.x 顺序消息实践中的重要概念。它和 4.x 中使用 MessageQueueSelector 固定队列的思路类似，但接入模型更面向业务分组。

## 定时/延时消息

5.x 对定时/延时能力做了增强，比 4.x 固定延迟级别更灵活。设计时仍要评估消息规模、最大延迟时间、精度要求和 Broker 存储压力。

## 迁移关注

- 客户端 SDK、协议和接入方式变化。
- Proxy 部署容量和高可用。
- 4.x 顺序、事务、延迟语义与 5.x API 的映射。
- 监控、ACL、限流和灰度发布策略。
