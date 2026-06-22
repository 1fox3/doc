# Java 9-11 新特性

Java 9 到 Java 11 主要围绕模块化、工具增强、API 增强和长期支持版本演进。Java 11 是 LTS，很多企业从 Java 8 升级时会直接选择 Java 11。

## Java 9：模块系统 JPMS

Java 9 引入 Java Platform Module System，也称 JPMS。

模块通过 `module-info.java` 声明：

```java
module com.example.app {
    requires java.sql;
    exports com.example.api;
}
```

核心能力：

- 明确依赖关系。
- 强封装内部包。
- 减少运行时镜像体积。
- 改善大型系统模块边界。

面试重点：

- 模块系统不是 Maven 依赖管理的替代品，而是 JDK 层面的可读性和封装机制。
- 强封装会影响反射访问，很多老框架升级时会遇到非法反射警告或失败。

## Java 9：集合工厂方法

```java
List<String> list = List.of("a", "b");
Set<String> set = Set.of("a", "b");
Map<String, Integer> map = Map.of("a", 1, "b", 2);
```

注意：

- 返回不可变集合。
- 不允许 null 元素或 null key/value。

## Java 9：JShell

JShell 是交互式 Java REPL 工具，适合快速验证代码片段。

启动 JShell：

```bash
jshell
```

进入后可以直接输入 Java 表达式、变量、方法和类定义，不需要先创建 `.java` 文件，也不需要手写 `public static void main`。

```text
jshell> 1 + 2
$1 ==> 3

jshell> String name = "fox"
name ==> "fox"

jshell> name.toUpperCase()
$3 ==> "FOX"
```

定义并调用方法：

```text
jshell> int add(int a, int b) {
   ...>     return a + b;
   ...> }
|  created method add(int,int)

jshell> add(10, 20)
$5 ==> 30
```

使用集合和 Stream 快速验证代码：

```text
jshell> import java.util.*

jshell> var names = List.of("Tom", "Jerry", "Spike")
names ==> [Tom, Jerry, Spike]

jshell> names.stream().filter(n -> n.length() > 3).toList()
$8 ==> [Jerry, Spike]
```

查看当前已经输入过的片段：

```text
jshell> /list
```

退出 JShell：

```text
jshell> /exit
```

JShell 常用于验证 API 行为、测试简单表达式、演示语言特性。它适合快速试验，不适合替代正式项目中的单元测试或完整应用代码。

## Java 9：Stream/Optional 增强

Stream 增强：

- `takeWhile`
- `dropWhile`
- `ofNullable`
- `iterate` 增强

Optional 增强：

- `ifPresentOrElse`
- `or`
- `stream`

## Java 10：var 局部变量类型推断

```java
var name = "fox";
var list = new ArrayList<String>();
```

限制：

- 只能用于局部变量。
- 不能用于字段、方法参数、返回值。
- 必须能从初始化表达式推断出类型。

实践建议：

- 类型明显时使用 var 可以减少冗余。
- 类型不明显时不要滥用，否则降低可读性。

## Java 11：HTTP Client 标准化

Java 11 标准化 `java.net.http.HttpClient`。

```java
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://example.com"))
    .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

能力：

- 支持 HTTP/1.1 和 HTTP/2。
- 支持同步和异步调用。
- 替代部分 `HttpURLConnection` 使用场景。

## Java 11：String API 增强

常用方法：

- `isBlank()`
- `lines()`
- `strip()`
- `stripLeading()`
- `stripTrailing()`
- `repeat(int)`

## Java 11：单文件源码运行

```bash
java Hello.java
```

适合脚本化、小工具和教学场景。

## Java 11：移除 Java EE/CORBA 模块

Java 11 移除了部分 Java EE 和 CORBA 模块，例如 JAXB、JAX-WS 等。老项目升级时如果依赖这些 API，需要显式引入第三方依赖。

## 面试回答模板

Java 9 到 11 的重点是模块系统、不可变集合工厂、Stream/Optional 增强、var 类型推断、标准 HTTP Client、String API 增强和 Java 11 LTS。升级 Java 11 时要特别关注模块封装、非法反射和 Java EE 模块移除。
