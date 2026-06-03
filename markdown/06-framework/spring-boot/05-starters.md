# Starters

> 专题：Spring Boot
> 来源：面试内容汇总/SpringBoot.xmind

## 补充与实践

- 补充：Spring Boot 3 使用新的 AutoConfiguration imports 机制，并全面基于 Spring Framework 6。
- 实践：自定义 Starter 应提供条件装配、配置元数据、默认值和清晰的覆盖方式。
- 排障：自动配置不生效时查看条件评估报告、Bean 定义冲突、配置绑定和依赖版本。

## 脑图内容

## Starters

### 介绍

#### 包含一系列可以继承到应用里面的依赖包，可以一站式继承Spring及其他技术

### 命名规范

#### SpringBoot官方

- spring-boot-starter-*命名

- *代表一个特定的应用类型

#### 第三方

- 不以spring-boot开头

- mybatis-spring-boot-starter

### 官方分类

#### application starters

- spring-boot-starter-data-redis

#### production starters

- spring-boot-starter-actuator

#### technical starters

- spring-boot-starter-tomcat

### 自定义一个Starter

#### 创建一个自动化配置类

#### 创建META-INF/spring.factories
