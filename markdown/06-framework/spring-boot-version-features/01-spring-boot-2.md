# Spring Boot 2.x 关键变化

## 基础依赖

Spring Boot 2.x 基于 Spring Framework 5，最低 Java 版本从 Java 7/8 逐步提升。升级时需要同步检查 Spring Data、Spring Security、Hibernate、Tomcat、Jackson、Micrometer 等依赖版本。

## WebFlux

Boot 2 引入对 Spring WebFlux 的自动配置支持。WebFlux 基于 Reactive Streams，适合高并发 I/O、流式处理和响应式数据链路。传统 Servlet MVC 项目不应仅为追新迁移到 WebFlux，除非调用链路和驱动都能支持非阻塞。

## Actuator 2

Actuator 2 重构端点模型，端点路径、暴露配置和响应结构与 1.x 有明显差异。

常见变化：

- 默认基础路径为 `/actuator`。
- 端点暴露需要通过 `management.endpoints.web.exposure.include` 配置。
- 健康检查细节需要显式配置显示策略。
- 指标体系整合 Micrometer。

## Micrometer

Boot 2 使用 Micrometer 作为指标门面，可对接 Prometheus、Graphite、Datadog、Influx 等监控系统。

指标设计要点：

- tag 维度不能无限增长，避免用户 ID、订单 ID 等高基数字段。
- 业务指标应明确名称、单位、标签和采样位置。
- HTTP、JVM、连接池、线程池、数据库等基础指标应统一接入。

## ConfigData

Boot 2.4 引入 ConfigData 机制，改变配置文件加载方式。`spring.config.import` 用于导入额外配置源。

升级影响：

- `bootstrap.yml` 行为可能变化，尤其是 Spring Cloud 项目。
- Profile 激活和包含规则需要重新检查。
- 配置文件导入顺序会影响覆盖关系。
- 配置中心客户端版本必须与 Boot 版本匹配。

## 路径匹配策略

Boot 2.6 默认路径匹配从 AntPathMatcher 转向 PathPatternParser。部分依赖 Ant 风格细节的路径、拦截器、Swagger 或 Springfox 可能出现兼容问题。

短期可配置回退，长期应升级相关依赖并修正路径模式。

## 循环依赖

Boot 2.6 默认禁止循环依赖。可以通过配置临时允许，但更推荐重构依赖关系。常见修复方式包括拆分职责、延迟注入、事件解耦和引入中间服务。
