# Spring Boot 3.x 关键变化

## Java 17 基线

Spring Boot 3 要求 Java 17+。升级前需要确认构建工具、CI/CD、运行镜像、字节码增强工具、APM Agent 和本地开发环境都支持 Java 17。

## Spring Framework 6

Boot 3 基于 Spring Framework 6。核心变化包括 Java 17 基线、Jakarta EE 9 API、AOT 处理、改进的 HTTP 接口和观测性整合。

## Jakarta EE 迁移

Java EE 包名从 `javax.*` 迁移到 `jakarta.*`。影响范围包括 Servlet、Validation、JPA、JMS、WebSocket、Annotation 等 API。

常见替换：

- `javax.servlet.*` -> `jakarta.servlet.*`
- `javax.validation.*` -> `jakarta.validation.*`
- `javax.persistence.*` -> `jakarta.persistence.*`
- `javax.annotation.*` -> `jakarta.annotation.*`

第三方库如果仍依赖旧 `javax` API，可能无法与 Boot 3 兼容。

## 自动配置声明

Boot 3 使用 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` 声明自动配置类。旧的 `spring.factories` 自动配置声明方式不再作为主路径。

自定义 Starter 升级时应检查：

- 自动配置类是否迁移到 `AutoConfiguration.imports`。
- 是否使用 `@AutoConfiguration`。
- 条件注解是否仍准确。
- 配置属性元数据是否正常生成。

## AOT 与 Native Image

Boot 3 增强 AOT 支持，可为 GraalVM Native Image 生成运行时提示和预处理代码。

Native Image 注意事项：

- 反射、动态代理、资源加载需要 RuntimeHints。
- 启动快、内存低，但构建慢，运行时动态能力受限。
- 依赖库必须支持 Native Image 或提供 hints。
- 需要用真实业务路径验证序列化、反射、代理和资源访问。

## Observability

Boot 3 使用 Micrometer Observation 统一指标、追踪和上下文传播。Sleuth 不再是主线方案，链路追踪通常迁移到 Micrometer Tracing，并对接 OpenTelemetry、Zipkin、Tempo 或 Jaeger。

## Spring Security

Boot 3 通常伴随 Spring Security 6。旧的 `WebSecurityConfigurerAdapter` 已移除，需要改为声明 `SecurityFilterChain` Bean。授权配置也应从旧 DSL 迁移到新的 lambda 风格配置。
