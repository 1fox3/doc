# Spring Boot 3.x

Spring Boot 3 是一次重大升级，基于 Spring Framework 6，要求 Java 17+，并迁移到 Jakarta EE 9+ 命名空间。

## 基线变化

- Java 17+。
- Spring Framework 6+。
- Jakarta EE 9+。
- GraalVM Native Image 支持增强。

## javax 到 jakarta 迁移

最重要的破坏性变化是包名迁移：

```java
import javax.servlet.http.HttpServletRequest;
```

变为：

```java
import jakarta.servlet.http.HttpServletRequest;
```

影响范围：

- Servlet API。
- JPA。
- Validation。
- JAXB。
- WebSocket。
- 第三方库和 Starter。

## AOT 与 Native Image

Spring Boot 3 强化 AOT 编译和 GraalVM Native Image 支持。

收益：

- 启动更快。
- 内存占用更低。
- 适合 Serverless、CLI、小型微服务。

限制：

- 反射、动态代理、资源加载需要元数据提示。
- 部分第三方库兼容性需要验证。
- 构建链路更复杂。

## Observability

Spring Boot 3 用 Micrometer Observation 统一指标、日志、Tracing 的观测模型。

相关组件：

- Micrometer Metrics。
- Micrometer Tracing。
- OpenTelemetry Bridge。
- Actuator。

迁移注意：

- Spring Cloud Sleuth 不再作为新版本主线。
- 新项目通常使用 Micrometer Tracing + OpenTelemetry。

## 自动配置机制变化

Spring Boot 3 使用新的自动配置声明方式：

```text
META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
```

旧的 `spring.factories` 仍在部分场景中存在，但自动配置主路径已变化。

## Spring Security 配置变化

老式 `WebSecurityConfigurerAdapter` 已被移除。

新方式通常声明 `SecurityFilterChain` Bean：

```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
    return http.authorizeHttpRequests(auth -> auth.anyRequest().authenticated()).build();
}
```

## Java 17 带来的影响

可以更自然使用：

- Record。
- Sealed Classes。
- Pattern Matching。
- Text Blocks。

## 面试重点

Spring Boot 3 的核心变化可以概括为：Java 17 基线、Spring 6、Jakarta 迁移、AOT/Native Image、Observability、自动配置声明变化和 Spring Security 新配置模型。升级时最大风险是第三方依赖和 `javax` 包兼容性。
