# 生产确认与可靠投递

## Publisher Confirm

Publisher Confirm 是生产者确认机制，Broker 在消息被接收并按条件处理后向生产者发送 ack/nack。它比 AMQP 事务模式吞吐更高，是生产可靠投递的主流方案。

## Confirm 与事务模式

- 事务模式：`txSelect`、`txCommit`、`txRollback`，语义清晰但性能差。
- Confirm 模式：异步确认，吞吐高，适合生产环境。

RabbitMQ 的事务不是 RocketMQ 事务消息，不负责协调本地数据库事务和消息最终一致。

## ReturnCallback

Confirm 只能说明消息是否到达 Exchange 或被 Broker 处理，不能说明是否路由到队列。未路由消息需要通过 `mandatory=true` 和 return callback 感知。

## 可靠投递组合

生产端可靠投递通常包括：

- Exchange durable。
- Queue durable。
- Message persistent。
- Publisher Confirm。
- mandatory return。
- 生产端消息表或 outbox 记录发送状态。

## 失败处理

- Confirm nack：记录失败并按策略重试。
- Return：说明路由失败，应检查 Exchange、Binding 和 RoutingKey。
- 超时未确认：不能直接判断失败，需查询或按幂等策略重发。

## 幂等要求

生产者重试可能导致重复投递。消费者必须基于业务唯一键、消息 ID 或去重表实现幂等。
