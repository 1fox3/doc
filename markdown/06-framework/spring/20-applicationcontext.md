# ApplicationContext

> 专题：Spring
> 来源：面试内容汇总/Spring.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

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
