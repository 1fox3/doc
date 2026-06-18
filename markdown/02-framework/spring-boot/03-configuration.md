# 配置体系

## 外部化配置

Spring Boot 支持从命令行参数、系统属性、环境变量、配置文件、配置中心等来源读取配置。多个来源存在优先级，后加载或高优先级来源可覆盖低优先级配置。

常见配置文件包括：

- `application.properties`
- `application.yml`
- `application-{profile}.properties`
- `application-{profile}.yml`

## Profile

Profile 用于隔离不同环境配置。常见激活方式：

- `spring.profiles.active=dev`
- 命令行参数 `--spring.profiles.active=prod`
- 环境变量 `SPRING_PROFILES_ACTIVE=prod`

Profile 配置适合处理环境差异，不应承载业务开关的复杂组合逻辑。

## ConfigurationProperties

`@ConfigurationProperties` 适合绑定结构化配置，比大量使用 `@Value` 更容易校验、复用和测试。

建议：

- 为配置类设置明确前缀。
- 使用类型安全字段，避免全字符串配置。
- 配合 Bean Validation 校验必填项和范围。
- 对复杂配置提供默认值。

## ConfigData

Spring Boot 2.4 引入 ConfigData 机制，统一处理配置文件导入和外部配置源。`spring.config.import` 可导入额外配置，如配置树、外部文件、配置中心位置等。

升级旧项目时需要重点检查 `bootstrap.yml`、配置中心加载顺序、Profile 激活方式和配置覆盖关系。

## 敏感配置

密码、密钥、Token 不应提交到仓库。生产环境应通过环境变量、密钥管理系统、配置中心加密能力或运行平台 Secret 注入。
