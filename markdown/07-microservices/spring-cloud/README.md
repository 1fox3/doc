# Spring Cloud

> 来源：SpringCloud.xmind, 面试内容汇总/Spring Cloud.xmind

## 核心认知

- Spring Cloud 是微服务治理工具集，关注服务注册发现、负载均衡、声明式调用、网关、熔断限流和配置管理。
- 微服务不是简单拆应用，而是围绕团队边界、业务能力、数据自治和故障隔离进行架构设计。

## 面试重点

- 注册发现、Ribbon/LoadBalancer、OpenFeign、Gateway、Hystrix/Resilience4j、配置中心。
- 服务雪崩、超时、重试、熔断、限流、降级和链路追踪。

## 实践检查点

- 能设计合理的超时与重试组合，避免放大故障。
- 能说明微服务拆分后数据一致性、灰度发布和观测性的治理方式。

## 版本与趋势

- Spring Cloud 2023/2024 版本线围绕 Spring Boot 3.x 演进，Netflix 老组件逐步被 Gateway、LoadBalancer、Resilience4j 替代。
- 微服务治理重点转向可观测、弹性、灰度、配置安全、服务网格和平台工程。

## 章节目录

### SpringCloud.xmind

- [微服务](01-微服务.md)
- [Spring Cloud 简介](02-spring-cloud-简介.md)
- [构建微服务准备](03-构建微服务准备.md)
- [Spring Boot](04-spring-boot.md)
- [Eureka](05-eureka.md)
- [Ribbon](06-ribbon.md)
- [声明式调用Feign](07-声明式调用feign.md)
- [熔断器Hystrix](08-熔断器hystrix.md)
- [路由网关Spring Cloud Zuul](09-路由网关spring-cloud-zuul.md)
- [服务网关(Spring Cloud Gateway)](10-服务网关spring-cloud-gateway.md)
- [服务注册和发现Consul](11-服务注册和发现consul.md)
- [配置中心Spring Cloud Config](12-配置中心spring-cloud-config.md)
- [服务链路追踪Spring Cloud Sleuth](13-服务链路追踪spring-cloud-sleuth.md)
- [微服务监控Spring Boot Admin](14-微服务监控spring-boot-admin.md)
- [Spring Boot Security](15-spring-boot-security.md)
- [Spring Cloud OAuth2保护微服务系统](16-spring-cloud-oauth2保护微服务系统.md)
- [使用Spring Security OAuth2 和JWT保护微服务系统](17-使用spring-security-oauth2-和jwt保护微服务系统.md)
- [使用Spring Cloud构建微服务综合案例](18-使用spring-cloud构建微服务综合案例.md)
- [instantiate](19-instantiate.md)
### 面试内容汇总/Spring Cloud.xmind

- [重要组件](20-重要组件.md)
- [版本号](21-版本号.md)
- [基本信息](22-基本信息.md)
- [组件](23-组件.md)
- [Alibaba](24-alibaba.md)
- [instantiate](25-instantiate.md)
