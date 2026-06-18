# 自动配置

## 自动配置导入

Spring Boot 自动配置通过 `@EnableAutoConfiguration` 启用。Boot 2.x 主要通过 `spring.factories` 声明自动配置类，Boot 3.x 使用 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`。

自动配置类本质是普通配置类，通常结合条件注解、配置属性和默认 Bean 声明实现约定优于配置。

## 条件注解

常见条件注解：

- `@ConditionalOnClass`：类路径存在指定类。
- `@ConditionalOnMissingClass`：类路径不存在指定类。
- `@ConditionalOnBean`：容器存在指定 Bean。
- `@ConditionalOnMissingBean`：容器不存在指定 Bean。
- `@ConditionalOnProperty`：配置属性满足条件。
- `@ConditionalOnWebApplication`：当前是 Web 应用。
- `@ConditionalOnResource`：资源存在。

条件注解决定自动配置是否生效，也决定默认 Bean 是否创建。

## 覆盖默认配置

Spring Boot 推荐通过以下方式覆盖默认行为：

- 定义同类型 Bean，让 `@ConditionalOnMissingBean` 失效。
- 修改配置属性，改变自动配置参数。
- 排除指定自动配置类。
- 使用定制器 Bean，如 `WebMvcConfigurer`、`RestTemplateCustomizer`、`Jackson2ObjectMapperBuilderCustomizer`。

## 排查自动配置

自动配置未生效时应检查：

- 依赖是否在 classpath 中。
- 条件注解是否匹配。
- 是否已有用户 Bean 导致默认 Bean 不创建。
- 配置属性名称、类型和前缀是否正确。
- 自动配置类是否被排除。
- 启动包扫描范围是否覆盖配置类。

可通过 Actuator `conditions` 端点或启动 `--debug` 查看条件评估报告。
