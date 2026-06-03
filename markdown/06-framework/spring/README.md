# Spring

> 来源：Spring.xmind, 面试内容汇总/Spring.xmind

## 核心认知

- Spring 的主线是 IoC 容器、Bean 生命周期、依赖注入、AOP 和扩展点。
- 源码阅读应围绕 `refresh`、BeanDefinition、BeanPostProcessor、FactoryBean、代理创建展开。

## 面试重点

- Bean 生命周期、循环依赖三级缓存、作用域、自动装配、条件装配。
- JDK 动态代理、CGLIB、事务传播行为、事务失效场景。

## 实践检查点

- 能解释为什么自调用会导致事务失效，以及如何通过代理边界修正。
- 能用后置处理器或条件注解实现轻量扩展。

## 版本与趋势

- Spring Framework 6 基于 Jakarta EE 9+，要求 Java 17+，新项目需要注意 `javax` 到 `jakarta` 的迁移。
- Spring 的核心竞争力仍是容器、AOP、事务和生态整合，源码学习应服务于排障和扩展。

## 章节目录

### Spring.xmind

- [容器基本实现](01-容器基本实现.md)
- [默认标签解析](02-默认标签解析.md)
- [自定义标签](03-自定义标签.md)
- [Bean加载(BeanFactory)](04-bean加载beanfactory.md)
- [ApplicationContext](05-applicationcontext.md)
- [AOP](06-aop.md)
- [数据库连接JDBC](07-数据库连接jdbc.md)
- [整合MyBatis](08-整合mybatis.md)
- [事务](09-事务.md)
- [SpringMVC](10-springmvc.md)
- [远程服务](11-远程服务.md)
- [Spring消息](12-spring消息.md)
- [Spring Boot](13-spring-boot.md)
- [instantiate](14-instantiate.md)
### 面试内容汇总/Spring.xmind

- [基础](15-基础/README.md)
- [常用注解](16-常用注解.md)
- [核心模块](17-核心模块.md)
- [IOC](18-ioc.md)
- [BeanFactory](19-beanfactory.md)
- [ApplicationContext](20-applicationcontext.md)
- [模块](21-模块.md)
- [IOC](22-ioc.md)
- [AOP](23-aop.md)
- [MVC](24-mvc.md)
- [事务](25-事务.md)
- [自动装配](26-自动装配.md)
- [设计模式](27-设计模式.md)
- [instantiate](28-instantiate.md)
