# Spring Bean 实例化流程

## 实例化在 Bean 生命周期中的位置

Spring 创建 Bean 时，大致流程是：

1. 解析 `BeanDefinition`。

   Spring 启动时会先把 XML、注解、Java Config 等配置来源解析成 `BeanDefinition`。`BeanDefinition` 可以理解为 Bean 的“创建说明书”，里面记录了 Bean 的类名、作用域、是否懒加载、构造参数、属性值、初始化方法、销毁方法、依赖关系等元数据。后续创建 Bean 时，容器不会直接重新扫描原始配置，而是主要依据 `BeanDefinition` 来决定如何创建和管理对象。

2. 选择构造方法或工厂方法。

   准备创建 Bean 时，Spring 需要先确定“通过什么入口创建对象”。如果 Bean 是普通类，Spring 会根据无参构造、有参构造、`@Autowired` 构造方法、构造参数配置、参数类型匹配等信息选择合适的构造方法。如果 Bean 配置了静态工厂方法或实例工厂方法，Spring 则会选择对应的 `factory-method`，由工厂方法返回目标对象，而不是直接调用目标类构造方法。

3. 实例化对象。

   实例化阶段只负责把对象本身创建出来，相当于执行了构造方法或工厂方法，得到一个原始对象实例。此时对象已经存在于内存中，但它的属性依赖通常还没有注入，`Aware` 回调、初始化方法、AOP 代理等也还没有完成。因此这个阶段得到的对象还不能简单理解为“完整可用的 Spring Bean”。

4. 填充属性和依赖注入。

   对象实例创建完成后，Spring 会根据 `BeanDefinition` 中的属性配置、`@Autowired`、`@Resource`、`@Value` 等信息为对象设置属性和依赖。对于引用类型依赖，容器会从自身管理的 Bean 中查找候选对象，并按照类型、名称、`@Qualifier`、`@Primary` 等规则完成匹配。这个阶段也是循环依赖处理的关键阶段之一，单例 Bean 在属性填充前可能会提前暴露对象引用，用于解决部分 setter 注入场景下的循环依赖。

5. 执行 Aware 回调。

   如果 Bean 实现了 Spring 的 `Aware` 系列接口，容器会在依赖注入后把相关容器对象或环境信息回调给 Bean。例如实现 `BeanNameAware` 可以拿到当前 Bean 的名称，实现 `BeanFactoryAware` 可以拿到 `BeanFactory`，实现 `ApplicationContextAware` 可以拿到 `ApplicationContext`。这些回调让 Bean 可以感知容器信息，但也会增强 Bean 与 Spring 容器的耦合。

6. 执行 `BeanPostProcessor` 前置处理。

   初始化方法执行前，Spring 会调用所有匹配的 `BeanPostProcessor#postProcessBeforeInitialization`。这是容器提供的扩展点，允许框架或用户在初始化之前对 Bean 做统一处理，例如处理部分注解、注入额外能力、做校验或包装。很多 Spring 内部功能都依赖 `BeanPostProcessor` 扩展点完成，而不是写死在 Bean 创建流程里。

7. 执行初始化方法。

   前置处理完成后，Spring 会执行 Bean 的初始化逻辑。常见初始化方式包括 `@PostConstruct` 标注的方法、实现 `InitializingBean` 接口的 `afterPropertiesSet()` 方法，以及在 XML 或 `@Bean(initMethod = "...")` 中指定的初始化方法。这个阶段通常用于检查必要属性、建立连接、加载缓存、启动内部组件等需要在依赖注入完成后才能执行的逻辑。

8. 执行 `BeanPostProcessor` 后置处理，AOP 代理通常在这个阶段形成。

   初始化完成后，Spring 会继续调用 `BeanPostProcessor#postProcessAfterInitialization`。AOP 自动代理创建器就是一种 `BeanPostProcessor`，它会在这个阶段判断当前 Bean 是否需要被切面增强。如果需要增强，返回的可能不再是原始对象，而是 JDK 动态代理或 CGLIB 代理对象。也就是说，最终放入容器并对外暴露的 Bean，有时是代理对象而不是第 3 步创建出来的原始对象。

9. 放入单例池或按作用域返回。

   对于默认的 singleton Bean，完整创建完成后会被放入单例池，后续再次获取同名 Bean 时会直接复用这个对象。对于 prototype Bean，容器每次请求都会创建新对象，创建完成后直接返回，通常不会继续管理它的完整生命周期。对于 request、session 等 Web 作用域 Bean，Spring 会按照对应作用域的上下文缓存和返回对象。

实例化只负责“对象先被创建出来”，不等同于“Bean 已经完全初始化”。

## InstantiationStrategy

Spring 使用 `InstantiationStrategy` 抽象 Bean 的实例化策略。常见实现包括：

