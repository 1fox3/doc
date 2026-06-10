# Spring Boot 1.x 到 2.x

Spring Boot 2.0 是一次重要版本升级，底层升级到 Spring Framework 5，引入响应式编程支持，并重构了 Actuator 和监控体系。

## 基线变化

- Spring Boot 1.x 基于 Spring Framework 4.x。
- Spring Boot 2.0 基于 Spring Framework 5.x。
- Java 基线从 Java 7/8 时代逐步转向 Java 8+。

## WebFlux

Spring Boot 2.0 引入对 Spring WebFlux 的自动配置支持。

WebFlux 特点：

- 基于 Reactor。
- 支持非阻塞响应式编程模型。
- 可运行在 Netty、Servlet 3.1+ 容器上。

适合场景：

- 高并发 IO。
- 流式响应。
- API Gateway。

不适合场景：

- 传统阻塞 JDBC 调用较多的业务系统。
- 团队不熟悉响应式链路和调试方式。

## Actuator 2 重构

Spring Boot 2 对 Actuator 做了较大调整：

- endpoint 路径从 `/metrics` 等变化为 `/actuator/metrics` 等。
- 暴露端点需要显式配置。
- Endpoint 注解模型变化。
- 安全配置方式变化。

常用配置：

```properties
management.endpoints.web.exposure.include=health,info,metrics,prometheus
```

## Micrometer

Spring Boot 2 引入 Micrometer 作为指标门面。

它的定位类似日志中的 SLF4J：

- 应用使用统一指标 API。
- 后端可接 Prometheus、Datadog、Graphite、InfluxDB 等。

## 配置属性绑定变化

Spring Boot 2 增强了 Binder 机制和类型安全配置绑定。

常用方式：

```java
@ConfigurationProperties(prefix = "app")
public class AppProperties {
    private String name;
}
```

## 迁移注意事项

- Actuator endpoint 路径和暴露配置变化。
- Spring Security 配置方式变化。
- 部分自动配置属性名变化。
- 第三方 Starter 需要确认是否兼容 Boot 2。
- 响应式和 Servlet 栈不要混用到难以维护。

## 面试回答模板

Spring Boot 2 相比 1.x 的核心变化是升级到 Spring 5，引入 WebFlux 响应式支持，Actuator 端点模型重构，并引入 Micrometer 作为统一指标门面。升级时要重点检查 Actuator 路径、安全配置、配置属性和第三方 Starter 兼容性。
