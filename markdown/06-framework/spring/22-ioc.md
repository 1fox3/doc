# IOC

> 专题：Spring
> 来源：面试内容汇总/Spring.xmind

## 补充与实践

- 补充：Spring 6 要求 Java 17+ 并迁移到 Jakarta 命名空间，理解 Bean 生命周期仍是排查问题的基础。
- 实践：复杂初始化逻辑优先使用明确的生命周期回调，避免在构造器里访问尚未注入完成的依赖。
- 误区：三级缓存只能解决部分单例 setter 循环依赖，构造器循环依赖和原型循环依赖无法靠它解决。

## 详细说明

### 是什么

- `IOC` 是 `Spring` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `IOC` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `IOC`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `IOC` 展开，属于 `Spring` 的复习范围。
- 建议优先掌握：@Component和@Bean, Bean注入, Bean作用域（@Scope）, Bean的声明周期。
- 二级节点提示了主要拆分角度：@Component用于类，@Bean用于方法, @Component通常是通过路径扫描来自动侦测和装配到Spring容器中的。@Bean通常需要我们自定发产生这个bean, @Bean比@Component自定义性强。@Bean一般可用于引入第三方的类装配到Spring容器中, @Autowired, @Resource, @Inject, singleton, prototype, request, session。
- 三级节点通常对应具体细节、API、机制或易错点：Spring内置注解，默认byType, @Qualifier, JDK提供的注解, 默认编译Type，其次byType, name和type属性。

### 复习追问

- `@Component和@Bean` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `Bean注入` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `Bean作用域（@Scope）` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `Bean的声明周期` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## IOC

### @Component和@Bean

#### @Component用于类，@Bean用于方法

#### @Component通常是通过路径扫描来自动侦测和装配到Spring容器中的。@Bean通常需要我们自定发产生这个bean

#### @Bean比@Component自定义性强。@Bean一般可用于引入第三方的类装配到Spring容器中

### Bean注入

#### @Autowired

- Spring内置注解，默认byType

- @Qualifier

#### @Resource

- JDK提供的注解

- 默认编译Type，其次byType

- name和type属性

#### @Inject

### Bean作用域（@Scope）

#### singleton

#### prototype

#### request

#### session

#### application

#### websocket

### Bean的声明周期

#### Bean容器到配置文件中找到Spring Bean的定义

#### Bean容器利用Java Reflection API创建一个Bean的实例

#### 如果涉及到一些属性值，利用set()方法设置一些属性值

#### 如果Bean实现了BeanNameAware接口，调用setBeanName()方法，传入bean的名字

#### 如果Bean实现了BeanClassLoaderAware接口，调用setBeanClassLoader()方法，传入ClassLoader对象的实例

#### 如果Bean实现了BeanFactoryAware接口，调用setBeanFactoryer()方法，传入BeanFactory对象的实例

#### 与上面相似，如果实现了*,Aware接口，就调用相应的方法

#### 如果Bean实现了BeanPostProcessor对象，执行postProcessBeforeInitialization()方法

#### 如果Bean实现了InitializingBean接口，执行afterPropertiesSet()方法

#### 如果Bean实现了BeanPostProcessor对象，执行postProcessAfterInitialization()方法

#### 当销毁Bean时候，如果实现了DisposableBean接口，执行destory()方法

#### 当要销毁Bean的时候，如果bean配置文件中包含了destory-method属性，执行指定的方法
