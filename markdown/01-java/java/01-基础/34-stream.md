# Stream

## 核心概念

### 核心概念

- Stream 是 Java 8 引入的声明式数据处理 API，用于对集合、数组、IO 等数据源进行流水线处理。
- Stream 不存储数据，通常由数据源创建，经中间操作转换，最后由终止操作触发执行。
- Stream 只能被消费一次；终止操作执行后，再次使用同一个 Stream 会抛出 `IllegalStateException`。
- Stream 默认保持 encounter order，也就是数据源本身的遍历顺序；无序流或并行流下部分操作的结果顺序可能不同。

### 操作类型

- 创建操作：从集合、数组、值、生成器、范围、文件等创建 Stream。
- 中间操作：返回新的 Stream，通常惰性执行，例如 `filter`、`map`、`flatMap`、`sorted`、`distinct`、`peek`、`limit`、`skip`。
- 终止操作：触发流水线执行并返回结果或产生副作用，例如 `collect`、`toList`、`forEach`、`reduce`、`count`、`findFirst`、`anyMatch`。
- 短路操作：可以提前结束处理，例如 `limit`、`takeWhile`、`anyMatch`、`findFirst`。
- 中间操作通常是惰性的，只有遇到终止操作才执行。

### 实践注意

- Stream 只能消费一次。
- 避免在 Stream 中写复杂副作用逻辑。
- parallelStream 不一定更快，可能带来线程池竞争、顺序问题和上下文丢失。
- `peek` 主要用于调试，不建议把核心业务修改逻辑放到 `peek` 中。
- `toList()` 返回不可变 List，`Collectors.toList()` 不保证可变性但当前常见实现通常可变；需要明确可变时使用 `Collectors.toCollection(ArrayList::new)`。
- `findFirst` 关注顺序，`findAny` 更适合并行流中获取任意匹配值。

## 基础 Demo

```java
record User(String name, int age, String city, List<String> tags) {}

List<User> users = List.of(
    new User("Alice", 18, "Beijing", List.of("java", "mysql")),
    new User("Bob", 23, "Shanghai", List.of("redis", "java")),
    new User("Charlie", 17, "Beijing", List.of("linux")),
    new User("David", 30, "Hangzhou", List.of("java", "spring"))
);

List<String> names = users.stream()
    .filter(user -> user.age() >= 18)
    .map(User::name)
    .distinct()
    .sorted()
    .toList();
```

如果项目使用普通 JavaBean，`user.age()` 和 `User::name` 分别替换为 `user.getAge()` 和 `User::getName`。

## 创建 Stream

### Collection.stream / parallelStream

从集合创建顺序流或并行流。

```java
List<String> names = List.of("Alice", "Bob", "Charlie");

List<String> sequential = names.stream()
    .map(String::toUpperCase)
    .toList();

List<String> parallel = names.parallelStream()
    .map(String::toUpperCase)
    .toList();
```

差异：`stream()` 使用当前线程顺序处理；`parallelStream()` 使用 ForkJoinPool 并行处理，适合 CPU 密集且无共享状态的大数据量任务，不适合依赖顺序、副作用、线程上下文的逻辑。

### Arrays.stream

从数组创建 Stream，支持对象数组和基本类型数组。

```java
String[] arr = {"a", "b", "c"};
List<String> list = Arrays.stream(arr)
    .map(String::toUpperCase)
    .toList();

int sum = Arrays.stream(new int[] {1, 2, 3})
    .sum();
```

### Stream.of / ofNullable / empty

从固定值创建 Stream。

```java
List<String> words = Stream.of("java", "redis", "mysql")
    .filter(s -> s.length() > 4)
    .toList();

List<String> emptyWhenNull = Stream.ofNullable(null)
    .map(Object::toString)
    .toList();

long count = Stream.empty().count();
```

差异：`Stream.of(null)` 会创建一个包含 `null` 的流；`Stream.ofNullable(null)` 会创建空流，更适合处理可能为空的单值。

### Stream.builder

适合逐步添加元素后再构建 Stream。

