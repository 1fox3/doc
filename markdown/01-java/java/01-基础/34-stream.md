# Stream

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 核心概念

- Stream 是 Java 8 引入的声明式数据处理 API，用于对集合、数组、IO 等数据源进行流水线处理。
- Stream 不存储数据，通常由数据源创建，经中间操作转换，最后由终止操作触发执行。

### 操作类型

- 中间操作：`map`、`filter`、`flatMap`、`sorted`、`distinct`、`peek`。
- 终止操作：`collect`、`forEach`、`reduce`、`count`、`findFirst`、`anyMatch`。
- 中间操作通常是惰性的，只有遇到终止操作才执行。

### 实践注意

- Stream 只能消费一次。
- 避免在 Stream 中写复杂副作用逻辑。
- parallelStream 不一定更快，可能带来线程池竞争、顺序问题和上下文丢失。

### 示例代码

```java
List<String> names = users.stream()
    .filter(user -> user.getAge() >= 18)
    .map(User::getName)
    .distinct()
    .sorted()
    .toList();
```

### 复习检查

- 能用自己的话解释 `Stream`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `Stream` 展开，属于 `Java 语言基础` 的复习范围。
- 建议优先掌握：map和flatmap, map、peek、foreach。
- 二级节点提示了主要拆分角度：map适用于对每个元素进行简单的转换, flatmap适用于对数组流进行平铺后合并, map用于对流中的每个元素进行映射处理，然后在形成新的流, peek用于debug调试流中间结果，不能形成新的流，但能修改引用类型字段的值, foreach用于遍历操作，会中断流操作。

### 复习追问

- `map和flatmap` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `map、peek、foreach` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## Stream

### map和flatmap

#### map适用于对每个元素进行简单的转换

#### flatmap适用于对数组流进行平铺后合并

### map、peek、foreach

#### map用于对流中的每个元素进行映射处理，然后在形成新的流

#### peek用于debug调试流中间结果，不能形成新的流，但能修改引用类型字段的值

#### foreach用于遍历操作，会中断流操作
