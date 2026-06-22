# 工作模式与路由

## 简单模式

一个生产者、一个队列、一个消费者。适合最简单的异步任务，不需要显式声明复杂交换机。

## Work Queue

一个队列绑定多个消费者，一条消息只会被其中一个消费者处理。适合任务分发和水平扩展。配合手动 ack 和 prefetch 可以避免慢消费者堆积过多未确认消息。

## Publish/Subscribe

使用 fanout exchange 广播到多个队列，每个队列对应一类订阅者。适合事件通知、缓存刷新、多系统同步。

## Routing

使用 direct exchange 根据 RoutingKey 精确路由。适合按级别、业务类型或租户分发消息。

## Topic

使用 topic exchange 按模式匹配路由键。适合多维度事件路由，例如 `order.created.eu`、`order.paid.cn`。

## RPC 模式

RabbitMQ 可以通过 reply queue 和 correlationId 实现 RPC，但生产环境要谨慎。消息队列更适合异步解耦，强同步请求优先使用 HTTP/gRPC。
