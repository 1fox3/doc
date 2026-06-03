# Spring Cloud Alibaba

> 来源：SpringCloudAlibaba.xmind

## 核心认知

- Spring Cloud Alibaba 提供 Nacos、Sentinel、Seata、RocketMQ 等阿里生态治理组件。
- 重点是理解各组件解决的治理问题，而不是只记注解和配置。

## 面试重点

- Nacos 注册配置、Sentinel 限流熔断、Seata 分布式事务、RocketMQ 消息集成。
- AP/CP、动态配置推送、流控规则、事务模式 AT/TCC/Saga。

## 实践检查点

- 能根据业务一致性要求选择本地消息、TCC、Saga 或 Seata AT。
- 能设计 Sentinel 规则并说明资源名、簇点链路、热点参数限流。

## 版本与趋势

- Spring Cloud Alibaba 持续围绕 Nacos、Sentinel、Seata、RocketMQ 生态演进，版本兼容矩阵必须优先确认。
- 生产落地应关注规则治理、配置权限、注册中心容量和分布式事务边界。

## 脑图内容整理

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 微服务发展史

### SOA

#### 面向服务的架构

#### 核心目标时把一些通用的，会被多个上层服务调用的共享业务提取成独立的基础服务

#### 主要解决

- 信息孤岛

- 共享业务的重用

### 微服务与SOA区别

#### SOA关注的是服务的重用性及解决信息孤岛问题

#### 微服务关注的是解耦。解耦是降低业务之间的耦合度，重用性关注的数服务的复用

#### 微服务更多的关注在DevOps的持续交付上，与容器化技术结合的更加紧密

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## Spring Cloud

### Spring Cloud Alibaba

#### Sentinel

- 流量控制和服务降级

#### Nacos

- 服务注册与发现

- 分布式配置中心

#### RocketMQ

- 消息驱动

#### Seate

- 分布式事务

#### Dubbo

- RPC通信

#### OSS

- 阿里云对象存储

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## Spring Boot

### Spring

#### IoC(Inversion of Control)

- 控制反转

#### DI(Dependency Injection)

- 依赖注入

- 实现方式
  - 接口注入
  - 构造方法注入
  - setter方法注入

### 注解支持

#### @ComponentScan

- <context:component-scan basepackage=""/>

#### @Import

- <import resource=""/>

### Spring Boot自动装配

#### @EnableAutoConfiguration

#### @AutoConfigurationPackage

#### AutoConfigurationImportSelector

- 实现了ImportSelector

#### 流程

- 通过@Import(AutoConfigurationImportSelector)实现配置类的导入，但是这里并不是传统意义上得单个配置类装配

- AutoConfigurationImportSelector类实现了ImportSelector接口，重写了方法selectImports，它用于实现选择性批量配置类的装配

- 通过Spring提供的SpringFactoriesLoader机制，扫描classpath路径下的META-INF/spring.factories，读取需要实现自动装配的配置类

- 通过条件筛选的方式，把不符合条件的配置类移除，最终完成自动装配

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 微服务架构下的服务治理

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## instantiate

### 1、无覆盖方法，直接实例化

### 2、有覆盖方法，则生成cglib子类(动态代理)
