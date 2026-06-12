# Spring Cloud Alibaba

## 组件定位

Spring Cloud Alibaba 将阿里生态组件接入 Spring Cloud 编程模型，常用能力包括 Nacos 注册配置、Sentinel 流量治理、Seata 分布式事务、RocketMQ 消息驱动、Dubbo RPC 和 OSS 对象存储。

选型前必须确认 Spring Boot、Spring Cloud、Spring Cloud Alibaba 与各组件版本兼容矩阵，避免启动失败、配置不生效或运行时协议不兼容。

## Nacos 集成

Nacos 在 Spring Cloud Alibaba 中通常同时承担 DiscoveryClient 和 ConfigService。

关键配置维度：

- 服务注册：服务名、命名空间、Group、集群名、权重、元数据、临时实例标记。
- 配置读取：DataId、Group、Namespace、文件扩展名、共享配置、扩展配置。
- 动态刷新：监听配置变化并刷新 Spring Environment、`@ConfigurationProperties` 或 `@RefreshScope` Bean。

## Sentinel

Sentinel 提供流量控制、熔断降级、系统保护、热点参数限流和实时监控。

核心概念：

- Resource：被保护资源，可以是接口、方法、URL、消息消费逻辑或自定义名称。
- Rule：规则，包括流控规则、熔断规则、热点参数规则、系统规则和授权规则。
- Slot Chain：请求经过一系列 Slot，完成统计、限流、熔断、权限和降级判断。
- Dashboard：控制台用于查看簇点链路、配置规则和实时监控。

规则需要持久化到 Nacos、Apollo、ZooKeeper 或数据库，否则控制台临时规则重启会丢失。

## Seata

Seata 用于处理分布式事务，常见模式包括 AT、TCC、Saga 和 XA。

- AT：业务侵入较低，通过代理数据源记录 undo log，适合关系型数据库的常规本地事务。
- TCC：Try、Confirm、Cancel 三阶段由业务实现，适合资金、库存等强业务语义场景。
- Saga：通过状态机编排多个本地事务和补偿动作，适合长流程、跨系统、最终一致性场景。
- XA：基于数据库 XA 协议，强一致但资源锁持有时间较长，吞吐和可用性成本较高。

## RocketMQ

RocketMQ 常用于异步解耦、削峰填谷、最终一致性、事务消息和事件驱动。

可靠消息设计：

- 生产端发送结果需要落库或结合本地事务，避免业务成功但消息丢失。
- 消费端必须幂等，使用业务唯一键或消息 ID 去重。
- 顺序消息只在同一队列内有序，需要按业务键选择队列。
- 监控消息堆积、消费失败率、重试次数和死信数量。

## Dubbo 与 OSS

Dubbo 适合内部高频低延迟 RPC 调用，支持接口代理、注册发现、负载均衡、集群容错、过滤器和泛化调用。OSS 用于对象存储，微服务中通常只保存对象元数据和访问 URL，不把大文件直接写入业务数据库。
