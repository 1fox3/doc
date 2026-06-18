# Starter 与内嵌容器

## Starter 设计

Starter 是依赖聚合模块，用于把一组常用依赖组合起来。标准设计通常拆成两部分：

- `xxx-spring-boot-starter`：只声明依赖，不包含复杂逻辑。
- `xxx-spring-boot-autoconfigure`：提供自动配置类、配置属性类和默认 Bean。

## 自定义 Starter 要点

- 自动配置类使用条件注解，避免无条件污染容器。
- 使用 `@ConfigurationProperties` 暴露可配置参数。
- 默认 Bean 使用 `@ConditionalOnMissingBean`，允许用户覆盖。
- 对外部依赖使用 `@ConditionalOnClass` 控制启用条件。
- Boot 3 使用 `AutoConfiguration.imports` 声明自动配置类。

## 内嵌 Servlet 容器

Spring Boot Web 应用默认使用内嵌 Servlet 容器。常见容器包括 Tomcat、Jetty、Undertow。

启动时，Spring Boot 创建 `ServletWebServerApplicationContext`，在 `refresh()` 过程中创建并启动 WebServer，同时注册 Servlet、Filter、Listener。

## 注册 Servlet 组件

常见方式：

- 使用 `ServletRegistrationBean` 注册 Servlet。
- 使用 `FilterRegistrationBean` 注册 Filter。
- 使用 `ServletListenerRegistrationBean` 注册 Listener。
- 使用 `@ServletComponentScan` 扫描 `@WebServlet`、`@WebFilter`、`@WebListener`。

Spring Boot 项目更推荐使用 RegistrationBean，便于条件装配和顺序控制。

## WebMvcConfigurer

`WebMvcConfigurer` 用于定制 MVC 行为，如拦截器、跨域、静态资源、消息转换器、格式化器等。添加 `@EnableWebMvc` 会接管 Boot 的 MVC 自动配置，除非明确需要完全控制，否则不建议使用。
