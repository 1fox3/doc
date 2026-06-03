# Spring Boot

> 来源：面试内容汇总/SpringBoot.xmind

## 核心认知

- Spring Boot 的价值是自动配置、约定优于配置、Starter 生态和生产可观测能力。
- 理解自动配置要抓住条件注解、配置属性绑定和 `spring.factories`/AutoConfiguration imports。

## 面试重点

- 启动流程、自动配置原理、Starter 设计、配置加载顺序、Actuator。
- 内嵌 Servlet 容器、日志系统、Runner、Profile 和外部化配置。

## 实践检查点

- 能写一个自定义 Starter，并保证默认配置可覆盖、Bean 可条件装配。
- 能排查自动配置未生效：条件报告、Bean 冲突、配置属性绑定失败。

## 版本与趋势

- Spring Boot 3.x 基于 Spring 6 和 Java 17+，原生镜像、观测性、配置绑定和自动配置机制都有变化。
- 老项目从 2.x 升级到 3.x 时，要重点处理 Jakarta 包名、依赖版本、Spring Security 和第三方 Starter 兼容性。

## 章节目录

- [基本信息](01-基本信息.md)
- [核心模块](02-核心模块.md)
- [最核心的注解](03-最核心的注解.md)
- [自动配置](04-自动配置.md)
- [Starters](05-starters.md)
- [注册Servlet](06-注册servlet.md)
- [Runner](07-runner.md)
- [日志框架](08-日志框架.md)
- [热部署方式](09-热部署方式.md)
- [instantiate](10-instantiate.md)
