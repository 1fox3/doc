# 基础概念与架构

## 核心组件

- `Producer`：消息生产者，负责选择队列并发送消息。
- `Consumer`：消息消费者，负责拉取或接收消息并提交消费进度。
- `Broker`：消息存储与投递节点，负责写入 CommitLog、构建 ConsumeQueue、处理消费请求。
- `NameServer`：路由中心，负责 Broker 注册、Topic 路由发现和失效剔除。
- `Topic`：消息逻辑分类。
- `MessageQueue`：Topic 下的队列，是并行投递和顺序消息的基础。
- `ConsumerGroup`：消费者组，同组内负载均衡消费。

## 架构链路

1. Broker 启动后向所有 NameServer 注册路由和心跳。
2. Producer 从 NameServer 获取 Topic 路由。
3. Producer 根据路由选择 Broker 和 MessageQueue 发送消息。
4. Broker 写入 CommitLog，并分发 ConsumeQueue 与 IndexFile。
5. Consumer 获取路由后按队列拉取或接收消息。
6. Consumer 处理成功后更新消费进度。

## 适用场景

- 交易、支付、订单等需要可靠异步解耦的业务消息。
- 需要顺序消息、事务消息、延迟消息的场景。
- 需要消费失败重试和死信治理的业务系统。
- 国内 Java 技术栈和阿里云生态中落地成本较低。

## 版本边界

RocketMQ 4.x 以 NameServer、Broker、Client 为主；RocketMQ 5.x 引入 Proxy、gRPC、多协议、Pop 消费、SimpleConsumer 和更云原生的接入层。阅读资料时要区分版本，不要把 5.x Proxy 与 4.x 客户端直连 Broker 的链路混在一起。