| 类 | 说明 |
| --- | --- |
| `SimpleInstantiationStrategy` | 默认策略，使用构造方法或工厂方法直接实例化 |
| `CglibSubclassingInstantiationStrategy` | 需要方法覆盖时生成 CGLIB 子类 |

核心判断逻辑可以概括为：

```java
if (!beanDefinition.hasMethodOverrides()) {
    // 没有 lookup-method 或 replaced-method，直接使用构造方法实例化。
    return BeanUtils.instantiateClass(constructorToUse);
}

// 存在方法覆盖，需要通过 CGLIB 创建子类，在子类中拦截指定方法。
return instantiateWithMethodInjection(beanDefinition, beanName, owner);
```

## 使用 CGLIB 实例化示例

当 Bean 中存在方法注入需求时，Spring 不能只创建目标类本身，而是需要通过 CGLIB 生成一个子类，在子类中覆盖指定方法。典型场景是 singleton Bean 需要每次获取一个新的 prototype Bean。

```java
import org.springframework.beans.factory.annotation.Lookup;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

@Component
public class ReportService {
    public void export() {
        ReportTask task = createTask();
        task.run();
    }

    @Lookup
    protected ReportTask createTask() {
        // 这个方法体不会真正执行，Spring 会用 CGLIB 子类覆盖它。
        return null;
    }
}

@Component
@Scope("prototype")
class ReportTask {
    void run() {
        System.out.println("run report task: " + System.identityHashCode(this));
    }
}
```

上面的 `ReportService` 默认是 singleton，`ReportTask` 是 prototype。如果直接把 `ReportTask` 注入到 `ReportService` 字段中，那么 singleton 创建时只会注入一次，后续每次调用都会复用同一个 `ReportTask`。

使用 `@Lookup` 后，Spring 会为 `ReportService` 创建一个 CGLIB 子类，大致效果类似下面这样：

```java
class ReportService$$SpringCglib extends ReportService {
    private final BeanFactory beanFactory;

    @Override
    protected ReportTask createTask() {
        return beanFactory.getBean(ReportTask.class);
    }
}
```

因此，每次执行 `export()` 调用 `createTask()` 时，实际进入的是 CGLIB 子类覆盖后的方法，由容器重新获取一个 `ReportTask`。这里的 CGLIB 发生在实例化阶段，目的是实现方法注入，不是为了织入 AOP 切面。

## 直接实例化

没有方法覆盖时，Spring 可以直接通过无参构造、有参构造或工厂方法创建对象。

```java
public class DirectService {
    private final String region;

    public DirectService(String region) {
        this.region = region;
    }

    public String region() {
        return region;
    }
}
```

等价配置示例：

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DirectServiceConfig {
    @Bean
    DirectService directService() {
        return new DirectService("cn");
    }
}
```

## 构造方法选择

Spring 并不总是简单调用无参构造。它会结合以下信息选择构造方法：

- `@Autowired` 标记的构造方法。
- `BeanDefinition` 中的构造参数。
- 参数类型、参数名、依赖候选 Bean。
- 是否存在默认构造方法。

```java
import org.springframework.stereotype.Component;

@Component
public class OrderService {
    private final OrderRepository repository;

    public OrderService(OrderRepository repository) {
        this.repository = repository;
    }
}

interface OrderRepository {
}
```

## 工厂方法实例化

Bean 也可以通过静态工厂方法或实例工厂方法创建。此时实例化对象的是工厂方法，不是目标类构造方法直接被容器调用。

```java
public class ClientFactory {
    public static ApiClient create() {
        return new ApiClient("https://example.com");
    }
}

class ApiClient {
    private final String endpoint;

    public ApiClient(String endpoint) {
        this.endpoint = endpoint;
    }
}
```

XML 风格示例：

```xml
<bean id="apiClient" class="com.example.ClientFactory" factory-method="create" />
```

## JDK、CGLIB、AOP 代理的区别

文档中提到的 JDK 动态代理、CGLIB 代理、AOP 代理不是同一层面的概念。JDK 动态代理和 CGLIB 代理是“代理对象怎么生成”的技术手段，AOP 代理是“这个代理对象用来做什么”的框架机制。

## JDK 动态代理

JDK 动态代理是 Java 标准库提供的代理机制，核心类是 `java.lang.reflect.Proxy` 和 `InvocationHandler`。它只能基于接口生成代理对象，代理类实现目标对象的接口，方法调用会被转发到 `InvocationHandler#invoke`。

