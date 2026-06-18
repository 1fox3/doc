# 日志、Runner 与 Actuator

## 日志体系

Spring Boot 默认使用 Commons Logging 作为内部日志门面，默认 Starter 引入 Logback。常见组合是 SLF4J + Logback。

实践要点：

- 使用统一日志门面，避免直接依赖具体日志实现。
- 通过 `logging.level` 调整包级别日志。
- 生产环境输出结构化日志，包含 traceId、spanId、请求路径、耗时和错误码。
- 避免在高频路径输出大对象或敏感信息。

## 热部署

开发期可使用 `spring-boot-devtools` 支持自动重启和 LiveReload。它适合本地开发，不应作为生产热更新方案。

生产环境发布应依赖滚动发布、蓝绿发布、灰度发布或容器编排平台，而不是类热替换。

## Actuator

Actuator 提供生产诊断端点，常见端点包括：

- `health`：健康检查。
- `info`：应用信息。
- `metrics`：指标。
- `prometheus`：Prometheus 格式指标。
- `env`：环境属性。
- `beans`：Bean 列表。
- `conditions`：自动配置条件报告。
- `threaddump`：线程栈。
- `heapdump`：堆转储。

生产环境应严格控制端点暴露范围，敏感端点必须加认证和网络隔离。

## 可观测性

Spring Boot 3 整合 Micrometer Observation，统一指标、链路追踪和观测上下文。链路追踪通常配合 OpenTelemetry、Zipkin、Tempo、Jaeger 等系统落地。
