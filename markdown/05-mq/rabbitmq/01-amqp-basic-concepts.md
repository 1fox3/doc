# AMQP 基础概念

## 核心对象

- `ConnectionFactory`：客户端连接工厂，负责创建连接。
- `Connection`：TCP 连接，成本较高，通常长连接复用。
- `Channel`：逻辑信道，复用在 Connection 上，大多数发布、消费和确认操作都在 Channel 上完成。
- `Exchange`：交换机，接收生产者消息并根据规则路由。
- `Queue`：队列，保存等待消费的消息。
- `Binding`：交换机和队列之间的绑定关系。
- `RoutingKey`：生产者发送消息时携带的路由键。
- `BindingKey`：绑定时声明的匹配键。
- `Virtual Host`：逻辑隔离空间，用于隔离权限、Exchange、Queue 和 Binding。

## 投递链路

1. Producer 发送消息到 Exchange。
2. Exchange 根据类型、RoutingKey 和 BindingKey 匹配队列。
3. 匹配成功后消息进入一个或多个 Queue。
4. Consumer 从 Queue 获取消息。
5. Consumer ack 后消息从队列删除。

## Channel 使用原则

- Connection 数量不要过多，通常每个应用实例维护少量连接。
- Channel 不建议多线程共享，线程内复用或使用 Channel 池。
- 生产和消费可以使用不同 Channel，避免确认和流控互相影响。

## RabbitMQ 与 Kafka 差异

- RabbitMQ 强调队列和路由，Kafka 强调分区日志。
- RabbitMQ 消息被 ack 后通常从队列删除，Kafka 消息按保留策略保存。
- RabbitMQ 适合复杂业务路由和任务队列，Kafka 适合高吞吐事件流和数据管道。