```java
Stream<String> stream = Stream.<String>builder()
    .add("java")
    .add("redis")
    .add("mysql")
    .build();

List<String> result = stream.toList();
```

### Stream.generate / iterate

创建无限流，通常配合 `limit` 使用。

```java
List<Double> randoms = Stream.generate(Math::random)
    .limit(3)
    .toList();

List<Integer> powers = Stream.iterate(1, n -> n * 2)
    .limit(5)
    .toList(); // [1, 2, 4, 8, 16]

List<Integer> lessThanTen = Stream.iterate(1, n -> n < 10, n -> n + 2)
    .toList(); // [1, 3, 5, 7, 9]
```

差异：`generate` 每次通过 Supplier 独立产生元素；`iterate` 后一个元素依赖前一个元素。

### IntStream / LongStream / DoubleStream

基本类型流避免装箱拆箱，并提供数值统计能力。

```java
int sum = IntStream.range(1, 5).sum();        // 1 + 2 + 3 + 4 = 10
int sumClosed = IntStream.rangeClosed(1, 5).sum(); // 1 + 2 + 3 + 4 + 5 = 15

double average = DoubleStream.of(1.0, 2.0, 3.0)
    .average()
    .orElse(0.0);
```

差异：`range(start, end)` 左闭右开；`rangeClosed(start, end)` 左闭右闭。

### Files.lines

按行读取文件，需要关闭资源，推荐 `try-with-resources`。

```java
Path path = Path.of("app.log");

try (Stream<String> lines = Files.lines(path)) {
    long errorCount = lines
        .filter(line -> line.contains("ERROR"))
        .count();
}
```

## 中间操作

### filter

按条件过滤元素。

```java
List<Integer> evenNumbers = List.of(1, 2, 3, 4, 5).stream()
    .filter(n -> n % 2 == 0)
    .toList(); // [2, 4]
```

### map

把每个元素一对一转换为另一个值。

```java
List<Integer> lengths = List.of("java", "redis", "mysql").stream()
    .map(String::length)
    .toList(); // [4, 5, 5]
```

### mapToInt / mapToLong / mapToDouble

把对象流转换为基本类型流，适合求和、平均值、最大值、最小值。

```java
int totalAge = users.stream()
    .mapToInt(User::age)
    .sum();

double avgAge = users.stream()
    .mapToInt(User::age)
    .average()
    .orElse(0.0);
```

差异：`map` 返回 `Stream<R>`；`mapToInt` 返回 `IntStream`，可以直接调用 `sum()`、`average()` 等数值操作。

### flatMap

把每个元素转换成一个 Stream，再把多个 Stream 合并成一个 Stream。

```java
List<String> allTags = users.stream()
    .flatMap(user -> user.tags().stream())
    .distinct()
    .toList(); // [java, mysql, redis, linux, spring]
```

差异：`map` 是一对一转换；`flatMap` 是一对多后再平铺。处理 `List<List<T>>`、订单和订单明细、用户和标签时优先考虑 `flatMap`。

```java
List<List<Integer>> nested = List.of(List.of(1, 2), List.of(3, 4));

List<Stream<Integer>> wrong = nested.stream()
    .map(List::stream)
    .toList();

List<Integer> right = nested.stream()
    .flatMap(List::stream)
    .toList(); // [1, 2, 3, 4]
```

### flatMapToInt / flatMapToLong / flatMapToDouble

一对多平铺后得到基本类型流。

```java
int total = List.of("1,2", "3,4").stream()
    .flatMapToInt(s -> Arrays.stream(s.split(",")).mapToInt(Integer::parseInt))
    .sum(); // 10
```

### distinct

按 `equals` 和 `hashCode` 去重。

```java
List<Integer> unique = List.of(1, 2, 2, 3, 3, 3).stream()
    .distinct()
    .toList(); // [1, 2, 3]
```

注意：对象去重依赖 `equals/hashCode`；如果只想按某个字段去重，通常需要 `toMap` 或自定义 Predicate。

