# Spring Boot

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 是什么

- `Spring Boot` 是 `Spring Cloud` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `Spring Boot` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `Spring Boot`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `Spring Boot` 展开，属于 `Spring Cloud` 的复习范围。
- 建议优先掌握：三大特点, @SpringBootApplication, 配置赋值给实体类, 自定义配置文件, Actuator。
- 二级节点提示了主要拆分角度：自动配置, 起步依赖, Actuator对运行期间的状态监控, @SpringBootConfiguration, @EnableAutoConfiguration, @ComponentScan, @ConfigurationProperties(prefix="my"), @Component, @Configuration, @PropertySource。
- 三级节点通常对应具体细节、API、机制或易错点：management.port, management.security.enabled, /autoconfig, /configprops, /beans, /threaddump, /env, /sessions, /health, /info。

### 复习追问

- `三大特点` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `@SpringBootApplication` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `配置赋值给实体类` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `自定义配置文件` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `Actuator` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

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
