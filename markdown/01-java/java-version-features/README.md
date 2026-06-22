# Java 版本新特性总览

本目录整理 Java 8 到 Java 26 的关键新特性，重点服务后端面试、老项目升级和新项目技术选型。

截至 2026-06，OpenJDK 当前 GA 版本是 JDK 26；JDK 27、JDK 28 仍属于 Early Access。生产选型通常优先关注 LTS 版本，例如 Java 8、11、17、21、25。

## 为什么要掌握版本特性

- Java 8 仍是很多存量系统的基础版本，Lambda、Stream、Optional、CompletableFuture 是高频面试点。
- Java 11 是长期支持版本，很多企业从 Java 8 升级到 Java 11。
- Java 17 是 Spring Boot 3/Spring 6 的基线，也是当前后端新项目常见 LTS。
- Java 21 是新的 LTS，虚拟线程、结构化并发、模式匹配等对服务端开发影响明显。
- Java 25 是 Java 21 之后的新 LTS，Scoped Values、紧凑源码、构造方法增强、GC 改进等能力更成熟。

## 阅读顺序

1. [Java 8](java-8.md)
2. [Java 9-11](java-9-11.md)
3. [Java 12-17](java-12-17.md)
4. [Java 18-21](java-18-21.md)
5. [Java 22-26](java-22-26.md)
6. [LTS 版本选型与升级](lts-upgrade.md)

## 版本特性汇总

| 版本 | 是否 LTS | 主要特性 |
| --- | --- | --- |
| Java 8 | 是 | Lambda、函数式接口、Stream、Optional、默认方法、CompletableFuture、新时间 API、元空间 |
| Java 9 | 否 | JPMS 模块系统、JShell、集合工厂方法、接口私有方法、进程 API、Reactive Streams、VarHandle |
| Java 10 | 否 | `var` 局部变量类型推断、垃圾回收器接口、应用类数据共享增强 |
| Java 11 | 是 | HTTP Client 标准化、String API 增强、单文件源码运行、移除 Java EE/CORBA 模块 |
| Java 12 | 否 | Switch 表达式预览、Shenandoah GC 实验特性、JVM 常量 API |
| Java 13 | 否 | Text Blocks 预览、Switch 表达式二次预览、动态 CDS 归档 |
| Java 14 | 否 | Switch 表达式标准化、`instanceof` 模式匹配预览、Record 预览、精准 NPE 提示 |
| Java 15 | 否 | Text Blocks 标准化、Sealed Classes 预览、Hidden Classes、ZGC 和 Shenandoah 转正 |
| Java 16 | 否 | Record 标准化、`instanceof` 模式匹配标准化、`jpackage`、Stream `toList()` |
| Java 17 | 是 | Sealed Classes 标准化、Java 17 LTS、Spring Boot 3/Spring 6 基线、JVM 和 GC 能力成熟 |
| Java 18 | 否 | 默认字符集 UTF-8、Simple Web Server、Javadoc `@snippet`、Internet-Address Resolution SPI |
| Java 19 | 否 | 虚拟线程预览、结构化并发孵化、Record Patterns 预览、switch 模式匹配预览、FFM API 预览 |
| Java 20 | 否 | 虚拟线程二次预览、Scoped Values 孵化、结构化并发二次孵化、Record Patterns 二次预览 |
| Java 21 | 是 | 虚拟线程标准化、Record Patterns 标准化、switch 模式匹配标准化、Sequenced Collections |
| Java 22 | 否 | FFM API 标准化、未命名变量和模式、多文件源码运行、Class-File API 预览、Stream Gatherers 预览 |
| Java 23 | 否 | Markdown Documentation Comments、分代 ZGC 默认、模块导入预览、Stream Gatherers 二次预览 |
| Java 24 | 否 | Stream Gatherers 标准化、Class-File API 标准化、虚拟线程 synchronized pinning 改进、Security Manager 永久禁用 |
| Java 25 | 是 | Scoped Values 标准化、紧凑源码文件、模块导入声明、灵活构造方法体、分代 Shenandoah、紧凑对象头 |
| Java 26 | 否 | HTTP/3 for HTTP Client、AOT 对象缓存增强、G1 吞吐优化、强化 final 语义准备、Applet API 移除 |

## 找工作建议

- 面试 Java 后端，至少要能讲清 Java 8、11、17、21、25 的代表性变化。
- 如果目标 Spring Boot 3，需要重点掌握 Java 17、Jakarta 迁移、Record、Pattern Matching、文本块等。
- 如果目标高并发服务，Java 21/25 虚拟线程和 Scoped Values 是加分项，但要能讲清适用场景和限制。
