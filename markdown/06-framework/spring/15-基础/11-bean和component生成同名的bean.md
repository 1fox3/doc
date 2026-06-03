# @Bean和@Component生成同名的Bean

> 专题：Spring
> 来源：面试内容汇总/Spring.xmind

## 补充与实践

- 补充：Spring 6 要求 Java 17+ 并迁移到 Jakarta 命名空间，理解 Bean 生命周期仍是排查问题的基础。
- 实践：复杂初始化逻辑优先使用明确的生命周期回调，避免在构造器里访问尚未注入完成的依赖。
- 误区：三级缓存只能解决部分单例 setter 循环依赖，构造器循环依赖和原型循环依赖无法靠它解决。

## 脑图内容

## @Bean和@Component生成同名的Bean

### spring.main.allow-bean-definition-overriding

#### 为true时，表示允许覆盖，以Spring后初始化的为准

#### 为false，表示不允许覆盖，抛异常
