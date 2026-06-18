# AOP 与代理机制

## AOP 概念

AOP 用于把日志、事务、权限、缓存、监控等横切逻辑从业务方法中分离出来。Spring AOP 是运行期代理模型，只拦截通过 Spring Bean 代理对象发起的方法调用。

## 核心组件

- `Aspect`：切面，包含切点和通知。
- `Pointcut`：匹配连接点的表达式。
- `Advice`：增强逻辑，如前置、后置、返回、异常、环绕通知。
- `Advisor`：Pointcut 与 Advice 的组合。
- `ProxyFactory`：根据目标对象和 Advisor 创建代理。

## 代理类型

- JDK 动态代理：基于接口创建代理类，目标对象需要实现接口。
- CGLIB 代理：基于子类生成代理，不能代理 `final` 类和 `final` 方法。

Spring Boot 默认在多数场景下使用 CGLIB 代理，具体取决于配置和代理创建器设置。

## 通知执行顺序

环绕通知位于最外层，典型顺序是：

1. `@Around` 前半段。
2. `@Before`。
3. 目标方法。
4. `@AfterReturning` 或 `@AfterThrowing`。
5. `@After`。
6. `@Around` 后半段。

多个切面同时匹配时，可使用 `@Order` 或实现 `Ordered` 控制顺序。数值越小优先级越高，进入时越靠外，退出时越靠后。

## 代理失效场景

- 同类内部方法自调用不会经过代理。
- `private` 方法不能被代理拦截。
- `final` 方法无法被 CGLIB 覆盖。
- 对象不是 Spring 管理的 Bean。
- 目标方法没有匹配到切点表达式。

解决方式通常是拆分 Bean、通过代理对象调用、使用 AspectJ 编译期或加载期织入，或调整方法可见性和 Bean 管理方式。
