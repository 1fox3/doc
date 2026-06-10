# Spring Boot 升级路线

Spring Boot 升级不能只改版本号，要按依赖、配置、代码、测试、压测和灰度逐步推进。

## 推荐路线

### 1.x 到 2.x

重点检查：

- Spring Framework 5 兼容性。
- Actuator endpoint 变化。
- Spring Security 配置。
- 第三方 Starter 版本。
- Micrometer 指标接入。

### 2.0-2.3 到 2.7

建议先升级到 2.7，作为进入 3.x 前的过渡版本。

重点检查：

- 配置属性废弃项。
- 循环依赖。
- 路径匹配策略。
- Spring Security 新写法。
- Spring Cloud 版本矩阵。

### 2.7 到 3.x

重点检查：

- JDK 升级到 17+。
- `javax.*` 到 `jakarta.*`。
- 第三方库是否支持 Jakarta。
- Spring Security 配置迁移。
- 自动配置声明方式。
- 观测链路从 Sleuth 迁移到 Micrometer Tracing/OpenTelemetry。

## 升级前清单

- 梳理 Spring Boot、Spring Cloud、JDK、Tomcat/Jetty、ORM、连接池、日志、监控 Agent 版本。
- 检查 Spring Boot 官方 compatibility matrix。
- 扫描废弃配置和废弃 API。
- 梳理自定义 Starter 和自动配置。
- 准备回滚方案。

## 升级中检查

- 编译错误。
- 单元测试和集成测试。
- 启动日志中的 deprecated 配置。
- 自动配置条件报告。
- Actuator endpoint 是否正常。
- 接口兼容性。

## 升级后验证

- 核心接口 P95/P99。
- JVM GC 和内存。
- 线程池、连接池和请求错误率。
- 日志、指标、链路追踪。
- 灰度流量和回滚演练。

## 面试回答模板

如果被问 Spring Boot 升级，我会先说明目标版本和原因，再讲风险点：依赖兼容、配置变化、自动配置变化、Jakarta 迁移、Security 迁移和观测链路变化。执行上按“依赖扫描 -> 编译修复 -> 自动化测试 -> 压测 -> 灰度 -> 回滚预案”推进。
