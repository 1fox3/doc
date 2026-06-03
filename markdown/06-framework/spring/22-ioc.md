# IOC

> 专题：Spring
> 来源：面试内容汇总/Spring.xmind

## 补充与实践

- 补充：Spring 6 要求 Java 17+ 并迁移到 Jakarta 命名空间，理解 Bean 生命周期仍是排查问题的基础。
- 实践：复杂初始化逻辑优先使用明确的生命周期回调，避免在构造器里访问尚未注入完成的依赖。
- 误区：三级缓存只能解决部分单例 setter 循环依赖，构造器循环依赖和原型循环依赖无法靠它解决。

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
