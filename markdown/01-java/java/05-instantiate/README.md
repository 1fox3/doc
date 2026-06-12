# Instantiate

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind，已按技术主题重新整理。

## 核心认知

这里的 `instantiate` 更准确地说是“实例化策略”：普通 Java 对象如何创建，以及 Spring Bean 在实例化阶段如何根据是否存在方法覆盖选择直接反射创建或 CGLIB 子类创建。

## 学习主线

- Java 层面：对象创建通常经历类加载检查、内存分配、零值初始化、对象头设置、构造方法执行等步骤。
- API 层面：常见创建方式包括 `new`、反射构造、克隆、反序列化、`MethodHandle`、`Unsafe` 等，不同方式是否执行构造方法不同。
- Spring 层面：`InstantiationStrategy` 决定 Bean 如何实例化；无 `methodOverrides` 时直接实例化，有 `lookup-method` 或 `replaced-method` 时通过 CGLIB 生成子类。
- 工程层面：实例化只是 Bean 生命周期早期阶段，后面还会发生属性填充、Aware 回调、初始化、AOP 代理等步骤，不能把“实例化”和“完整可用 Bean”混为一谈。

## 章节目录

- [Java 对象实例化基础](01-java对象实例化基础.md)
- [对象创建方式对比](02-对象创建方式对比.md)
- [Spring Bean 实例化流程](03-spring-bean实例化流程.md)
- [方法注入与 CGLIB 实例化](04-方法注入与cglib实例化.md)
- [源码关键点](05-源码关键点.md)
- [实践检查与面试表达](06-实践检查与面试表达.md)

## 面试表达

- 如果问 Java 对象实例化，先说明 `new` 的 JVM 层流程，再补充反射、克隆、反序列化等特殊创建方式。
- 如果问 Spring 的 `instantiate`，重点说明 `SimpleInstantiationStrategy` 与 `CglibSubclassingInstantiationStrategy` 的选择条件。
- 如果出现“无覆盖方法直接实例化，有覆盖方法生成 CGLIB 子类”，这里的“覆盖方法”通常指 Spring `RootBeanDefinition` 中的 `methodOverrides`，不是普通 Java 子类重写方法。
- 实例化完成不代表依赖注入完成，也不代表 AOP 代理已经创建完成。
