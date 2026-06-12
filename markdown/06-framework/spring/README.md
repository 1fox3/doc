# Spring 核心

Spring 的核心能力是通过 IoC 容器管理对象关系，通过 AOP 在代理边界上织入横切逻辑，并通过事务、事件、资源抽象等模块提供企业应用基础设施。

## 技术专题

- [容器与 IoC](01-container-ioc.md)
- [Bean 生命周期与依赖注入](02-bean-lifecycle.md)
- [AOP 与代理机制](03-aop.md)
- [事务管理](04-transaction.md)
- [扩展点与常用注解](05-extension-points.md)

## 核心链路

- `ApplicationContext#refresh()` 是容器启动主线，包含环境准备、BeanDefinition 加载、BeanFactory 后处理器执行、BeanPostProcessor 注册、单例 Bean 实例化和生命周期回调。
- Bean 创建过程主要经过实例化、属性填充、Aware 回调、初始化前后置处理、初始化方法、销毁回调注册。
- AOP 基于 BeanPostProcessor 在 Bean 初始化后创建代理，事务、异步、缓存等能力都依赖代理边界生效。
- Spring 事务本质是通过 `PlatformTransactionManager` 控制连接、提交、回滚和挂起恢复，声明式事务由 AOP 拦截方法调用完成。
