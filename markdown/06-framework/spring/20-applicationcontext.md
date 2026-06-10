# ApplicationContext

> 专题：Spring
> 来源：面试内容汇总/Spring.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 是什么

- `ApplicationContext` 是 `Spring` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `ApplicationContext` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `ApplicationContext`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `ApplicationContext` 展开，属于 `Spring` 的复习范围。
- 建议优先掌握：介绍, 具体实现。
- 二级节点提示了主要拆分角度：Spring框架的核心容器，是管理Bean的高级容器，它可以读取配置，管理Bean的生命周期，装配Bean之间的关系，并提供了许多企业级应用所需的服务，如JNDI，EJB集成，远程访问等, ClassPathXmlApplicationContext, FileSystemXmlApplicationContext, AnnotationConfigApplicationContext, WebApplicationContext, XmlWebApplicationContext, StaticApplicationContext, GenericApplicationContext, GenericXmlApplicationContext。
- 三级节点通常对应具体细节、API、机制或易错点：从类路径下的XML文件中加载上下文, 从文件系统中的XML文件中加载上下文, 根据注解创建上下文, 用于Web应用程序的上下文, 用于Web应用程序的XML上下文, 不依赖于外部资源的ApplicationContext实现, 可以集成任何BeanFactory或ApplicationContext实现, 从XML文件中加载上下文定义，并可以集成任何BeanFactory或ApplicationContext实现。

### 复习追问

- `介绍` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `具体实现` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## ApplicationContext

### 介绍

#### Spring框架的核心容器，是管理Bean的高级容器，它可以读取配置，管理Bean的生命周期，装配Bean之间的关系，并提供了许多企业级应用所需的服务，如JNDI，EJB集成，远程访问等

### 具体实现

#### ClassPathXmlApplicationContext

- 从类路径下的XML文件中加载上下文

#### FileSystemXmlApplicationContext

- 从文件系统中的XML文件中加载上下文

#### AnnotationConfigApplicationContext

- 根据注解创建上下文

#### WebApplicationContext

- 用于Web应用程序的上下文

#### XmlWebApplicationContext

- 用于Web应用程序的XML上下文

#### StaticApplicationContext

- 不依赖于外部资源的ApplicationContext实现

#### GenericApplicationContext

- 可以集成任何BeanFactory或ApplicationContext实现

#### GenericXmlApplicationContext

- 从XML文件中加载上下文定义，并可以集成任何BeanFactory或ApplicationContext实现