```java
List<User> uniqueByCity = new ArrayList<>(users.stream()
    .collect(Collectors.toMap(
        User::city,
        Function.identity(),
        (first, second) -> first,
        LinkedHashMap::new
    ))
    .values());
```

### sorted

排序，可使用自然顺序或 Comparator。

```java
List<Integer> sorted = List.of(3, 1, 2).stream()
    .sorted()
    .toList(); // [1, 2, 3]

List<User> byAgeDesc = users.stream()
    .sorted(Comparator.comparingInt(User::age).reversed())
    .toList();
```

差异：`sorted()` 要求元素实现 `Comparable`；`sorted(comparator)` 可以自定义排序规则。

### peek

在流水线中查看元素，常用于调试。

```java
List<String> result = List.of("java", "redis", "mysql").stream()
    .filter(s -> s.length() > 4)
    .peek(s -> System.out.println("after filter: " + s))
    .map(String::toUpperCase)
    .toList();
```

差异：`peek` 是中间操作，不会终止流；`forEach` 是终止操作，会触发执行并结束流水线。`peek` 不应该承担核心业务副作用。

### limit / skip

截取或跳过指定数量元素。

```java
List<Integer> page = IntStream.rangeClosed(1, 10)
    .boxed()
    .skip(3)
    .limit(4)
    .toList(); // [4, 5, 6, 7]
```

差异：`limit(n)` 保留前 n 个；`skip(n)` 跳过前 n 个。分页时通常先 `skip` 再 `limit`。

### takeWhile / dropWhile

Java 9 新增，基于有序流的前缀条件处理。

```java
List<Integer> taken = List.of(1, 2, 3, 0, 4, 5).stream()
    .takeWhile(n -> n > 0)
    .toList(); // [1, 2, 3]

List<Integer> dropped = List.of(1, 2, 3, 0, 4, 5).stream()
    .dropWhile(n -> n > 0)
    .toList(); // [0, 4, 5]
```

差异：`filter` 会检查所有元素；`takeWhile` 遇到第一个不满足条件的元素就停止；`dropWhile` 丢弃前缀中满足条件的元素，遇到第一个不满足条件的元素后保留剩余元素。

### unordered

声明不关心顺序，可能提升并行流性能。

```java
List<Integer> result = IntStream.rangeClosed(1, 1000)
    .parallel()
    .unordered()
    .filter(n -> n % 2 == 0)
    .limit(5)
    .boxed()
    .toList();
```

注意：`unordered` 不一定打乱顺序，它只是移除顺序约束；如果业务依赖顺序，不要使用。

### boxed

把基本类型流转换为对象流。

```java
List<Integer> numbers = IntStream.rangeClosed(1, 5)
    .boxed()
    .toList();
```

### asLongStream / asDoubleStream

把 `IntStream` 转换为更宽的基本类型流。

```java
long longSum = IntStream.rangeClosed(1, 3)
    .asLongStream()
    .sum();

double doubleSum = IntStream.rangeClosed(1, 3)
    .asDoubleStream()
    .sum();
```

### parallel / sequential

切换流的执行模式。

```java
List<Integer> result = IntStream.rangeClosed(1, 1000)
    .parallel()
    .filter(n -> n % 2 == 0)
    .sequential()
    .limit(5)
    .boxed()
    .toList();
```

注意：同一条流水线最终是并行还是顺序，通常取决于最后一次调用 `parallel()` 或 `sequential()`。

### onClose

注册 Stream 关闭回调，通常和资源型 Stream 配合使用。

```java
try (Stream<String> stream = Stream.of("a", "b")
    .onClose(() -> System.out.println("stream closed"))) {
    stream.forEach(System.out::println);
}
```

## 终止操作

### forEach / forEachOrdered

遍历元素并执行副作用逻辑。

```java
List.of("a", "b", "c").stream()
    .forEach(System.out::println);

List.of("a", "b", "c").parallelStream()
    .forEachOrdered(System.out::println);
```

差异：`forEach` 在并行流中不保证顺序；`forEachOrdered` 尽量保持 encounter order，但可能牺牲并行性能。

### toArray

把流转换为数组。

