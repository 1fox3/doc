# Java 语言基础

> 来源：面试内容汇总/Java.xmind

## 核心认知

- Java 面试通常围绕语言语义、集合、并发、IO、泛型与新版本特性展开，关键是能解释设计取舍与运行时行为。
- 基础问题不要停留在 API 记忆，应结合内存模型、对象生命周期、异常边界和编码规范理解。

## 面试重点

- `equals` 与 `hashCode` 契约、值传递、自动装箱缓存、字符串常量池、泛型擦除。
- 集合扩容、哈希冲突、fail-fast、线程安全集合与并发容器的适用场景。
- 线程生命周期、锁升级、`volatile`、`synchronized`、AQS、线程池参数和拒绝策略。

## 实践检查点

- 能根据业务吞吐、延迟和资源限制设计线程池参数，而不是机械套公式。
- 能说明 HashMap 在高并发下的问题，以及为什么 ConcurrentHashMap 的分段/桶级并发设计更合适。

## 版本与趋势

- 主流生产环境仍以 Java 8/11/17 为主，新项目建议优先评估 Java 17 或 Java 21 LTS。
- 现代 Java 重点关注 Record、Sealed Class、Pattern Matching、Virtual Threads、结构化并发等能力，但面试仍需夯实集合、并发和内存模型。

## 章节目录

- [基础](01-基础/README.md)
- [集合](02-集合.md)
- [多线程](03-多线程/README.md)
- [IO](04-io.md)
- [instantiate](05-instantiate.md)
