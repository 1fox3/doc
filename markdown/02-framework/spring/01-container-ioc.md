# 容器与 IoC

## 容器职责

Spring IoC 容器负责对象定义、对象创建、依赖装配、生命周期管理和扩展点执行。应用代码不再主动 `new` 复杂对象图，而是把对象关系声明给容器，由容器统一构建和管理。

## BeanFactory 与 ApplicationContext

- `BeanFactory` 是基础容器接口，提供 Bean 获取、类型判断、作用域判断和别名管理。
- `ApplicationContext` 在 `BeanFactory` 之上增加国际化、事件发布、资源加载、环境抽象、自动注册后处理器等能力。
- 生产应用通常使用 `ApplicationContext`，底层 Bean 创建仍委托给 `DefaultListableBeanFactory`。

## BeanDefinition

`BeanDefinition` 是 Bean 的元数据模型，描述 Bean 类型、作用域、构造参数、属性值、初始化方法、销毁方法、是否懒加载、依赖关系等。XML、注解、Java Config 最终都会被解析为 BeanDefinition。

常见来源包括：

- XML 标签解析生成 BeanDefinition。
- `@ComponentScan` 扫描 `@Component`、`@Service`、`@Repository`、`@Controller`。
- `@Bean` 方法由配置类解析器转换为 BeanDefinition。
- `ImportBeanDefinitionRegistrar` 编程式注册 BeanDefinition。

## refresh 主流程

`ApplicationContext#refresh()` 是理解 Spring 启动的主线：

1. 准备环境和容器状态。
2. 创建或刷新底层 `BeanFactory`。
3. 加载 BeanDefinition。
4. 执行 `BeanFactoryPostProcessor`，允许修改 BeanDefinition。
5. 注册 `BeanPostProcessor`，参与后续 Bean 生命周期。
6. 初始化消息源、事件广播器和监听器。
7. 实例化非懒加载单例 Bean。
8. 发布容器刷新完成事件。

## 作用域

- `singleton`：每个容器一个实例，默认作用域。
- `prototype`：每次获取创建新实例，容器不负责完整销毁流程。
- `request`：每个 HTTP 请求一个实例。
- `session`：每个 HTTP Session 一个实例。
- `application`：每个 ServletContext 一个实例。

当单例 Bean 依赖 prototype Bean 时，prototype 只会在单例创建时注入一次。需要每次获取新实例时，应使用 `ObjectProvider`、`Provider`、`@Lookup` 或作用域代理。
