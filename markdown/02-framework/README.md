# Framework 技术体系

本目录只保留后端框架相关的技术内容，按框架边界和运行链路重新划分。重点覆盖 Spring、Spring MVC、Spring Boot、MyBatis 以及 Spring Boot 版本升级。

## 内容划分

- [Spring 核心](spring/README.md)：IoC 容器、Bean 生命周期、AOP、事务、扩展点。
- [Spring MVC](spring-mvc/README.md)：请求分发、参数绑定、返回值处理、异常处理、校验。
- [Spring Boot](spring-boot/README.md)：启动流程、自动配置、配置体系、Starter、Actuator、日志。
- [MyBatis](mybatis/README.md)：执行流程、映射体系、动态 SQL、缓存、事务、插件、生产实践。
- [Spring Boot 版本升级](spring-boot-version-features/README.md)：2.x、3.x 核心变化和升级检查项。

## 学习顺序

1. 先掌握 Spring 容器和 Bean 生命周期，理解依赖注入、作用域、循环依赖和扩展点。
2. 再理解 AOP 与事务代理边界，明确事务失效场景和传播行为。
3. 接着学习 Spring MVC 的请求处理链路，串联 Controller、参数解析、类型转换和异常处理。
4. 然后学习 Spring Boot 的启动与自动配置，把条件装配、属性绑定和 Starter 设计串起来。
5. 最后补充 MyBatis 执行链路、动态 SQL、缓存和插件，结合 Spring 事务理解数据访问层行为。
