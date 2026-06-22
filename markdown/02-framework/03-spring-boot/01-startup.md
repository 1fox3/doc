# 启动流程

## SpringApplication.run

`SpringApplication.run()` 是 Spring Boot 启动入口，主要职责包括创建应用上下文、准备环境、加载配置、刷新容器和启动运行器。

核心步骤：

1. 创建 `SpringApplication` 实例。
2. 推断 Web 应用类型：Servlet、Reactive 或 None。
3. 加载 `ApplicationContextInitializer` 和 `ApplicationListener`。
4. 发布启动事件。
5. 创建并准备 `Environment`。
6. 创建 `ApplicationContext`。
7. 加载主启动类和配置类。
8. 调用 `refresh()` 初始化 Spring 容器。
9. 执行 Runner。
10. 发布启动完成事件。

## 主启动注解

`@SpringBootApplication` 是组合注解，包含：

- `@SpringBootConfiguration`：本质是 `@Configuration`，表示配置类。
- `@EnableAutoConfiguration`：启用自动配置导入。
- `@ComponentScan`：从启动类所在包向下扫描组件。

启动类位置会影响组件扫描范围。通常应放在业务根包，避免漏扫组件或意外扫描过多类。

## 事件阶段

Spring Boot 启动期间会发布多个事件，例如环境准备完成、上下文准备完成、应用启动完成、应用运行失败等。监听器适合做启动期诊断、环境校验、外部资源预热等逻辑。

## Runner

`ApplicationRunner` 和 `CommandLineRunner` 在容器启动完成后执行。二者区别在参数模型：

- `ApplicationRunner` 接收结构化 `ApplicationArguments`。
- `CommandLineRunner` 接收原始字符串数组。

Runner 适合执行轻量启动任务，不应放置长时间阻塞逻辑。需要控制顺序时使用 `@Order` 或实现 `Ordered`。
