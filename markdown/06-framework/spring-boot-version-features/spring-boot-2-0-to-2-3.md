# Spring Boot 2.0 到 2.3

Spring Boot 2.0 到 2.3 主要围绕响应式体系、可观测性、容器化和优雅停机增强。

## Spring Boot 2.1

重点变化：

- 支持 Java 11。
- 改进应用启动性能和自动配置报告。
- Bean 覆盖默认被禁用，避免无意覆盖同名 Bean。

相关配置：

```properties
spring.main.allow-bean-definition-overriding=true
```

实践意义：

- 老项目中如果存在同名 Bean，升级后可能启动失败。
- 需要通过重命名、条件装配或显式允许覆盖解决。

## Spring Boot 2.2

重点变化：

- 支持 Java 13。
- 延迟初始化支持。
- Actuator 和 Micrometer 持续增强。

延迟初始化：

```properties
spring.main.lazy-initialization=true
```

优点：

- 减少启动时间。
- 开发和测试环境更轻量。

风险：

- 部分 Bean 初始化错误会延迟到运行期暴露。
- 首次请求可能变慢。

## Spring Boot 2.3

重点变化：

- 支持构建 OCI 镜像。
- 引入 graceful shutdown 优雅停机。
- 健康检查增强，支持 Kubernetes probes。

优雅停机：

```properties
server.shutdown=graceful
spring.lifecycle.timeout-per-shutdown-phase=30s
```

Kubernetes 探针：

```properties
management.endpoint.health.probes.enabled=true
```

## 容器化支持

Spring Boot 2.3 开始强化云原生部署体验：

- Buildpacks 构建镜像。
- 分层 jar，提升 Docker 镜像缓存效率。
- readiness/liveness 健康检查。

## 面试重点

Spring Boot 2.0 到 2.3 的变化重点是：Bean 覆盖保护、延迟初始化、Micrometer 增强、优雅停机、Kubernetes 探针和容器镜像构建支持。这些变化体现了 Spring Boot 从单体快速开发走向云原生运行治理。
