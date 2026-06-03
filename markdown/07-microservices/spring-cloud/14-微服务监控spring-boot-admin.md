# 微服务监控Spring Boot Admin

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

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
