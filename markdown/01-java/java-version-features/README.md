# Java 版本新特性总览

本目录整理 Java 8 到 Java 21 的关键新特性，重点服务后端面试、老项目升级和新项目技术选型。

## 为什么要掌握版本特性

- Java 8 仍是很多存量系统的基础版本，Lambda、Stream、Optional、CompletableFuture 是高频面试点。
- Java 11 是长期支持版本，很多企业从 Java 8 升级到 Java 11。
- Java 17 是 Spring Boot 3/Spring 6 的基线，也是当前后端新项目常见 LTS。
- Java 21 是新的 LTS，虚拟线程、结构化并发、模式匹配等对服务端开发影响明显。

## 阅读顺序

1. [Java 8](java-8.md)
2. [Java 9-11](java-9-11.md)
3. [Java 12-17](java-12-17.md)
4. [Java 18-21](java-18-21.md)
5. [LTS 版本选型与升级](lts-upgrade.md)

## 面试重点

- Java 8：Lambda、Stream、Optional、默认方法、CompletableFuture、新时间 API、元空间。
- Java 9：模块系统、JShell、集合工厂方法。
- Java 10：`var` 局部变量类型推断。
- Java 11：HTTP Client、标准化运行单文件源码、ZGC 实验特性。
- Java 14/16：Switch 表达式、Record。
- Java 15/17：Text Blocks、Sealed Classes、Java 17 LTS。
- Java 21：Virtual Threads、Record Patterns、Pattern Matching for switch、Sequenced Collections。

## 原脑图新特性摘要

- Java 8：接口 default/static 方法、函数式接口、Stream/parallelStream、Optional、Date Time API。
- Java 9：JShell、模块系统 `module-info.java`、G1 默认垃圾收集器、`List.of/Set.of/Map.of`、String 存储优化、接口私有方法、进程 API、Reactive Streams、VarHandle。
- Java 10：局部变量类型推断 `var`、垃圾回收器接口。
- Java 11：HTTP Client 标准化、单文件源代码运行。
- Java 12：Shenandoah GC、预览特性开关 `--enable-preview`。
- Java 14：空指针精准提示、Switch 支持 `yield` 和箭头表达式。
- Java 15：ZGC 转正、Hidden Classes、Text Blocks。
- Java 16：`jpackage`、`instanceof` 模式匹配。
- Java 17：Sealed Classes。
- Java 18：默认字符集改为 UTF-8。

## 找工作建议

- 面试 Java 后端，至少要能讲清 Java 8、11、17、21 的代表性变化。
- 如果目标 Spring Boot 3，需要重点掌握 Java 17、Jakarta 迁移、Record、Pattern Matching、文本块等。
- 如果目标高并发服务，Java 21 虚拟线程是加分项，但要能讲清适用场景和限制。
