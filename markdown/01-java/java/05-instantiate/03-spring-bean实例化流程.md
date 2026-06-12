# Spring Bean 实例化流程

## 实例化在 Bean 生命周期中的位置

Spring 创建 Bean 时，大致流程是：

1. 解析 `BeanDefinition`。
2. 选择构造方法或工厂方法。
3. 实例化对象。
4. 填充属性和依赖注入。
5. 执行 Aware 回调。
6. 执行 `BeanPostProcessor` 前置处理。
7. 执行初始化方法。
8. 执行 `BeanPostProcessor` 后置处理，AOP 代理通常在这个阶段形成。
9. 放入单例池或按作用域返回。

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

## 与 AOP 代理的区别

`CglibSubclassingInstantiationStrategy` 的 CGLIB 子类用于实现 Spring 的方法注入，不等同于 AOP 代理。

| 对比点 | 方法注入 CGLIB | AOP CGLIB 代理 |
| --- | --- | --- |
| 发生阶段 | Bean 实例化阶段 | Bean 初始化后置处理阶段 |
| 目的 | 覆盖特定方法返回容器中的 Bean 或替换方法实现 | 拦截业务方法织入切面逻辑 |
| 触发条件 | `lookup-method`、`replaced-method` | `@Transactional`、`@Async`、自定义切面等 |

两者都可能使用 CGLIB，但解决的问题不同。
