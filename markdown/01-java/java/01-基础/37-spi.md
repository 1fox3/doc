# SPI

SPI（Service Provider Interface）是 Java 的面向接口插件化机制：框架定义接口，第三方提供实现，运行时通过 `ServiceLoader` 动态发现并加载。调用方与实现方解耦——框架 jar 里只有接口，实现 jar 放在 classpath 上即可被发现，无需修改框架代码。

## JDK SPI 工作原理

1. 框架定义接口（如 `com.example.spi.MessageSender`）。
2. 实现方在 jar 中创建配置文件：路径 `META-INF/services/<接口全限定名>`，内容为实现类全限定名，每行一个。
3. 调用方用 `ServiceLoader.load(接口.class)` 加载，底层通过 `Thread.currentThread().getContextClassLoader()` 读取配置文件，再反射实例化。

```
ServiceLoader.load(接口)
  └── 读取 META-INF/services/<接口全限定名>
        └── 反射 newInstance() 每个实现类
```

## Demo：手写 JDK SPI

目录结构：

```
src/main/java/com/example/spi/
  MessageSender.java      ← 接口
  EmailSender.java        ← 实现 A
  SmsSender.java          ← 实现 B
  SpiMain.java            ← 调用方

src/main/resources/META-INF/services/
  com.example.spi.MessageSender   ← SPI 配置文件
```

**① 接口**

```java
package com.example.spi;

public interface MessageSender {
    String channel();
    void send(String to, String content);
}
```

**② 实现类**

```java
package com.example.spi;

public class EmailSender implements MessageSender {
    @Override
    public String channel() { return "email"; }

    @Override
    public void send(String to, String content) {
        System.out.printf("[Email] to=%s  content=%s%n", to, content);
    }
}
```

```java
package com.example.spi;

public class SmsSender implements MessageSender {
    @Override
    public String channel() { return "sms"; }

    @Override
    public void send(String to, String content) {
        System.out.printf("[SMS]   to=%s  content=%s%n", to, content);
    }
}
```

**③ SPI 配置文件** `META-INF/services/com.example.spi.MessageSender`

```
com.example.spi.EmailSender
com.example.spi.SmsSender
```

**④ 调用方**

```java
package com.example.spi;

import java.util.ServiceLoader;

public class SpiMain {

    public static void main(String[] args) {
        ServiceLoader<MessageSender> loader = ServiceLoader.load(MessageSender.class);

        // 遍历所有实现
        for (MessageSender sender : loader) {
            System.out.println("发现实现: " + sender.channel());
            sender.send("user@example.com", "Hello SPI");
        }

        // 按 channel 筛选（Java 9+ stream API）
        loader.reload();
        loader.stream()
              .map(ServiceLoader.Provider::get)
              .filter(s -> "sms".equals(s.channel()))
              .findFirst()
              .ifPresent(s -> s.send("13800000000", "验证码: 1234"));
    }
}
```

输出：

```
发现实现: email
[Email] to=user@example.com  content=Hello SPI
发现实现: sms
[SMS]   to=user@example.com  content=Hello SPI
[SMS]   to=13800000000  content=验证码: 1234
```

## Demo：按需加载（Java 9+）

```java
ServiceLoader<MessageSender> loader = ServiceLoader.load(MessageSender.class);

// 只读取类名（不实例化），按条件过滤后再 get()
MessageSender sender = loader.stream()
        .filter(p -> p.type().getSimpleName().startsWith("Email"))
        .findFirst()
        .map(ServiceLoader.Provider::get)  // 此时才实例化
        .orElseThrow(() -> new IllegalStateException("未找到 EmailSender"));

sender.send("user@example.com", "按需加载成功");
```

## JDK SPI vs Dubbo SPI vs Spring SPI

| 维度 | JDK SPI | Dubbo SPI | Spring SPI |
|------|---------|-----------|------------|
| 配置路径 | `META-INF/services/` | `META-INF/dubbo/` | `META-INF/spring.factories` / `META-INF/spring/…imports` |
| 加载时机 | 迭代时全量（Java 8）；`stream()` 按需（Java 9+） | 按名称按需加载 | 启动时加载，按条件激活 |
| 命名扩展 | 不支持 | 支持，`key=实现类` 格式 | 支持（`@ConditionalOnXxx`） |
| AOP/依赖注入 | 不支持 | 支持（Wrapper、Activate） | 支持（Spring 容器托管） |
| 典型用途 | JDBC Driver、日志实现 | Dubbo 协议、负载均衡、序列化插件 | Spring Boot 自动配置 |

## 经典案例

**JDBC Driver 自动注册**：MySQL Connector jar 中声明 `META-INF/services/java.sql.Driver → com.mysql.cj.jdbc.Driver`，`DriverManager` 静态块通过 SPI 完成自动注册，这是 JDBC 4.0 后不再需要手写 `Class.forName("com.mysql.cj.jdbc.Driver")` 的原因。

**SLF4J 日志绑定**：`slf4j-api` 只定义接口，`logback-classic` 等通过 SPI 声明绑定实现，运行期 `LoggerFactory` 自动发现。

## ServiceLoader 源码关键路径（Java 11）

```
ServiceLoader.load(service)
  └── new ServiceLoader(service, ClassLoader)
        └── LazyIterator
              └── hasNextService()
                    └── 读取 "META-INF/services/" + service.getName()
                          └── 逐行解析类名
              └── nextService()
                    └── Class.forName(cn, false, loader)
                          └── service.cast(c.newInstance())
```

## 注意点

- **全量实例化（Java 8）**：迭代时所有实现类都会被反射实例化，Java 9+ 的 `stream()` 可延迟到 `Provider.get()` 才实例化。
- **必须有无参构造器**：`ServiceLoader` 用 `newInstance()` 反射构造，有参或私有构造器会导致 `ServiceConfigurationError`。
- **ClassLoader 问题**：多类加载器环境（OSGi 等）下默认使用 `Thread.currentThread().getContextClassLoader()`，若与接口所在 ClassLoader 不同会找不到实现，需显式传入：`ServiceLoader.load(接口, 指定ClassLoader)`。
- **配置文件格式**：必须 UTF-8，类名前后不能有空格，否则静默失败或 `ClassNotFoundException`。
- **线程不安全**：`ServiceLoader` 本身不是线程安全的，多线程环境下需各自 `load()` 或做外部同步。
- **实现类顺序不确定**：多个 jar 提供实现时，顺序取决于 jar 加载顺序，不应依赖固定顺序。
