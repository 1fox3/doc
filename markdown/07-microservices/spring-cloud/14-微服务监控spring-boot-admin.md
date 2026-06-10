# 微服务监控Spring Boot Admin

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 是什么

- `微服务监控Spring Boot Admin` 是 `Spring Cloud` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `微服务监控Spring Boot Admin` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `微服务监控Spring Boot Admin`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `微服务监控Spring Boot Admin` 展开，属于 `Spring Cloud` 的复习范围。
- 建议优先掌握：Spring Boot Admin监控Spring Boot应用, Spring Boot Admin监控Spring Cloud微服务, Spring Boot Admin集成Security组件, Spring Boot Admin继承Email。
- 二级节点提示了主要拆分角度：创建Spring Boot Admin Server, 创建Spring Boot Admin Client, 依赖spring-boot-starter-security, security.user, eureka.instance.metadata-map.user, 继承WebSecurityConfigurerAdapter实现ScurityConfig的配置类, 依赖spring-boot-starter-mail, spring.mail, spring.boot.admin.notify.mail.to, 做如上配置后，已注册的客户端状态从UP变为OFFLINE或其他状态时，admin-server就会自动将电子邮件发送到上面配置的邮箱。
- 三级节点通常对应具体细节、API、机制或易错点：依赖spring-boot-admin-starter-server, @EnableAdminServer, 依赖spring-boot-admin-strater-client, spring.boot.admin.client.url=Admin Server地址, spring.management.endpoints.web.exposure.include:"*", spring.management.endpoints.endpoint.health.show-details:ALWAYS, @EnableEurekaClient, name, password, host。

### 复习追问

- `Spring Boot Admin监控Spring Boot应用` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `Spring Boot Admin监控Spring Cloud微服务` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `Spring Boot Admin集成Security组件` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `Spring Boot Admin继承Email` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## 微服务监控Spring Boot Admin

### Spring Boot Admin监控Spring Boot应用

#### 创建Spring Boot Admin Server

- 依赖spring-boot-admin-starter-server

- @EnableAdminServer

#### 创建Spring Boot Admin Client

- 依赖spring-boot-admin-strater-client

- spring.boot.admin.client.url=Admin Server地址

- spring.management.endpoints.web.exposure.include:"*"

- spring.management.endpoints.endpoint.health.show-details:ALWAYS

### Spring Boot Admin监控Spring Cloud微服务

#### 创建Spring Boot Admin Server (3)

- 依赖spring-boot-admin-starter-server

- spring.management.endpoints.web.exposure.include:"*"

- spring.management.endpoints.endpoint.health.show-details:ALWAYS

#### 创建Spring Boot Admin Client (4)

- 依赖spring-boot-admin-strater-client

- @EnableEurekaClient

- spring.management.endpoints.web.exposure.include:"*"

- spring.management.endpoints.endpoint.health.show-details:ALWAYS

### Spring Boot Admin集成Security组件

#### 依赖spring-boot-starter-security

#### security.user

- name

- password

#### eureka.instance.metadata-map.user

- name

- password

#### 继承WebSecurityConfigurerAdapter实现ScurityConfig的配置类

### Spring Boot Admin继承Email

#### 依赖spring-boot-starter-mail

#### spring.mail

- host

- username

- password

#### spring.boot.admin.notify.mail.to

#### 做如上配置后，已注册的客户端状态从UP变为OFFLINE或其他状态时，admin-server就会自动将电子邮件发送到上面配置的邮箱