```java
String[] arr = Stream.of("java", "redis")
    .toArray(String[]::new);
```

### reduce

把多个元素规约为一个结果。

```java
int sum = List.of(1, 2, 3, 4).stream()
    .reduce(0, Integer::sum); // 10

Optional<Integer> max = List.of(1, 2, 3, 4).stream()
    .reduce(Integer::max);

int totalLength = List.of("java", "redis").stream()
    .reduce(0, (total, s) -> total + s.length(), Integer::sum);
```

差异：无初始值的 `reduce` 返回 `Optional<T>`，因为空流没有结果；有初始值的 `reduce` 返回确定结果；三参数 `reduce` 常用于并行流中元素类型和结果类型不同的规约。

### collect

把流收集到集合、Map、字符串或统计结果。

```java
List<String> list = Stream.of("a", "b")
    .collect(Collectors.toList());

Set<String> set = Stream.of("a", "b", "a")
    .collect(Collectors.toSet());

Map<String, Integer> nameToAge = users.stream()
    .collect(Collectors.toMap(User::name, User::age));
```

### toList

Java 16 新增的终止操作，直接返回不可变 List。

```java
List<String> list = Stream.of("a", "b")
    .toList();
```

差异：`stream.toList()` 返回不可变 List；`collect(Collectors.toList())` 返回的具体类型和可变性不在接口层承诺；需要可变 `ArrayList` 时使用 `Collectors.toCollection(ArrayList::new)`。

```java
List<String> mutable = Stream.of("a", "b")
    .collect(Collectors.toCollection(ArrayList::new));

mutable.add("c");
```

### min / max / count

获取最小值、最大值、数量。

```java
Optional<User> youngest = users.stream()
    .min(Comparator.comparingInt(User::age));

Optional<User> oldest = users.stream()
    .max(Comparator.comparingInt(User::age));

long adultCount = users.stream()
    .filter(user -> user.age() >= 18)
    .count();
```

### anyMatch / allMatch / noneMatch

匹配判断，都是短路终止操作。

```java
boolean hasAdult = users.stream().anyMatch(user -> user.age() >= 18);
boolean allAdult = users.stream().allMatch(user -> user.age() >= 18);
boolean noChild = users.stream().noneMatch(user -> user.age() < 18);
```

差异：`anyMatch` 任意一个满足即返回 true；`allMatch` 全部满足才返回 true；`noneMatch` 全部不满足才返回 true。对空流，`anyMatch` 返回 false，`allMatch` 和 `noneMatch` 返回 true。

### findFirst / findAny

查找元素，返回 `Optional<T>`。

```java
Optional<User> firstAdult = users.stream()
    .filter(user -> user.age() >= 18)
    .findFirst();

Optional<User> anyAdult = users.parallelStream()
    .filter(user -> user.age() >= 18)
    .findAny();
```

差异：`findFirst` 保证返回 encounter order 中第一个匹配元素；`findAny` 可以返回任意匹配元素，并行流中通常更容易优化。

### iterator / spliterator

以传统迭代器或可拆分迭代器消费流。

```java
Iterator<String> iterator = Stream.of("a", "b", "c").iterator();
while (iterator.hasNext()) {
    System.out.println(iterator.next());
}

Spliterator<String> spliterator = Stream.of("a", "b", "c").spliterator();
spliterator.forEachRemaining(System.out::println);
```

差异：`Iterator` 面向普通顺序遍历；`Spliterator` 支持拆分，Stream 并行处理底层依赖它。

## Collectors 常用操作

### toMap

收集为 Map。

```java
Map<String, Integer> nameToAge = users.stream()
    .collect(Collectors.toMap(User::name, User::age));

Map<String, User> cityToUser = users.stream()
    .collect(Collectors.toMap(
        User::city,
        Function.identity(),
        (oldValue, newValue) -> oldValue
    ));
```

注意：key 重复时，二参数 `toMap` 会抛出 `IllegalStateException`；三参数 `toMap` 可以指定冲突合并策略。

### groupingBy

按 key 分组。

