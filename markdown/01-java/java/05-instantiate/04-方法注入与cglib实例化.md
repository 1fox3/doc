# 方法注入与 CGLIB 实例化

## 什么是方法覆盖

Spring BeanDefinition 中的 `methodOverrides` 主要来自两类配置：

| 类型 | 说明 |
| --- | --- |
| `lookup-method` | 覆盖一个方法，让它每次从容器中查找并返回指定 Bean |
| `replaced-method` | 用 `MethodReplacer` 替换某个方法的实现 |

这里的“覆盖方法”不是指普通 Java 继承中的方法重写，而是 Spring 在实例化阶段发现 BeanDefinition 有方法注入需求，需要生成子类完成拦截。

## lookup-method 解决的问题

典型问题：单例 Bean 依赖原型 Bean。如果把原型 Bean 直接注入单例 Bean，注入只发生一次，后续每次使用的仍然是同一个实例。

`lookup-method` 可以让单例 Bean 的某个方法每次调用时都从容器重新获取原型 Bean。

```java
public abstract class ReportService {
    public void export(String content) {
        ReportTask task = createTask();
        task.run(content);
    }

    protected abstract ReportTask createTask();
}

public class ReportTask {
    public void run(String content) {
        System.out.println("export: " + content + ", task=" + System.identityHashCode(this));
    }
}
```

XML 配置示例：

```xml
<bean id="reportTask" class="com.example.ReportTask" scope="prototype" />

<bean id="reportService" class="com.example.ReportService">
    <lookup-method name="createTask" bean="reportTask" />
</bean>
```

Spring 会生成 `ReportService` 的 CGLIB 子类，覆盖 `createTask()`，使它每次调用时返回容器中的 `reportTask`。

## 注解方式 lookup

现代 Spring 可以使用 `@Lookup` 表达同类需求。

```java
import org.springframework.beans.factory.annotation.Lookup;
import org.springframework.stereotype.Component;

@Component
public abstract class ReportService {
    public void export(String content) {
        createTask().run(content);
    }

    @Lookup
    protected abstract ReportTask createTask();
}
```

```java
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

@Component
@Scope("prototype")
public class ReportTask {
    public void run(String content) {
        System.out.println(content);
    }
}
```

## Scope 枚举值

`@Scope` 的值本质上是字符串，Spring 在 `ConfigurableBeanFactory` 和 `WebApplicationContext` 中提供了常用 scope 常量。

| 常量 | 字符串值 | 说明 |
| --- | --- | --- |
| `ConfigurableBeanFactory.SCOPE_SINGLETON` | `singleton` | 默认作用域。整个 Spring 容器中同名 Bean 只创建一个实例，后续获取都会复用该实例。 |
| `ConfigurableBeanFactory.SCOPE_PROTOTYPE` | `prototype` | 原型作用域。每次从容器获取 Bean 时都会创建一个新实例，容器通常只负责创建和依赖注入，不负责完整销毁流程。 |
| `WebApplicationContext.SCOPE_REQUEST` | `request` | Web 作用域。每个 HTTP request 创建并复用一个实例，请求结束后失效。 |
| `WebApplicationContext.SCOPE_SESSION` | `session` | Web 作用域。每个 HTTP session 创建并复用一个实例，session 失效后销毁。 |
| `WebApplicationContext.SCOPE_APPLICATION` | `application` | Web 作用域。每个 `ServletContext` 创建并复用一个实例，通常等价于当前 Web 应用级别的共享对象。 |
| `WebApplicationContext.SCOPE_WEBSOCKET` | `websocket` | WebSocket 作用域。每个 WebSocket 会话创建并复用一个实例，会话结束后失效。 |

使用常量可以避免手写字符串：

```java
import org.springframework.beans.factory.config.ConfigurableBeanFactory;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

@Component
@Scope(ConfigurableBeanFactory.SCOPE_PROTOTYPE)
public class ReportTask {
}
```

`request`、`session`、`application`、`websocket` 属于 Web 环境作用域，通常需要在 Web 应用上下文中使用；普通非 Web `ApplicationContext` 默认不支持这些 scope。

## replaced-method

`replaced-method` 允许使用 `MethodReplacer` 替换方法实现。这个能力较老，生产代码中使用频率不高，但理解它有助于理解 `methodOverrides` 的来源。

```java
public class LegacyCalculator {
    public int calculate(int value) {
        return value + 1;
    }
}
```

```java
import java.lang.reflect.Method;
import org.springframework.beans.factory.support.MethodReplacer;

public class CalculatorReplacer implements MethodReplacer {
    @Override
    public Object reimplement(Object obj, Method method, Object[] args) {
        int value = (Integer) args[0];
        return value * 10;
    }
}
```

XML 配置示例：

```xml
<bean id="calculatorReplacer" class="com.example.CalculatorReplacer" />

<bean id="legacyCalculator" class="com.example.LegacyCalculator">
    <replaced-method name="calculate" replacer="calculatorReplacer" />
</bean>
```

## CGLIB 限制

| 限制 | 原因 |
| --- | --- |
| `final` 类不能被代理 | CGLIB 依赖继承生成子类 |
| `final` 方法不能被覆盖 | 子类无法重写 final 方法 |
| `private` 方法不能被覆盖 | private 方法不参与多态 |
| 构造方法不能被覆盖 | 构造方法不是普通可继承方法 |

因此，方法注入目标方法不应是 `final` 或 `private`，目标类也不能是 `final`。

## 替代方案

很多场景下不需要使用 `lookup-method`，可以用更直观的方式替代：

```java
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.stereotype.Component;

@Component
public class ReportService {
    private final ObjectProvider<ReportTask> taskProvider;

    public ReportService(ObjectProvider<ReportTask> taskProvider) {
        this.taskProvider = taskProvider;
    }

    public void export(String content) {
        taskProvider.getObject().run(content);
    }
}
```

`ObjectProvider` 更显式、易测试，也不会依赖方法覆盖语义。
