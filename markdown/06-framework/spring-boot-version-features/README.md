# Spring Boot 版本新特性总览

本目录整理 Spring Boot 1.x、2.x、3.x 的关键变化，重点服务后端面试、项目升级和技术选型。

## 为什么要单独整理版本特性

- Spring Boot 1.x 是早期自动配置和 Starter 体系的成型阶段，很多老系统仍能看到它的影子。
- Spring Boot 2.x 是企业存量项目最常见版本线，包含 WebFlux、Actuator 2、Micrometer、配置机制变化等重要内容。
- Spring Boot 3.x 基于 Spring Framework 6 和 Java 17，涉及 Jakarta EE 迁移、AOT、Native Image、Observability 等重大变化。

## 阅读顺序

1. [Spring Boot 1.x 到 2.x](spring-boot-1-to-2.md)
2. [Spring Boot 2.0 到 2.3](spring-boot-2-0-to-2-3.md)
3. [Spring Boot 2.4 到 2.7](spring-boot-2-4-to-2-7.md)
4. [Spring Boot 3.x](spring-boot-3.md)
5. [版本升级路线](upgrade-guide.md)

## 面试重点

- Spring Boot 的核心价值：自动配置、Starter、外部化配置、Actuator、内嵌容器。
- Spring Boot 2.x：响应式 WebFlux、Micrometer、Actuator 端点模型变化、配置加载机制调整。
- Spring Boot 2.4：`ConfigData` 配置加载机制，引入 `spring.config.import`。
- Spring Boot 2.6：默认禁止循环依赖，路径匹配策略变化。
- Spring Boot 3.x：Java 17、Spring 6、Jakarta EE、AOT、GraalVM Native Image、Observability。

## 找工作建议

- 存量项目面试：重点准备 Spring Boot 2.x、自动配置原理、Actuator、配置加载、循环依赖变化。
- 新项目面试：重点准备 Spring Boot 3.x、Java 17、Jakarta 迁移、Micrometer Tracing、AOT/Native。
- 如果简历写过升级项目，要能讲清依赖兼容、配置变更、自动配置差异、压测和灰度方案。