```java
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

interface PaymentService {
    void pay();
}

class PaymentServiceImpl implements PaymentService {
    @Override
    public void pay() {
        System.out.println("pay");
    }
}

class LogInvocationHandler implements InvocationHandler {
    private final Object target;

    LogInvocationHandler(Object target) {
        this.target = target;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        System.out.println("before");
        Object result = method.invoke(target, args);
        System.out.println("after");
        return result;
    }
}

PaymentService target = new PaymentServiceImpl();
PaymentService proxy = (PaymentService) Proxy.newProxyInstance(
        target.getClass().getClassLoader(),
        new Class<?>[] { PaymentService.class },
        new LogInvocationHandler(target)
);
```

在 Spring AOP 中，如果目标 Bean 实现了接口，并且没有强制使用类代理，Spring 通常可以选择 JDK 动态代理。此时从容器中拿到的 Bean 类型更接近接口类型，而不是目标实现类本身。

## CGLIB 代理

CGLIB 是基于字节码生成子类的代理机制。它不要求目标类实现接口，而是通过创建目标类的子类，覆盖可重写的方法，在方法前后加入拦截逻辑。

```java
class OrderService {
    public void createOrder() {
        System.out.println("create order");
    }
}

class OrderService$$SpringCglib extends OrderService {
    @Override
    public void createOrder() {
        System.out.println("before");
        super.createOrder();
        System.out.println("after");
    }
}
```

这段代码只是说明 CGLIB 子类的大致效果，真实的 CGLIB 代理类由框架在运行时生成。因为 CGLIB 依赖继承，所以 `final` 类不能被代理，`final`、`private` 方法也不能被覆盖。

在本文前面的 `@Lookup` 示例中，Spring 也使用了 CGLIB，但它的目的不是 AOP，而是方法注入：通过生成子类覆盖 `createTask()`，让该方法每次都从容器中重新获取 Bean。

## AOP 代理

AOP 代理是 Spring 为了实现切面编程而创建的代理对象，常见触发场景包括 `@Transactional`、`@Async`、`@Cacheable`、`@PreAuthorize` 和自定义切面等。AOP 代理关注的是在业务方法调用前后织入增强逻辑，例如开启事务、提交事务、记录日志、做权限判断等。

Spring AOP 创建代理时，底层通常会在 JDK 动态代理和 CGLIB 代理之间选择一种实现方式：

- 如果目标类实现了接口，默认倾向使用 JDK 动态代理。
- 如果目标类没有实现接口，通常使用 CGLIB 代理。
- 如果配置了 `proxyTargetClass = true`，会强制使用 CGLIB 代理。

因此，“AOP 代理”不是第三种独立于 JDK 和 CGLIB 之外的字节码技术，它是 Spring AOP 的代理机制；JDK 动态代理和 CGLIB 代理是它可以采用的两种底层实现。

## 三者对比

| 对比点 | JDK 动态代理 | CGLIB 代理 | AOP 代理 |
| --- | --- | --- | --- |
| 概念层级 | Java 标准库代理技术 | 字节码子类代理技术 | Spring AOP 的代理机制 |
| 主要作用 | 基于接口创建代理对象 | 基于目标类子类创建代理对象 | 为切面增强创建代理对象 |
| 是否要求接口 | 要求目标对象有接口 | 不要求接口 | 不一定，取决于底层选择 JDK 还是 CGLIB |
| 代理对象形态 | 实现相同接口的代理类 | 继承目标类的子类 | 可能是 JDK 代理，也可能是 CGLIB 代理 |
| 方法限制 | 只能代理接口方法 | 不能代理 `final`、`private` 方法 | 受底层代理方式限制 |
| Spring 中的常见场景 | 有接口的 `@Transactional`、自定义 AOP | 无接口或强制类代理的 AOP、`@Lookup` 方法注入 | 事务、缓存、异步、权限、日志等切面增强 |
| 发生阶段 | AOP 场景下通常在初始化后置处理阶段 | 方法注入时在实例化阶段，AOP 场景下在初始化后置处理阶段 | 通常在 `BeanPostProcessor#postProcessAfterInitialization` 阶段形成 |

还需要特别区分两种 CGLIB：

| 对比点 | 方法注入 CGLIB | AOP CGLIB 代理 |
| --- | --- | --- |
| 发生阶段 | Bean 实例化阶段 | Bean 初始化后置处理阶段 |
| 目的 | 覆盖特定方法返回容器中的 Bean 或替换方法实现 | 拦截业务方法织入切面逻辑 |
| 触发条件 | `lookup-method`、`replaced-method`、`@Lookup` | `@Transactional`、`@Async`、自定义切面等 |
| 返回对象 | 通过 CGLIB 子类直接实例化目标 Bean | 初始化后可能把原始 Bean 包装成代理对象 |

一句话总结：JDK 动态代理和 CGLIB 是代理实现技术，AOP 代理是 Spring 使用这些代理技术实现切面增强的机制；而本文中的 `CglibSubclassingInstantiationStrategy` 使用 CGLIB 是为了方法注入，不等同于 AOP 代理。
