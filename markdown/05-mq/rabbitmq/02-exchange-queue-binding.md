# Exchange、Queue 与 Binding

## Exchange 类型

- `direct`：RoutingKey 与 BindingKey 精确匹配。
- `fanout`：忽略 RoutingKey，广播到所有绑定队列。
- `topic`：按通配符匹配路由键，`*` 匹配一个单词，`#` 匹配零个或多个单词。
- `headers`：按消息 headers 匹配，表达能力强但性能较差，使用较少。

## Queue 属性

- `durable`：队列元数据是否持久化。
- `exclusive`：是否只允许当前连接使用，连接关闭后删除。
- `autoDelete`：最后一个消费者取消订阅后是否自动删除。
- `x-message-ttl`：队列内消息 TTL。
- `x-dead-letter-exchange`：死信交换机。
- `x-max-priority`：优先级队列最大优先级。

## Binding 设计

Binding 决定 Exchange 如何把消息路由到 Queue。一个 Exchange 可以绑定多个 Queue，一个 Queue 也可以绑定多个 Exchange。设计时要避免路由规则过度复杂，否则排查消息去向会非常困难。

## mandatory 与 unroutable 消息

生产者发送到 Exchange 后，如果没有任何 Queue 匹配：

- `mandatory=false`：Broker 直接丢弃消息。
- `mandatory=true`：Broker 通过 basic.return 把消息退回生产者。

可靠投递场景应同时使用 Publisher Confirm 和 mandatory return。
