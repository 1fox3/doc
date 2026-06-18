# Spring Boot

Spring Boot 在 Spring Framework 之上提供应用启动、自动配置、外部化配置、内嵌容器、Starter 依赖管理和生产运维能力。理解 Spring Boot 的关键是把启动流程、自动配置导入、条件装配和配置属性绑定串起来。

## 技术专题

- [启动流程](01-startup.md)
- [自动配置](02-auto-configuration.md)
- [配置体系](03-configuration.md)
- [Starter 与内嵌容器](04-starter-web.md)
- [日志、Runner 与 Actuator](05-runtime-ops.md)

## 核心链路

1. `SpringApplication.run()` 创建并准备环境。
2. 推断应用类型，加载监听器和初始化器。
3. 创建 `ApplicationContext`。
4. 加载主配置类和自动配置类。
5. 执行 Spring 容器 `refresh()`。
6. 启动内嵌 Web 容器。
7. 执行 `ApplicationRunner` 和 `CommandLineRunner`。

## 关键机制

- 自动配置通过条件注解决定是否创建默认 Bean。
- 配置属性通过 Binder 绑定到 `@ConfigurationProperties` 对象。
- Starter 只负责依赖聚合，真正的默认行为来自 auto-configuration 模块。
- 用户自定义 Bean 通常通过 `@ConditionalOnMissingBean` 覆盖默认配置。