```java
Map<String, List<User>> usersByCity = users.stream()
    .collect(Collectors.groupingBy(User::city));

Map<String, Long> countByCity = users.stream()
    .collect(Collectors.groupingBy(User::city, Collectors.counting()));
```

### partitioningBy

按 boolean 条件分成 true 和 false 两组。

```java
Map<Boolean, List<User>> partitioned = users.stream()
    .collect(Collectors.partitioningBy(user -> user.age() >= 18));
```

差异：`groupingBy` 可以按任意 key 分多组；`partitioningBy` 固定按 boolean 分两组。

### joining

拼接字符串。

```java
String names = users.stream()
    .map(User::name)
    .collect(Collectors.joining(", ", "[", "]"));
```

### mapping / filtering / flatMapping

在分组下游继续转换、过滤、平铺。

```java
Map<String, List<String>> namesByCity = users.stream()
    .collect(Collectors.groupingBy(
        User::city,
        Collectors.mapping(User::name, Collectors.toList())
    ));

Map<String, List<String>> adultNamesByCity = users.stream()
    .collect(Collectors.groupingBy(
        User::city,
        Collectors.filtering(user -> user.age() >= 18,
            Collectors.mapping(User::name, Collectors.toList()))
    ));

Map<String, Set<String>> tagsByCity = users.stream()
    .collect(Collectors.groupingBy(
        User::city,
        Collectors.flatMapping(user -> user.tags().stream(), Collectors.toSet())
    ));
```

差异：`stream.map/filter/flatMap` 作用于分组前的全局流；`Collectors.mapping/filtering/flatMapping` 作用于分组后的每个桶。

### counting / summing / averaging / summarizing

统计数量、总和、平均值和摘要信息。

```java
long count = users.stream().collect(Collectors.counting());

int totalAge = users.stream()
    .collect(Collectors.summingInt(User::age));

double avgAge = users.stream()
    .collect(Collectors.averagingInt(User::age));

IntSummaryStatistics stats = users.stream()
    .collect(Collectors.summarizingInt(User::age));
```

### reducing

作为 Collector 版本的规约，常用于 `groupingBy` 下游。

```java
Map<String, Optional<User>> oldestByCity = users.stream()
    .collect(Collectors.groupingBy(
        User::city,
        Collectors.reducing(BinaryOperator.maxBy(Comparator.comparingInt(User::age)))
    ));
```

### collectingAndThen

收集后再执行一次转换。

```java
Map<String, List<User>> immutableUsersByCity = users.stream()
    .collect(Collectors.groupingBy(
        User::city,
        Collectors.collectingAndThen(Collectors.toList(), List::copyOf)
    ));
```

### teeing

Java 12 新增，把同一批数据分别交给两个 Collector，再合并结果。

```java
record AgeRange(int min, int max) {}

AgeRange range = users.stream()
    .collect(Collectors.teeing(
        Collectors.mapping(User::age, Collectors.minBy(Integer::compareTo)),
        Collectors.mapping(User::age, Collectors.maxBy(Integer::compareTo)),
        (min, max) -> new AgeRange(min.orElse(0), max.orElse(0))
    ));
```

## 原始类型流专属终止操作

### sum / average / summaryStatistics

`IntStream`、`LongStream`、`DoubleStream` 提供更直接的数值计算。

```java
IntSummaryStatistics stats = users.stream()
    .mapToInt(User::age)
    .summaryStatistics();

System.out.println(stats.getCount());
System.out.println(stats.getSum());
System.out.println(stats.getMin());
System.out.println(stats.getMax());
System.out.println(stats.getAverage());
```

差异：对象流没有 `sum()` 和 `average()`；需要先 `mapToInt/mapToLong/mapToDouble`，或者使用 `Collectors.summingInt/averagingInt`。

## 相似操作差异汇总

