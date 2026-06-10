# Spring Boot 2.4 到 2.7

Spring Boot 2.4 到 2.7 是从 2.x 走向 3.x 的过渡阶段，配置加载机制、循环依赖、路径匹配和安全配置都有重要变化。

## Spring Boot 2.4：ConfigData

Spring Boot 2.4 引入新的配置加载机制 `ConfigData`。

核心变化：

- 支持 `spring.config.import`。
- 更清晰地处理 profile 配置。
- 对配置文件加载顺序做了调整。

示例：

```properties
spring.config.import=optional:nacos:example.yaml
```

升级风险：

- 老项目依赖旧的 profile 激活方式时，配置加载顺序可能变化。
- Spring Cloud 配置中心需要匹配对应版本。

## Spring Boot 2.5

重点变化：

- SQL 初始化配置调整。
- Docker 镜像构建增强。
- Actuator 和 metrics 持续增强。

SQL 初始化相关配置从早期 `spring.datasource.initialization-mode` 逐步迁移到：

```properties
spring.sql.init.mode=always
```

## Spring Boot 2.6：循环依赖默认禁用

Spring Boot 2.6 默认不允许 Bean 循环依赖。

如果存在循环依赖，可能启动失败。

临时兼容配置：

```properties
spring.main.allow-circular-references=true
```

实践建议：

- 不建议长期依赖该开关。
- 应通过拆分职责、事件、懒加载或重构依赖方向解决。

## Spring Boot 2.6：路径匹配策略变化

Spring MVC 默认路径匹配从 `AntPathMatcher` 转向 `PathPatternParser`。

可能影响：

- Swagger/Springfox 兼容问题。
- 部分路径匹配规则行为变化。

兼容配置：

```properties
spring.mvc.pathmatch.matching-strategy=ant_path_matcher
```

## Spring Boot 2.7

Spring Boot 2.7 是 2.x 到 3.x 的过渡版本。

重点：

- 提前适配部分 3.x 迁移路径。
- Spring Security 新配置方式更常见。
- 建议用它作为升级到 3.x 前的中间版本。

## 面试重点

Spring Boot 2.4 到 2.7 最容易问的是配置加载机制变化、循环依赖默认禁用、路径匹配策略变化，以及 2.7 作为升级 3.x 的过渡版本。回答时要能结合真实升级问题说明风险和解决方案。
