# Spring Boot

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## Spring Boot

### 三大特点

#### 自动配置

#### 起步依赖

#### Actuator对运行期间的状态监控

### @SpringBootApplication

#### @SpringBootConfiguration

#### @EnableAutoConfiguration

#### @ComponentScan

### 配置赋值给实体类

#### @ConfigurationProperties(prefix="my")

#### @Component

### 自定义配置文件

#### @Configuration

#### @PropertySource

#### @ConfigurationProperties

### Actuator

#### 依赖spring-boot-starter-actuator

#### 配置

- management.port

- management.security.enabled

#### API

- /autoconfig
  - 提供了一份自动配置报告，记录哪些自动配置条件通过了，哪些没有通过

- /configprops
  - 描述配置属性如何注入Bean

- /beans
  - 描述应用程序上下文里全部的Bean，以及它们的关系

- /threaddump
  - 获取线程活动的快照

- /env
  - 获取全部环境属性

- /sessions
  - 用户会话

- /health
  - 应用程序的健康指标

- /info
  - 获取应用程序的信息

- /auditevens
  - 显示当前应用程序的审计事件信息

- /conditions
  - 显示配置类和自动配置类的状态，以及它们被应用或未被应用的原因

- /flyway
  - 显示数据迁移路径

- /liquibase
  - 展示任何Liquibase数据库迁移路径(如果存在)

- /loggers
  - 显示和设置Logger级别

- /mappings
  - 描述全部的URI路径，以及它们和控制器(包含Actuaor端点)的映射关系

- /metrics
  - 获取应用程序度量信息，例如内存用量和HTTP请求计数

- /scheduledtasks
  - 显示应用程序中的计划任务

- /shutdown
  - 关闭应用程序，需要将endpoints.shutdown.enable设置为true

- /httptrace
  - 提供基本HTTP请求跟踪信息(时间戳、HTTP头等)

- /caches
  - 暴露可用缓存

#### shell连接Actuator

- 依赖spring-boot-starter-remote-shell

- 命令
  - beans
    - 列出SpringBoot程序应用上下文的Bean
  - endpoint
    - 调用Actuator端点
  - metrics
    - SpringBoot的度量信息
  - autoconfig
    - 生成自动配置说明报告

### Swagger2

#### 相关注解

- @Api
  - 修饰整个类

- @ApiOperation
  - 描述类的方法，或者一个接口

- @ApiParam
  - 单个参数描述

- @ApiModel
  - 用对象来接收参数

- @ApiProperty
  - 用对象接收参数时，描述对象的一个字段

- @ApiResponse
  - HTTP响应的一个描述

- @ApiResponses
  - HTTP响应的整体描述

- @ApiIgnore
  - 使用该注解，表示Swagger2忽略这个API

- @ApiError
  - 发生错误返回的信息

- @ApiParamImplicit
  - 一个请求参数

- @ApiParamsImplicit
  - 多个请求参数

#### 地址

- http://localhost:8080/swagger-ui.html
