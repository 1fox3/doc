# 扩展点与常用注解

## BeanFactoryPostProcessor

`BeanFactoryPostProcessor` 在 Bean 实例化前执行，可读取或修改 BeanDefinition。典型实现包括属性占位符解析、配置类处理和自定义扫描注册。

`BeanDefinitionRegistryPostProcessor` 是更早的扩展点，可以向容器新增 BeanDefinition。

## BeanPostProcessor

`BeanPostProcessor` 参与 Bean 初始化前后处理，是 AOP、`@Autowired`、`@PostConstruct` 等能力的重要基础。

常见用途包括：

- 为 Bean 创建代理。
- 注入框架对象或上下文对象。
- 校验 Bean 配置。
- 包装或替换目标 Bean。

## FactoryBean

`FactoryBean<T>` 用于把复杂对象创建逻辑封装为 Bean。获取 Bean 名称时默认返回 `getObject()` 的结果，使用 `&beanName` 才能获取 FactoryBean 本身。

常见场景包括代理对象、客户端对象、复杂 SDK 对象和 Mapper 代理创建。

## Import 机制

`@Import` 支持三类导入方式：

- 直接导入配置类或普通 Bean 类型。
- 通过 `ImportSelector` 根据条件返回要导入的类名。
- 通过 `ImportBeanDefinitionRegistrar` 编程式注册 BeanDefinition。

很多 `@EnableXxx` 注解本质上是 `@Import` 的封装。

## 常用注解边界

- `@Component` 是通用组件注解。
- `@Service` 表示业务服务语义。
- `@Repository` 表示数据访问组件，并参与持久化异常转换。
- `@Controller` 表示 Web 控制器。
- `@Configuration` 表示配置类，默认会通过代理保证 `@Bean` 方法调用返回容器单例。
- `@Bean` 用于显式声明第三方对象或需要定制构建逻辑的对象。
