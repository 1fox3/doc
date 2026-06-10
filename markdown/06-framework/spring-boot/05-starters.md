# Starters

> 专题：Spring Boot
> 来源：面试内容汇总/SpringBoot.xmind

## 补充与实践

- 补充：Spring Boot 3 使用新的 AutoConfiguration imports 机制，并全面基于 Spring Framework 6。
- 实践：自定义 Starter 应提供条件装配、配置元数据、默认值和清晰的覆盖方式。
- 排障：自动配置不生效时查看条件评估报告、Bean 定义冲突、配置绑定和依赖版本。

## 详细说明

### 是什么

- `Starters` 是 `Spring Boot` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `Starters` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `Starters`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `Starters` 展开，属于 `Spring Boot` 的复习范围。
- 建议优先掌握：介绍, 命名规范, 官方分类, 自定义一个Starter。
- 二级节点提示了主要拆分角度：包含一系列可以继承到应用里面的依赖包，可以一站式继承Spring及其他技术, SpringBoot官方, 第三方, application starters, production starters, technical starters, 创建一个自动化配置类, 创建META-INF/spring.factories。
- 三级节点通常对应具体细节、API、机制或易错点：spring-boot-starter-*命名, *代表一个特定的应用类型, 不以spring-boot开头, mybatis-spring-boot-starter, spring-boot-starter-data-redis, spring-boot-starter-actuator, spring-boot-starter-tomcat。

### 复习追问

- `介绍` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `命名规范` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `官方分类` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `自定义一个Starter` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

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
