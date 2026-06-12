# Spring Cloud

Spring Cloud 是围绕 Spring Boot 构建微服务系统的治理工具集，重点解决服务拆分、服务发现、客户端负载均衡、声明式调用、网关、配置管理、熔断限流、安全和可观测性等问题。

## 章节

- [01-微服务架构设计](01-微服务架构设计.md)
- [02-注册发现与负载均衡](02-注册发现与负载均衡.md)
- [03-服务调用与网关](03-服务调用与网关.md)
- [04-弹性治理与可观测性](04-弹性治理与可观测性.md)
- [05-安全与一致性](05-安全与一致性.md)
- [06-Spring Cloud Alibaba](06-spring-cloud-alibaba.md)

## 技术演进

- Ribbon、Hystrix、Zuul、Spring Cloud Sleuth 属于老组件，新项目通常使用 Spring Cloud LoadBalancer、Resilience4j 或 Sentinel、Spring Cloud Gateway、Micrometer Tracing。
- Spring Cloud 2023/2024 版本线围绕 Spring Boot 3.x 演进，需要关注 Jakarta 包名、Actuator、Micrometer、Observability 和原 Netflix 组件替代方案。
- Spring Cloud Alibaba 需要严格匹配 Spring Boot、Spring Cloud、Nacos、Sentinel、Seata 等版本兼容矩阵。

## 生产关注点

- 每个远程调用必须有连接超时、读取超时、总耗时预算和明确重试策略。
- 网关只承载通用入口能力，不应堆积复杂业务编排。
- 配置中心和注册中心必须高可用部署，并开启权限、审计、备份和回滚能力。
- 核心链路必须具备 TraceId、结构化日志、指标、链路追踪和告警规则。
- 跨服务写操作需要幂等、消息可靠性、补偿任务和对账机制。