| 操作 | 相似操作 | 核心差异 |
| --- | --- | --- |
| `map` | `flatMap` | `map` 一对一转换；`flatMap` 一对多并平铺。 |
| `map` | `mapToInt` | `map` 返回对象流；`mapToInt` 返回基本类型流，可直接数值计算。 |
| `peek` | `forEach` | `peek` 是中间操作，主要调试；`forEach` 是终止操作。 |
| `filter` | `takeWhile` | `filter` 检查所有元素；`takeWhile` 只保留满足条件的前缀。 |
| `skip` | `dropWhile` | `skip` 按数量跳过；`dropWhile` 按条件跳过前缀。 |
| `findFirst` | `findAny` | `findFirst` 保证顺序第一个；`findAny` 返回任意匹配值，适合并行。 |
| `forEach` | `forEachOrdered` | `forEach` 并行时不保序；`forEachOrdered` 保序但可能更慢。 |
| `reduce` | `collect` | `reduce` 更适合不可变规约为一个值；`collect` 更适合可变容器收集。 |
| `toList()` | `Collectors.toList()` | `toList()` 返回不可变 List；`Collectors.toList()` 不承诺具体可变性。 |
| `groupingBy` | `partitioningBy` | `groupingBy` 按任意 key 多组；`partitioningBy` 按 boolean 固定两组。 |
| `stream` | `parallelStream` | `stream` 顺序执行；`parallelStream` 并行执行但不一定更快。 |

## 完整 Demo Code

```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.IntSummaryStatistics;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.function.BinaryOperator;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class StreamDemo {
    record User(String name, int age, String city, List<String> tags) {}

    public static void main(String[] args) throws Exception {
        List<User> users = List.of(
            new User("Alice", 18, "Beijing", List.of("java", "mysql")),
            new User("Bob", 23, "Shanghai", List.of("redis", "java")),
            new User("Charlie", 17, "Beijing", List.of("linux")),
            new User("David", 30, "Hangzhou", List.of("java", "spring"))
        );

        List<String> adultNames = users.stream()
            .filter(user -> user.age() >= 18)
            .map(User::name)
            .sorted()
            .toList();
        System.out.println(adultNames);

        List<String> allTags = users.stream()
            .flatMap(user -> user.tags().stream())
            .distinct()
            .sorted()
            .toList();
        System.out.println(allTags);

        Map<String, Long> countByCity = users.stream()
            .collect(Collectors.groupingBy(User::city, Collectors.counting()));
        System.out.println(countByCity);

        Optional<User> oldest = users.stream()
            .max(Comparator.comparingInt(User::age));
        oldest.ifPresent(System.out::println);

        IntSummaryStatistics stats = users.stream()
            .mapToInt(User::age)
            .summaryStatistics();
        System.out.println(stats);

        Map<Boolean, List<User>> adultPartition = users.stream()
            .collect(Collectors.partitioningBy(user -> user.age() >= 18));
        System.out.println(adultPartition);

        List<User> uniqueByCity = new ArrayList<>(users.stream()
            .collect(Collectors.toMap(
                User::city,
                Function.identity(),
                (first, second) -> first,
                LinkedHashMap::new
            ))
            .values());
        System.out.println(uniqueByCity);

        int pageSum = IntStream.rangeClosed(1, 100)
            .skip(10)
            .limit(5)
            .sum();
        System.out.println(pageSum);

        boolean hasJavaUser = users.stream()
            .anyMatch(user -> user.tags().contains("java"));
        System.out.println(hasJavaUser);

        List<Integer> flattened = List.of(List.of(1, 2), List.of(3, 4)).stream()
            .flatMap(List::stream)
            .toList();
        System.out.println(flattened);

        int reduced = Stream.of(1, 2, 3, 4)
            .reduce(0, Integer::sum);
        System.out.println(reduced);

        Map<String, Optional<User>> oldestByCity = users.stream()
            .collect(Collectors.groupingBy(
                User::city,
                Collectors.reducing(BinaryOperator.maxBy(Comparator.comparingInt(User::age)))
            ));
        System.out.println(oldestByCity);

        try (Stream<String> lines = Files.exists(Path.of("app.log"))
            ? Files.lines(Path.of("app.log"))
            : Stream.empty()) {
            long errorCount = lines.filter(line -> line.contains("ERROR")).count();
            System.out.println(errorCount);
        }
    }
}
```

