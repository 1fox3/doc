# Java 8 新特性

Java 8 是现代 Java 的分水岭，引入函数式编程能力，并显著改变集合处理、异步编程和日期时间 API。

## Lambda 表达式

Lambda 用于把行为作为参数传递，简化匿名内部类。

```java
List<String> names = List.of("a", "bb", "ccc");
names.sort((a, b) -> Integer.compare(a.length(), b.length()));
```

### 面试重点

- Lambda 依赖函数式接口，即只有一个抽象方法的接口。
- Lambda 可以捕获 effectively final 的局部变量。
- Lambda 不是简单语法糖，底层通常通过 `invokedynamic` 实现。

## 函数式接口

常见接口：

- `Function<T, R>`：输入 T，输出 R。
- `Consumer<T>`：消费 T，无返回值。
- `Supplier<T>`：无输入，提供 T。
- `Predicate<T>`：输入 T，输出 boolean。
- `Runnable`、`Callable` 也可以用于函数式场景。

## Stream API

Stream 用于声明式处理集合和数据流。

```java
List<String> result = users.stream()
    .filter(u -> u.getAge() >= 18)
    .map(User::getName)
    .distinct()
    .toList();
```

### 常见操作

- 中间操作：`map`、`filter`、`flatMap`、`distinct`、`sorted`、`peek`。
- 终止操作：`collect`、`forEach`、`reduce`、`count`、`anyMatch`、`findFirst`。

### 注意事项

- Stream 只能消费一次。
- 并行流不一定更快，可能引入线程池竞争和顺序问题。
- 避免在 Stream 中写复杂副作用逻辑。

## Optional

Optional 用于表达“可能没有值”，减少空指针判断。

```java
String city = Optional.ofNullable(user)
    .map(User::getAddress)
    .map(Address::getCity)
    .orElse("unknown");
```

### 实践建议

- Optional 适合作为返回值，不建议作为实体字段或方法参数滥用。
- 不要直接 `get()`，应使用 `orElse`、`orElseGet`、`orElseThrow`。

## 默认方法和静态接口方法

接口可以定义 `default` 方法和 `static` 方法。

作用：

- 在不破坏已有实现类的情况下扩展接口能力。
- Java 集合框架大量使用默认方法增强 API。

## 新日期时间 API

Java 8 引入 `java.time` 包：

- `LocalDate`
- `LocalTime`
- `LocalDateTime`
- `Instant`
- `Duration`
- `Period`
- `DateTimeFormatter`

优势：

- 不可变。
- 线程安全。
- API 语义清晰。
- 替代 `Date`、`Calendar`、`SimpleDateFormat` 的很多场景。

## CompletableFuture

CompletableFuture 提供异步编排能力。

```java
CompletableFuture<User> userFuture = CompletableFuture.supplyAsync(() -> queryUser(id), executor);
CompletableFuture<Order> orderFuture = CompletableFuture.supplyAsync(() -> queryOrder(id), executor);

CompletableFuture<Result> result = userFuture.thenCombine(orderFuture, Result::new);
```

实践重点：

- 显式指定业务线程池。
- 处理异常：`exceptionally`、`handle`、`whenComplete`。
- 控制超时：`orTimeout`、`completeOnTimeout` 是 Java 9 后增强。

## 元空间替代永久代

Java 8 移除了永久代 PermGen，使用 Metaspace 存储类元数据。

区别：

- PermGen 在 JVM 堆内存逻辑区域中，大小固定，容易 OOM。
- Metaspace 使用本地内存，默认可增长，但仍需要限制和监控。

常见参数：

- `-XX:MetaspaceSize`
- `-XX:MaxMetaspaceSize`

## 面试回答模板

Java 8 的核心变化是引入函数式编程和更现代的 API。Lambda、函数式接口和 Stream 改变了集合处理方式；Optional 改善空值表达；CompletableFuture 增强异步编排；java.time 替代旧日期 API；JVM 层面用 Metaspace 替代永久代。
