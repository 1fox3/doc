# Bean 生命周期与依赖注入

## 生命周期阶段

单例 Bean 的典型创建链路如下：

1. 实例化：通过构造方法、静态工厂方法或实例工厂方法创建对象。
2. 属性填充：解析依赖并注入字段、setter、构造参数或集合属性。
3. Aware 回调：注入 `BeanName`、`BeanFactory`、`ApplicationContext` 等容器对象。
4. 初始化前处理：执行 `BeanPostProcessor#postProcessBeforeInitialization`。
5. 初始化：执行 `@PostConstruct`、`InitializingBean#afterPropertiesSet`、自定义 `initMethod`。
6. 初始化后处理：执行 `BeanPostProcessor#postProcessAfterInitialization`，AOP 代理通常在此阶段创建。
7. 使用阶段：业务代码通过容器或依赖注入使用 Bean。
8. 销毁：执行 `@PreDestroy`、`DisposableBean#destroy`、自定义 `destroyMethod`。

## 依赖注入方式

- 构造器注入：适合必需依赖，可以保证对象创建后处于完整状态，也便于测试。
- Setter 注入：适合可选依赖或运行期可替换依赖。
- 字段注入：代码短，但隐藏依赖关系，不利于测试和不可变设计。
- 方法参数注入：常用于 `@Bean` 方法，依赖由容器按类型解析。

## 自动装配解析

`@Autowired` 默认按类型查找候选 Bean。存在多个候选时，Spring 会结合 `@Primary`、`@Qualifier`、字段名或参数名进一步筛选。

`@Resource` 默认按名称查找，再按类型兜底。`@Inject` 来源于 JSR-330，语义接近 `@Autowired`，但功能更少。

## 循环依赖

Spring 只能在特定条件下解决单例 Bean 的属性注入循环依赖，典型依赖三级缓存：

- 一级缓存 `singletonObjects`：完整初始化后的单例对象。
- 二级缓存 `earlySingletonObjects`：提前暴露的早期对象。
- 三级缓存 `singletonFactories`：用于生成早期引用的工厂，AOP 场景可提前暴露代理。

不能自动解决的场景包括构造器循环依赖、prototype 循环依赖、禁用循环依赖、代理提前暴露不一致导致的依赖问题。工程上应优先通过拆分职责、事件发布、延迟注入或领域服务重构消除循环依赖。

## 同类型 Bean 冲突处理

- 使用 `@Qualifier` 指定 Bean 名称或限定符。
- 使用 `@Primary` 指定默认候选。
- 注入 `Map<String, T>` 或 `List<T>` 获取多个实现。
- 使用 `ObjectProvider<T>` 延迟获取或按需选择。
