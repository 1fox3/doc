# Spring Boot Security

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## Spring Boot Security

### 优点

#### 对环境无依赖性，低代码耦合性

#### 采用注解的方式控制权限，易上手

#### 易于集成与Spring Boot和Spring Cloud

### Spring Boot Security对Spring Security做了封装

#### Spring Security

- spring-security-web

- spring-security-config

#### Spring Boot Security

- spring-boot-starter-security

### 使用Spring Boot Security

#### 依赖spring-boot-starter-security

#### 继承WebSecurityConfigurerAdapter实现SecurityConfig

- @EnableWebSecurity

- @Bean注入AuthenticationManagerBuilder，添加账号

- configure方法配置HttpSecurity

- @EnableGlobalMethodSecurity开启方法级别的保护
  - prePostEnable
    - Spring Security的@PreAuthorize和@PostAuthorize注解是否可用
      - @PreAuthorize("hasRole('aaa')")
  - secureEnabled
    - Spring Security的@Secured注解是否可用
  - jsr250Enabled
    - Spring Security对JSR-250的注解是否可用

#### 可通过数据库获取用户

- UserDetailService
