#!/usr/bin/env python3
import json
import re
import zipfile
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "markdown"
MAX_SECTION_LINES = 450


TOPIC_CONFIG = {
    "Java": ("01-java", "Java 语言基础", ["面试内容汇总/Java.xmind"]),
    "JVM": ("01-java", "JVM", ["JVM.xmind", "面试内容汇总/JVM.xmind"]),
    "Mysql": ("02-database", "MySQL", ["Mysql.xmind", "面试内容汇总/Mysql.xmind"]),
    "MongoDB": ("02-database", "MongoDB", ["面试内容汇总/MongoDB.xmind"]),
    "Redis": ("03-cache", "Redis", ["Redis.xmind", "面试内容汇总/Redis.xmind"]),
    "ES": ("04-search", "Elasticsearch", ["ES.xmind", "面试内容汇总/ES.xmind"]),
    "Kafka": ("05-mq", "Kafka", ["Kafka.xmind"]),
    "RocketMQ": ("05-mq", "RocketMQ", ["RocketMQ.xmind"]),
    "MQ": ("05-mq", "消息队列总览", ["面试内容汇总/MQ.xmind"]),
    "Spring": ("06-framework", "Spring", ["Spring.xmind", "面试内容汇总/Spring.xmind"]),
    "SpringBoot": ("06-framework", "Spring Boot", ["面试内容汇总/SpringBoot.xmind"]),
    "SpringMVC": ("06-framework", "Spring MVC", ["面试内容汇总/Spring MVC.xmind"]),
    "MyBatis": ("06-framework", "MyBatis", ["面试内容汇总/MyBatis.xmind"]),
    "SpringCloud": (
        "07-microservices",
        "Spring Cloud",
        ["SpringCloud.xmind", "面试内容汇总/Spring Cloud.xmind"],
    ),
    "SpringCloudAlibaba": (
        "07-microservices",
        "Spring Cloud Alibaba",
        ["SpringCloudAlibaba.xmind"],
    ),
    "Nacos": ("07-microservices", "Nacos", ["面试内容汇总/Nacos.xmind"]),
    "Dubbo": ("08-distributed", "Dubbo", ["Dubbo.xmind", "面试内容汇总/Dubbo.xmind"]),
    "ZooKeeper": (
        "08-distributed",
        "ZooKeeper",
        ["ZooKeeper.xmind", "面试内容汇总/ZooKeeper.xmind"],
    ),
    "Netty": ("09-network", "Netty", ["Netty.xmind", "面试内容汇总/Netty.xmind"]),
    "PHP7": ("10-php", "PHP7 内核剖析", ["PHP7内核剖析.xmind"]),
    "Summary": ("00-overview", "重点汇总", ["重点汇总.xmind", "技术点.xmind"]),
}


FILE_NAMES = {
    "Java": "java",
    "JVM": "jvm",
    "Mysql": "mysql",
    "MongoDB": "mongodb",
    "Redis": "redis",
    "ES": "elasticsearch",
    "Kafka": "kafka",
    "RocketMQ": "rocketmq",
    "MQ": "mq-overview",
    "Spring": "spring",
    "SpringBoot": "spring-boot",
    "SpringMVC": "spring-mvc",
    "MyBatis": "mybatis",
    "SpringCloud": "spring-cloud",
    "SpringCloudAlibaba": "spring-cloud-alibaba",
    "Nacos": "nacos",
    "Dubbo": "dubbo",
    "ZooKeeper": "zookeeper",
    "Netty": "netty",
    "PHP7": "php7-kernel",
    "Summary": "summary",
}


SPLIT_DOCS = {
    "Summary",
    "Java",
    "JVM",
    "Mysql",
    "Redis",
    "ES",
    "Kafka",
    "RocketMQ",
    "MQ",
    "MyBatis",
    "SpringBoot",
    "SpringMVC",
    "Spring",
    "SpringCloud",
    "Nacos",
    "Dubbo",
    "ZooKeeper",
    "Netty",
    "PHP7",
}


EXPERT_NOTES = {
    "Java": {
        "核心认知": [
            "Java 面试通常围绕语言语义、集合、并发、IO、泛型与新版本特性展开，关键是能解释设计取舍与运行时行为。",
            "基础问题不要停留在 API 记忆，应结合内存模型、对象生命周期、异常边界和编码规范理解。",
        ],
        "面试重点": [
            "`equals` 与 `hashCode` 契约、值传递、自动装箱缓存、字符串常量池、泛型擦除。",
            "集合扩容、哈希冲突、fail-fast、线程安全集合与并发容器的适用场景。",
            "线程生命周期、锁升级、`volatile`、`synchronized`、AQS、线程池参数和拒绝策略。",
        ],
        "实践检查点": [
            "能根据业务吞吐、延迟和资源限制设计线程池参数，而不是机械套公式。",
            "能说明 HashMap 在高并发下的问题，以及为什么 ConcurrentHashMap 的分段/桶级并发设计更合适。",
        ],
    },
    "JVM": {
        "核心认知": [
            "JVM 的核心是运行时内存、类加载、字节码执行、JIT 优化和垃圾回收之间的协作。",
            "排障时要把现象映射到指标：CPU、内存、GC、线程、类加载、锁竞争和对象分配。",
        ],
        "面试重点": [
            "运行时数据区、对象创建过程、对象头、逃逸分析、TLAB、直接内存。",
            "可达性分析、三色标记、分代假说、常见收集器、STW、GC 日志分析。",
            "双亲委派、类加载阶段、破坏双亲委派的典型场景。",
        ],
        "实践检查点": [
            "掌握 `jps`、`jstack`、`jmap`、`jstat`、JFR、Arthas 等工具的使用场景。",
            "能够通过 GC 日志判断 Young GC、Full GC、晋升失败、元空间膨胀等问题。",
        ],
    },
    "Mysql": {
        "核心认知": [
            "MySQL 学习主线是存储引擎、索引、事务、锁、日志和优化器。InnoDB 是重点。",
            "SQL 性能问题通常由数据分布、索引选择、执行计划、锁等待或事务边界引起。",
        ],
        "面试重点": [
            "B+Tree 索引、聚簇索引、覆盖索引、最左前缀、索引下推、回表。",
            "MVCC、ReadView、隔离级别、当前读/快照读、间隙锁和临键锁。",
            "redo log、undo log、binlog、两阶段提交、主从复制和 crash recovery。",
        ],
        "实践检查点": [
            "能用 `EXPLAIN` 分析 type、key、rows、Extra，并给出索引或 SQL 改写方案。",
            "能说明慢 SQL 治理流程：定位、复现、看执行计划、改索引/SQL、压测验证。",
        ],
    },
    "MongoDB": {
        "核心认知": [
            "MongoDB 适合文档模型、灵活 schema、水平扩展和高写入吞吐场景，但不应替代所有关系型建模。",
            "建模时优先围绕查询路径设计文档结构，权衡嵌入、引用、冗余和一致性成本。",
        ],
        "面试重点": [
            "BSON、集合、文档、索引、复制集、分片、WriteConcern、ReadConcern。",
            "唯一索引、复合索引、TTL 索引、覆盖查询和慢查询分析。",
        ],
        "实践检查点": [
            "能解释复制集选举、oplog 同步和主从延迟对读一致性的影响。",
            "能根据高基数字段和查询条件设计复合索引顺序。",
        ],
    },
    "Redis": {
        "核心认知": [
            "Redis 的优势来自内存访问、单线程事件循环、高效数据结构和丰富的持久化/复制能力。",
            "使用 Redis 要同时考虑数据结构、过期策略、淘汰策略、持久化、集群与缓存一致性。",
        ],
        "面试重点": [
            "SDS、dict、ziplist/listpack、quicklist、skiplist、intset 等底层结构。",
            "RDB、AOF、混合持久化、主从复制、哨兵、Cluster 槽位迁移。",
            "缓存穿透、击穿、雪崩、热 key、大 key、分布式锁和 Lua 原子性。",
        ],
        "实践检查点": [
            "能通过 `INFO`、`SLOWLOG`、`MEMORY`、`MONITOR` 等命令定位性能问题。",
            "能设计缓存更新策略，并说明旁路缓存、延迟双删、消息订阅补偿的取舍。",
        ],
    },
    "ES": {
        "核心认知": [
            "Elasticsearch 的核心是倒排索引、分片副本、近实时搜索和 Lucene 段文件。",
            "搜索质量依赖 mapping、分词器、相关性评分、查询 DSL 与业务排序策略的共同设计。",
        ],
        "面试重点": [
            "倒排索引、doc values、segment、refresh、flush、merge、translog。",
            "mapping 设计、text/keyword、分词器、bool query、聚合、分页和深分页。",
            "分片规划、写入链路、搜索链路、节点角色、集群健康状态。",
        ],
        "实践检查点": [
            "能解释为什么深分页昂贵，以及 `search_after`、scroll、PIT 的适用场景。",
            "能针对写多读多场景分别调整 refresh interval、bulk、routing、分片数。",
        ],
    },
    "MQ": {
        "核心认知": [
            "消息队列解决异步解耦、削峰填谷、最终一致性和广播通知，但会引入延迟、重复、乱序和一致性复杂度。",
            "选型要围绕吞吐、延迟、可靠性、顺序性、事务消息、生态和运维成本。",
        ],
        "面试重点": [
            "至少一次、最多一次、恰好一次的语义差异，以及幂等消费的工程实现。",
            "消息堆积、重试、死信、延迟消息、顺序消息、事务消息。",
        ],
        "实践检查点": [
            "能设计可靠消息最终一致性方案：本地事务表、事务消息、定时补偿和幂等处理。",
            "能从生产、Broker、消费端三段定位消息积压原因。",
        ],
    },
    "Kafka": {
        "核心认知": [
            "Kafka 是以日志为核心的高吞吐分布式消息系统，主题、分区、副本和 offset 是基础模型。",
            "吞吐来自顺序写、页缓存、批量发送、零拷贝和分区并行。",
        ],
        "面试重点": [
            "Producer ack、幂等生产、事务、分区器、ISR、Leader/Follower、副本同步。",
            "Consumer Group、Rebalance、offset 提交、消息重复和顺序消费。",
        ],
        "实践检查点": [
            "能解释 `acks=all`、`min.insync.replicas`、副本数之间的可靠性关系。",
            "能处理 Rebalance 过频、消费滞后和分区热点问题。",
        ],
    },
    "RocketMQ": {
        "核心认知": [
            "RocketMQ 以 NameServer、Broker、Producer、Consumer 为核心，适合金融级可靠消息和事务消息场景。",
            "理解 CommitLog、ConsumeQueue、IndexFile 可以帮助解释高吞吐和查询能力。",
        ],
        "面试重点": [
            "消息发送、存储、刷盘、主从同步、重试、死信、延迟消息、事务消息。",
            "顺序消息与普通消息的队列选择、消费锁和失败重试差异。",
        ],
        "实践检查点": [
            "能说明同步刷盘/异步刷盘、同步复制/异步复制对性能和可靠性的影响。",
            "能设计事务消息的半消息、回查和本地事务状态处理。",
        ],
    },
    "Spring": {
        "核心认知": [
            "Spring 的主线是 IoC 容器、Bean 生命周期、依赖注入、AOP 和扩展点。",
            "源码阅读应围绕 `refresh`、BeanDefinition、BeanPostProcessor、FactoryBean、代理创建展开。",
        ],
        "面试重点": [
            "Bean 生命周期、循环依赖三级缓存、作用域、自动装配、条件装配。",
            "JDK 动态代理、CGLIB、事务传播行为、事务失效场景。",
        ],
        "实践检查点": [
            "能解释为什么自调用会导致事务失效，以及如何通过代理边界修正。",
            "能用后置处理器或条件注解实现轻量扩展。",
        ],
    },
    "SpringBoot": {
        "核心认知": [
            "Spring Boot 的价值是自动配置、约定优于配置、Starter 生态和生产可观测能力。",
            "理解自动配置要抓住条件注解、配置属性绑定和 `spring.factories`/AutoConfiguration imports。",
        ],
        "面试重点": [
            "启动流程、自动配置原理、Starter 设计、配置加载顺序、Actuator。",
            "内嵌 Servlet 容器、日志系统、Runner、Profile 和外部化配置。",
        ],
        "实践检查点": [
            "能写一个自定义 Starter，并保证默认配置可覆盖、Bean 可条件装配。",
            "能排查自动配置未生效：条件报告、Bean 冲突、配置属性绑定失败。",
        ],
    },
    "SpringMVC": {
        "核心认知": [
            "Spring MVC 围绕 DispatcherServlet 组织请求分发、参数绑定、调用控制器和视图/响应渲染。",
            "理解 HandlerMapping、HandlerAdapter、Interceptor、MessageConverter 是排查 Web 问题的关键。",
        ],
        "面试重点": [
            "请求处理链路、参数解析、数据绑定、异常处理、拦截器和过滤器区别。",
            "REST 接口返回、内容协商、JSON 序列化和统一响应/异常封装。",
        ],
        "实践检查点": [
            "能定位接口 404、415、参数绑定失败和序列化异常。",
            "能设计全局异常处理和请求链路日志。",
        ],
    },
    "MyBatis": {
        "核心认知": [
            "MyBatis 是半自动 ORM，重点是 SQL 映射、Executor、缓存、插件和动态 SQL。",
            "它适合 SQL 可控、复杂查询多的场景，但需要团队治理 SQL 质量。",
        ],
        "面试重点": [
            "一级缓存、二级缓存、Mapper 代理、Executor、StatementHandler、ResultSetHandler。",
            "插件拦截链、动态 SQL、`#{} / ${}` 区别和 SQL 注入风险。",
        ],
        "实践检查点": [
            "能实现分页、审计字段、慢 SQL 记录等插件，并说明拦截点选择。",
            "能处理 N+1 查询、结果映射错误和缓存脏读问题。",
        ],
    },
    "SpringCloud": {
        "核心认知": [
            "Spring Cloud 是微服务治理工具集，关注服务注册发现、负载均衡、声明式调用、网关、熔断限流和配置管理。",
            "微服务不是简单拆应用，而是围绕团队边界、业务能力、数据自治和故障隔离进行架构设计。",
        ],
        "面试重点": [
            "注册发现、Ribbon/LoadBalancer、OpenFeign、Gateway、Hystrix/Resilience4j、配置中心。",
            "服务雪崩、超时、重试、熔断、限流、降级和链路追踪。",
        ],
        "实践检查点": [
            "能设计合理的超时与重试组合，避免放大故障。",
            "能说明微服务拆分后数据一致性、灰度发布和观测性的治理方式。",
        ],
    },
    "SpringCloudAlibaba": {
        "核心认知": [
            "Spring Cloud Alibaba 提供 Nacos、Sentinel、Seata、RocketMQ 等阿里生态治理组件。",
            "重点是理解各组件解决的治理问题，而不是只记注解和配置。",
        ],
        "面试重点": [
            "Nacos 注册配置、Sentinel 限流熔断、Seata 分布式事务、RocketMQ 消息集成。",
            "AP/CP、动态配置推送、流控规则、事务模式 AT/TCC/Saga。",
        ],
        "实践检查点": [
            "能根据业务一致性要求选择本地消息、TCC、Saga 或 Seata AT。",
            "能设计 Sentinel 规则并说明资源名、簇点链路、热点参数限流。",
        ],
    },
    "Nacos": {
        "核心认知": [
            "Nacos 同时承担服务发现和配置管理，关键是数据模型、健康检查、推送机制和一致性协议。",
            "注册中心关注实例可用性，配置中心关注变更传播、版本管理和灰度。",
        ],
        "面试重点": [
            "Namespace、Group、Service、Cluster、Instance、DataId、配置监听。",
            "临时实例/持久实例、心跳、健康检查、AP/CP、一致性与本地缓存。",
        ],
        "实践检查点": [
            "能说明配置动态刷新失败的排查路径：客户端监听、权限、DataId/Group、网络和本地缓存。",
            "能设计多环境、多租户配置隔离方式。",
        ],
    },
    "Dubbo": {
        "核心认知": [
            "Dubbo 是高性能 RPC 框架，核心链路包括服务暴露、注册发现、引用、集群容错、负载均衡和协议编解码。",
            "理解 URL 驱动、SPI 扩展和 Filter 链有助于掌握 Dubbo 的扩展能力。",
        ],
        "面试重点": [
            "服务暴露/引用流程、注册中心、协议、序列化、负载均衡、容错策略、泛化调用。",
            "线程模型、连接管理、异步调用、Filter、Router、Directory、Invoker。",
        ],
        "实践检查点": [
            "能根据接口延迟和失败率选择超时、重试、熔断和降级策略。",
            "能定位 RPC 调用慢：客户端、网络、序列化、服务端线程池、下游依赖。",
        ],
    },
    "ZooKeeper": {
        "核心认知": [
            "ZooKeeper 提供一致性元数据协调，适合配置、命名、选主、分布式锁等小数据强一致场景。",
            "不要把 ZooKeeper 当作大数据存储或高频业务读写数据库。",
        ],
        "面试重点": [
            "ZNode、Watcher、Session、ACL、ZXID、Leader 选举、ZAB、过半机制。",
            "临时节点、顺序节点、分布式锁、羊群效应和 Curator 封装。",
        ],
        "实践检查点": [
            "能解释会话过期与连接断开的区别，以及对临时节点的影响。",
            "能设计可重入、公平、可超时的分布式锁，并处理锁释放异常。",
        ],
    },
    "Netty": {
        "核心认知": [
            "Netty 是基于事件驱动和 Reactor 模型的高性能网络框架，核心是 EventLoop、Channel、Pipeline 和 ByteBuf。",
            "高性能来自非阻塞 IO、线程模型、内存池、零拷贝和减少上下文切换。",
        ],
        "面试重点": [
            "NIO/Reactor、Boss/Worker、ChannelPipeline、Handler、ByteBuf、粘包拆包。",
            "编解码器、心跳、空闲检测、内存泄漏检测、背压和写缓冲水位。",
        ],
        "实践检查点": [
            "能实现一个长度字段或分隔符协议，并处理半包/粘包。",
            "能排查 Netty 内存泄漏、EventLoop 阻塞和连接数异常。",
        ],
    },
    "PHP7": {
        "核心认知": [
            "PHP7 内核重点包括 Zend 引擎、zval、HashTable、内存管理、OPcache、函数调用和对象模型。",
            "理解引用计数、写时复制和垃圾回收有助于解释 PHP 性能与内存行为。",
        ],
        "面试重点": [
            "SAPI、生命周期、zval 结构、HashTable、内存分配、编译执行流程。",
            "引用计数、循环引用回收、OPcache、函数和对象实现。",
        ],
        "实践检查点": [
            "能解释大数组复制、引用传递和写时复制的性能影响。",
            "能从 FPM、OPcache、慢日志和内存峰值定位 PHP 服务问题。",
        ],
    },
    "Summary": {
        "核心认知": [
            "重点汇总用于建立全局知识地图，先形成主题之间的边界，再进入具体专题深挖。",
            "建议按语言基础、JVM、数据库、缓存、消息队列、框架、微服务、网络通信、搜索与分布式协调建立复习路径。",
        ],
        "面试重点": [
            "每个技术点都应能回答：解决什么问题、核心原理是什么、常见故障如何排查、在项目中如何落地。",
            "不要孤立背题，应把业务场景、架构取舍、性能指标和故障案例串起来。",
        ],
        "实践检查点": [
            "为每个专题准备一个真实项目案例，说明背景、方案、难点、指标和复盘。",
            "复习时优先补齐高频基础，再补源码细节和边界问题。",
        ],
    },
}


TOPIC_TRENDS = {
    "Java": [
        "主流生产环境仍以 Java 8/11/17 为主，新项目建议优先评估 Java 17 或 Java 21 LTS。",
        "现代 Java 重点关注 Record、Sealed Class、Pattern Matching、Virtual Threads、结构化并发等能力，但面试仍需夯实集合、并发和内存模型。",
    ],
    "JVM": [
        "当前服务端常见组合是 JDK 17/21 + G1，低延迟场景可评估 ZGC 或 Shenandoah。",
        "JVM 调优从经验参数转向可观测驱动：先采集 GC 日志、JFR、线程栈和对象分配，再做小步验证。",
    ],
    "Mysql": [
        "MySQL 8.0 是当前主流版本，窗口函数、CTE、直方图、Invisible Index、Instant DDL 等能力值得掌握。",
        "生产治理重点从单 SQL 优化扩展到容量规划、慢查询治理、备份恢复、主从延迟和在线变更。",
    ],
    "MongoDB": [
        "MongoDB 6/7/8 持续强化分片、时间序列、变更流和查询性能，建模仍应围绕访问模式设计。",
        "不要把灵活 schema 等同于无 schema，生产环境需要字段规范、索引规范和容量治理。",
    ],
    "Redis": [
        "Redis 7.x 强化多线程 IO、函数、ACL、Cluster 和复制能力；生产上还需要关注 Valkey/Redis 生态变化。",
        "缓存系统的重点不只是命令使用，还包括容量评估、热 key 治理、大 key 拆分、持久化恢复和多级缓存。",
    ],
    "ES": [
        "Elasticsearch 8.x 默认安全能力更完整，向量检索、混合检索、运行时字段和 ILM 是近年重点。",
        "搜索系统需要同时治理写入、查询、索引生命周期、分片容量和相关性评估。",
    ],
    "MQ": [
        "消息系统的共同趋势是云原生部署、可观测性增强、Exactly-once 语义边界清晰化和事件驱动架构。",
        "面试回答应明确消息语义：Broker 保证什么、客户端保证什么、业务幂等补什么。",
    ],
    "Kafka": [
        "Kafka 3.x 进入 KRaft 去 ZooKeeper 架构阶段，新集群应关注 Controller Quorum、分层存储和再均衡优化。",
        "Kafka 的核心仍是分区日志模型，所有吞吐、顺序、可靠性和扩展性问题都应回到分区与副本分析。",
    ],
    "RocketMQ": [
        "RocketMQ 5.x 引入 Proxy、Pop 消费、轻量队列等能力，云原生和多协议接入能力增强。",
        "事务消息、延迟消息、顺序消息仍是 RocketMQ 区分度较高的面试与落地重点。",
    ],
    "Spring": [
        "Spring Framework 6 基于 Jakarta EE 9+，要求 Java 17+，新项目需要注意 `javax` 到 `jakarta` 的迁移。",
        "Spring 的核心竞争力仍是容器、AOP、事务和生态整合，源码学习应服务于排障和扩展。",
    ],
    "SpringBoot": [
        "Spring Boot 3.x 基于 Spring 6 和 Java 17+，原生镜像、观测性、配置绑定和自动配置机制都有变化。",
        "老项目从 2.x 升级到 3.x 时，要重点处理 Jakarta 包名、依赖版本、Spring Security 和第三方 Starter 兼容性。",
    ],
    "SpringMVC": [
        "Spring MVC 在 Spring 6 后同样迁移到 Jakarta Servlet API，过滤器、拦截器和异常处理链路仍是高频问题。",
        "接口治理重点包括统一错误码、参数校验、幂等、限流、链路追踪和访问日志。",
    ],
    "MyBatis": [
        "MyBatis 仍适合 SQL 可控场景，MyBatis-Plus 等增强工具可提升效率但不能替代 SQL 与索引能力。",
        "生产问题常集中在动态 SQL 失控、N+1 查询、分页性能、慢 SQL 和 Mapper 映射不一致。",
    ],
    "SpringCloud": [
        "Spring Cloud 2023/2024 版本线围绕 Spring Boot 3.x 演进，Netflix 老组件逐步被 Gateway、LoadBalancer、Resilience4j 替代。",
        "微服务治理重点转向可观测、弹性、灰度、配置安全、服务网格和平台工程。",
    ],
    "SpringCloudAlibaba": [
        "Spring Cloud Alibaba 持续围绕 Nacos、Sentinel、Seata、RocketMQ 生态演进，版本兼容矩阵必须优先确认。",
        "生产落地应关注规则治理、配置权限、注册中心容量和分布式事务边界。",
    ],
    "Nacos": [
        "Nacos 2.x 使用 gRPC 长连接提升推送与注册性能，部署时需关注 9848/9849 等端口和集群寻址。",
        "配置中心要治理命名空间、权限、灰度、回滚和敏感配置加密。",
    ],
    "Dubbo": [
        "Dubbo 3.x 强化应用级服务发现、Triple 协议、云原生和 Mesh 适配。",
        "RPC 治理重点是接口粒度、超时重试、线程池隔离、序列化兼容和调用链观测。",
    ],
    "ZooKeeper": [
        "ZooKeeper 仍常用于协调与元数据，但新系统应谨慎评估是否可由 etcd、Nacos、KRaft 或云服务替代。",
        "使用 ZooKeeper 时要控制节点数量、watcher 数量、会话超时和磁盘延迟。",
    ],
    "Netty": [
        "Netty 4.1 仍是主流，HTTP/2、QUIC、native transport、内存泄漏检测和背压控制是生产关注点。",
        "不要在 EventLoop 中执行阻塞逻辑，业务耗时任务应切到独立线程池。",
    ],
    "PHP7": [
        "PHP 8.x 已成为主流演进方向，JIT、Union Types、Attributes、Fibers、Readonly 等特性需要补充了解。",
        "PHP7 内核知识仍可用于理解 zval、HashTable、引用计数、写时复制和 FPM 性能问题。",
    ],
    "Summary": [
        "当前后端知识体系更强调工程化闭环：架构设计、性能优化、稳定性、可观测、安全和成本。",
        "复习时建议将每个知识点整理成：原理、适用场景、边界、故障案例、项目落地五段式。",
    ],
}


SECTION_RULES = [
    (
        "Java",
        ["基础", "语法", "变量", "常量", "包装", "字符串"],
        [
            "补充：现代 Java 基础题更关注语义边界，例如值传递、不可变对象、自动装箱缓存、字符串常量池和泛型擦除。",
            "实践：编码时优先使用清晰的不可变模型和显式类型边界，避免依赖隐式转换或包装类型比较。",
            "误区：`final` 只能保证引用不可变，不能保证引用对象内部状态不可变。",
        ],
    ),
    (
        "Java",
        ["try-catch-finally"],
        [
            "补充：异常处理要区分业务异常、系统异常和资源清理，重点掌握执行顺序与异常传播。",
            "实践：资源关闭优先使用 `try-with-resources`，finally 中避免 return 或吞异常。",
            "误区：finally 通常会执行，但不是绝对保证，例如 JVM 退出、进程被强杀或机器断电时不会执行。",
        ],
    ),
    (
        "Java",
        ["集合", "hashmap", "concurrenthashmap", "arraylist", "linkedlist"],
        [
            "补充：集合问题应从数据结构、扩容策略、迭代一致性、线程安全和内存占用五个角度回答。",
            "实践：高并发读写优先选择并发容器或不可变快照，避免用外部大锁包裹普通集合造成吞吐下降。",
            "误区：ConcurrentHashMap 保证单次操作线程安全，不代表复合业务操作天然原子。",
        ],
    ),
    (
        "Java",
        [
            "线程",
            "多线程",
            "juc",
            "aqs",
            "锁",
            "volatile",
            "synchronized",
            "threadlocal",
            "线程池",
        ],
        [
            "补充：JDK 21 的虚拟线程适合大量阻塞 IO 场景，但不适合 CPU 密集型任务，也不能消除共享状态同步问题。",
            "实践：线程池参数应结合任务类型、队列长度、拒绝策略、监控指标和下游容量一起设计。",
            "排障：线程问题优先看 `jstack`、线程池队列、活跃线程数、锁等待和上下文切换。",
        ],
    ),
    (
        "Java",
        ["io", "nio", "文件", "流"],
        [
            "补充：BIO/NIO/AIO 的差异本质是阻塞模型、事件通知机制和线程资源使用方式不同。",
            "实践：高并发网络 IO 通常选择 NIO/Reactor 框架，文件传输关注缓冲区、零拷贝和背压。",
            "误区：NIO 不必然更快，小规模同步调用中 BIO 可能更简单且足够稳定。",
        ],
    ),
    (
        "JVM",
        ["垃圾", "gc", "收集器", "g1", "zgc", "cms"],
        [
            "补充：G1 是通用低停顿收集器，ZGC/Shenandoah 更适合大堆低延迟场景；CMS 已不再是新版本首选。",
            "实践：GC 优化先确认目标是吞吐、停顿还是成本，再结合 GC 日志和对象分配热点调整。",
            "排障：频繁 Full GC 常见原因包括老年代晋升压力、元空间膨胀、大对象分配和内存泄漏。",
        ],
    ),
    (
        "JVM",
        ["类加载", "class", "双亲"],
        [
            "补充：类加载包括加载、验证、准备、解析、初始化，双亲委派主要用于保证核心类库一致性和安全边界。",
            "实践：插件化、热部署、容器隔离会定制 ClassLoader，排查冲突时要确认同名类由哪个加载器加载。",
            "误区：破坏双亲委派不是错误本身，关键是是否能控制类可见性和版本隔离。",
        ],
    ),
    (
        "Mysql",
        ["索引", "b+", "b树", "回表", "覆盖", "最左"],
        [
            "补充：MySQL 8.0 优化器会结合统计信息、直方图和成本模型选择执行计划，索引存在不代表一定会用。",
            "实践：设计复合索引时按等值、范围、排序、覆盖的优先级综合考虑，同时关注字段选择性和写入成本。",
            "排障：慢 SQL 分析先看 `EXPLAIN ANALYZE`、扫描行数、回表次数、临时表和文件排序。",
        ],
    ),
    (
        "Mysql",
        ["事务", "mvcc", "锁", "隔离", "redo", "undo", "binlog"],
        [
            "补充：InnoDB 通过 undo log 和 ReadView 实现 MVCC，通过 redo log 保证崩溃恢复，通过 binlog 支持复制和归档。",
            "实践：长事务会拖住 undo 清理并影响版本链，线上应限制事务时长和交互式事务。",
            "误区：可重复读不等于完全不会幻读，InnoDB 通过 next-key lock 在当前读场景解决幻读。",
        ],
    ),
    (
        "Redis",
        ["数据结构", "sds", "dict", "跳表", "listpack", "ziplist"],
        [
            "补充：Redis 7 逐步以 listpack 替代 ziplist，底层编码会随元素数量和大小自动转换。",
            "实践：选择数据类型时要同时考虑命令复杂度、内存编码、过期粒度和后续扩展。",
            "排障：大 key 会造成阻塞、复制延迟和迁移抖动，应通过拆分、压缩或异步清理治理。",
        ],
    ),
    (
        "Redis",
        ["缓存", "过期", "淘汰", "穿透", "击穿", "雪崩", "锁"],
        [
            "补充：缓存一致性没有银弹，应根据读写比例、容忍延迟和失败补偿选择旁路缓存、订阅失效或双写方案。",
            "实践：热 key 使用本地缓存、请求合并、分片或限流；分布式锁要设置唯一 token、过期时间和续期策略。",
            "误区：删除缓存后再写数据库容易产生脏缓存，常见方案是先写库再删缓存并配合补偿。",
        ],
    ),
    (
        "ES",
        ["索引", "mapping", "分词", "查询", "dsl", "评分", "聚合", "分页"],
        [
            "补充：ES 8.x 中 mapping 设计仍是性能和搜索质量的核心，text/keyword、doc_values、analyzer 选择要前置规划。",
            "实践：深分页优先使用 `search_after` + PIT，批量导出使用 scroll，普通分页避免过大 `from + size`。",
            "排障：查询慢时检查分片数、段数量、缓存命中、脚本排序、高基数聚合和 refresh/merge 压力。",
        ],
    ),
    (
        "Kafka",
        ["生产", "producer", "ack", "分区", "副本", "消费者", "rebalance", "offset"],
        [
            "补充：Kafka 3.x 新集群可使用 KRaft，不再依赖 ZooKeeper；可靠性仍由 ack、ISR、副本和幂等共同决定。",
            "实践：消费端必须设计幂等，offset 提交要与业务处理结果绑定，避免先提交后处理导致消息丢失。",
            "排障：消费延迟从生产速率、分区热点、Rebalance、消费耗时和下游依赖五处定位。",
        ],
    ),
    (
        "RocketMQ",
        ["事务", "顺序", "延迟", "消费", "存储", "刷盘", "主从"],
        [
            "补充：RocketMQ 5.x 架构引入 Proxy，客户端接入和云原生部署方式与 4.x 有差异。",
            "实践：事务消息要处理半消息、事务回查和幂等；顺序消息要保证同一业务键路由到同一队列。",
            "排障：消息堆积需区分 Broker 存储瓶颈、消费线程不足、单条消息卡死和下游服务慢。",
        ],
    ),
    (
        "Spring",
        ["ioc", "bean", "容器", "生命周期", "循环依赖"],
        [
            "补充：Spring 6 要求 Java 17+ 并迁移到 Jakarta 命名空间，理解 Bean 生命周期仍是排查问题的基础。",
            "实践：复杂初始化逻辑优先使用明确的生命周期回调，避免在构造器里访问尚未注入完成的依赖。",
            "误区：三级缓存只能解决部分单例 setter 循环依赖，构造器循环依赖和原型循环依赖无法靠它解决。",
        ],
    ),
    (
        "Spring",
        ["aop", "代理", "事务", "transaction"],
        [
            "补充：Spring AOP 基于代理，事务、缓存、异步等注解都依赖代理边界。",
            "实践：事务方法避免自调用，异常回滚规则要明确，跨服务事务优先采用最终一致性方案。",
            "误区：`@Transactional` 默认只对运行时异常回滚，且 private/final 方法通常不会被代理增强。",
        ],
    ),
    (
        "SpringBoot",
        ["自动配置", "starter", "启动", "配置"],
        [
            "补充：Spring Boot 3 使用新的 AutoConfiguration imports 机制，并全面基于 Spring Framework 6。",
            "实践：自定义 Starter 应提供条件装配、配置元数据、默认值和清晰的覆盖方式。",
            "排障：自动配置不生效时查看条件评估报告、Bean 定义冲突、配置绑定和依赖版本。",
        ],
    ),
    (
        "SpringMVC",
        ["dispatcherservlet", "handler", "参数", "异常", "拦截", "过滤"],
        [
            "补充：请求链路可拆为过滤器、DispatcherServlet、HandlerMapping、HandlerAdapter、参数解析、消息转换和异常处理。",
            "实践：统一异常处理应区分业务异常、参数异常、系统异常和下游异常，并输出可观测的 trace 信息。",
            "误区：Filter 属于 Servlet 容器链路，Interceptor 属于 Spring MVC 链路，二者生命周期和能力边界不同。",
        ],
    ),
    (
        "MyBatis",
        ["executor", "插件", "缓存", "动态", "mapper"],
        [
            "补充：MyBatis 插件通过拦截 Executor、StatementHandler、ParameterHandler、ResultSetHandler 扩展执行链路。",
            "实践：分页、审计、慢 SQL 插件要谨慎处理 SQL 改写和参数绑定，避免破坏执行计划。",
            "误区：二级缓存跨 SqlSession，若更新链路复杂或多服务写入，容易产生一致性问题。",
        ],
    ),
    (
        "SpringCloud",
        ["网关", "feign", "ribbon", "负载", "熔断", "限流", "注册", "配置"],
        [
            "补充：新版本更推荐 Spring Cloud LoadBalancer、Gateway、OpenFeign、Resilience4j，Hystrix/Ribbon 已不是新项目首选。",
            "实践：超时、重试、熔断、限流必须成套设计，错误组合会放大流量并拖垮下游。",
            "排障：微服务调用问题按入口网关、注册发现、负载均衡、网络、服务线程池、下游依赖逐层定位。",
        ],
    ),
    (
        "Dubbo",
        ["rpc", "暴露", "引用", "协议", "负载", "容错", "线程"],
        [
            "补充：Dubbo 3 支持 Triple 协议和应用级服务发现，适合云原生与多语言互通场景。",
            "实践：接口超时应小于调用方整体超时预算，重试只适合幂等读或可重复操作。",
            "排障：RPC 慢调用要同时看客户端等待、网络耗时、序列化、服务端线程池和业务执行。",
        ],
    ),
    (
        "ZooKeeper",
        ["zab", "leader", "watcher", "session", "节点", "锁"],
        [
            "补充：ZooKeeper 强在小数据协调和顺序一致性，不适合高频大数据读写。",
            "实践：分布式锁使用临时顺序节点并监听前一个节点，避免所有客户端监听同一节点造成羊群效应。",
            "排障：连接抖动时重点检查 GC 停顿、网络延迟、磁盘 IO 和 session timeout 配置。",
        ],
    ),
    (
        "Netty",
        ["eventloop", "pipeline", "bytebuf", "粘包", "拆包", "nio", "reactor"],
        [
            "补充：Netty 的核心约束是 EventLoop 不能阻塞，Pipeline 中 Handler 的线程模型必须明确。",
            "实践：自定义协议优先使用长度字段、魔数、版本号、序列化类型和校验字段，便于升级与排障。",
            "排障：内存泄漏通过 ResourceLeakDetector、引用计数检查和 ByteBuf 释放路径定位。",
        ],
    ),
    (
        "PHP7",
        ["zval", "hashtable", "内存", "引用", "gc", "opcache", "fpm"],
        [
            "补充：PHP 8 的 JIT、类型系统和协程生态改变了部分性能边界，但 zval/HashTable/引用计数仍是理解内核的基础。",
            "实践：PHP 服务性能优先关注 FPM 进程模型、OPcache 命中率、慢日志、内存峰值和外部 IO。",
            "误区：引用传递不一定更省内存，写时复制和引用计数状态会影响实际行为。",
        ],
    ),
]


DEFAULT_SECTION_NOTES = [
    "补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。",
    "实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。",
]


DETAIL_SECTION_RULES = [
    (
        "Java",
        ["equals和hashcode", "equals与hashcode"],
        [
            (
                "核心结论",
                [
                    "`equals` 用于判断两个对象在业务语义上是否相等，`hashCode` 用于支持哈希容器快速定位桶位置。",
                    "只要重写 `equals`，通常就必须同时重写 `hashCode`，否则对象放入 `HashMap`、`HashSet` 等容器后会出现查找失败、重复元素等问题。",
                ],
            ),
            (
                "基本契约",
                [
                    "自反性：`x.equals(x)` 必须为 true。",
                    "对称性：`x.equals(y)` 为 true 时，`y.equals(x)` 也必须为 true。",
                    "传递性：`x.equals(y)` 和 `y.equals(z)` 都为 true 时，`x.equals(z)` 必须为 true。",
                    "一致性：对象参与比较的字段未变化时，多次调用结果应一致。",
                    "非空性：任何非 null 对象 `x.equals(null)` 都应返回 false。",
                ],
            ),
            (
                "hashCode 规则",
                [
                    "如果两个对象 `equals` 为 true，它们的 `hashCode` 必须相同。",
                    "如果两个对象 `hashCode` 相同，它们不一定 `equals` 为 true，因为哈希冲突是允许的。",
                    "`hashCode` 应尽量让不同对象分布均匀，避免哈希桶退化。",
                ],
            ),
            (
                "工程实践",
                [
                    "用于相等判断的字段应尽量稳定，不建议使用会频繁变化的字段作为 `equals/hashCode` 依据。",
                    "实体类如果使用数据库自增 ID，要注意对象持久化前 ID 为空时的相等性问题。",
                    "Java 16+ 的 `record` 会自动生成基于组件字段的 `equals/hashCode/toString`，适合不可变值对象。",
                    "Lombok 的 `@EqualsAndHashCode` 要谨慎配置 `callSuper` 和包含字段，继承层级复杂时尤其容易出错。",
                ],
            ),
            (
                "面试回答",
                [
                    "我会先说明 `equals` 是业务相等，`hashCode` 是哈希容器定位；再强调两者契约：相等对象必须有相同哈希值；最后结合 `HashMap` 说明如果只重写 `equals` 不重写 `hashCode`，相同业务对象可能落到不同桶，导致查不到或去重失败。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["和equals", "==和equals"],
        [
            (
                "核心区别",
                [
                    "`==` 比较的是两侧值本身；对于基本类型比较数值，对于引用类型比较对象引用地址。",
                    "`equals` 是对象方法，默认实现等价于 `==`，但很多类会重写它来表达业务相等。",
                ],
            ),
            (
                "典型例子",
                [
                    "`String` 重写了 `equals`，所以通常用 `equals` 比较字符串内容。",
                    "包装类型存在缓存，例如 `Integer.valueOf(-128~127)` 通常复用对象，不能用 `==` 判断包装类型数值相等。",
                    "枚举可以使用 `==`，因为枚举实例天然单例且类型安全。",
                ],
            ),
            (
                "工程实践",
                [
                    '字符串常量比较建议写成 `"OK".equals(value)`，避免 `value` 为 null 时 NPE。',
                    "业务对象比较应明确相等语义，并保持 `equals/hashCode` 一致。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["exact:final"],
        [
            (
                "使用场景",
                [
                    "修饰类：类不能被继承，例如 `String`。",
                    "修饰方法：方法不能被子类重写。",
                    "修饰变量：变量只能赋值一次；引用类型变量不可重新指向其他对象，但对象内部状态仍可能变化。",
                ],
            ),
            (
                "并发语义",
                [
                    "`final` 字段在构造完成后具备特殊的安全发布语义，其他线程通常能看到正确初始化后的值。",
                    "`final` 不等于线程安全，如果引用指向的是可变对象，对象内部仍需要同步或不可变设计。",
                ],
            ),
            (
                "面试误区",
                [
                    "`final List` 不能重新赋值为另一个 List，但仍然可以调用 `add` 修改集合内容。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["try-catch-finally"],
        [
            (
                "核心作用",
                [
                    "`try`：包裹可能抛出异常的代码。",
                    "`catch`：捕获并处理指定类型的异常，可以有多个 catch，顺序应从具体异常到父类异常。",
                    "`finally`：无论 try/catch 是否抛出异常，通常都会执行，常用于释放资源或做收尾动作。",
                ],
            ),
            (
                "执行顺序",
                [
                    "正常执行：先执行 try，再执行 finally。",
                    "发生异常且被捕获：先执行 try 中异常前的代码，再执行匹配的 catch，最后执行 finally。",
                    "发生异常但未被捕获：先执行 try 中异常前的代码，再执行 finally，然后异常继续向外抛出。",
                    "如果 try 或 catch 中有 return，finally 通常仍会在方法真正返回前执行。",
                ],
            ),
            (
                "finally 不一定执行的情况",
                [
                    "JVM 进程直接退出，例如 `System.exit(0)`。",
                    "JVM 崩溃或进程被强杀，例如 `kill -9`。",
                    "执行 finally 前线程被强制终止或机器断电。",
                    "CPU 关闭这种说法不准确，更准确地说是进程或虚拟机没有机会继续执行字节码。",
                ],
            ),
            (
                "return 与 finally",
                [
                    "如果 try/catch 和 finally 都有 return，finally 的 return 会覆盖前面的 return。",
                    "不建议在 finally 中写 return，因为它会吞掉异常或覆盖真实返回值，导致排查困难。",
                    "如果 finally 修改的是返回对象的内部状态，调用方可能看到修改后的对象；如果只是修改局部基本类型变量，通常不会改变已经确定的返回值。",
                ],
            ),
            (
                "资源释放",
                [
                    "传统写法会在 finally 中关闭连接、流、锁等资源。",
                    "Java 7 后更推荐 `try-with-resources`，由编译器自动生成关闭逻辑。",
                    "资源类需要实现 `AutoCloseable` 或 `Closeable`。",
                ],
            ),
            (
                "try-with-resources 示例",
                [
                    {
                        "lang": "java",
                        "code": """import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class TryWithResourcesDemo {
    public static String readFirstLine(String path) throws IOException {
        try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
            return reader.readLine();
        }
    }
}""",
                    }
                ],
            ),
            (
                "finally 覆盖 return 示例",
                [
                    {
                        "lang": "java",
                        "code": """public class FinallyReturnDemo {
    public static int value() {
        try {
            return 1;
        } finally {
            return 2; // 不推荐：会覆盖 try 中的 return
        }
    }

    public static void main(String[] args) {
        System.out.println(value()); // 输出 2
    }
}""",
                    }
                ],
            ),
            (
                "实践建议",
                [
                    "不要用异常控制正常业务流程。",
                    "catch 中至少要记录关键上下文，不能简单吞掉异常。",
                    "不要捕获过宽的异常后不处理，例如空 catch 或只打印堆栈。",
                    "finally 中避免 return、throw 新异常或执行复杂业务逻辑。",
                    "资源关闭优先使用 try-with-resources。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["语法糖"],
        [
            (
                "核心概念",
                [
                    "语法糖是编程语言提供的便捷语法，本身不增加 JVM 的基础能力，通常会在编译期被转换成已有语法或字节码结构。",
                    "理解语法糖的关键是知道它在编译后变成什么，以及可能带来的边界问题。",
                ],
            ),
            (
                "switch 支持字符串",
                [
                    "Java 7 开始支持 `switch` 使用 `String`。",
                    "编译后通常会先通过 `hashCode` 分组，再用 `equals` 做精确匹配，最后映射到整数分支。",
                    "注意：字符串 hash 冲突时仍会用 `equals` 确认，因此语义是正确的。",
                ],
            ),
            (
                "字符串 + 拼接",
                [
                    "早期 Java 中，非编译期常量的字符串拼接通常会被编译成 `StringBuilder` append。",
                    "Java 9 之后字符串拼接使用 `invokedynamic` 和 `StringConcatFactory` 优化。",
                    "循环中大量拼接字符串仍建议显式使用 `StringBuilder`，避免产生过多中间对象。",
                ],
            ),
            (
                "泛型与类型擦除",
                [
                    "Java 泛型主要是编译期类型检查，运行期会进行类型擦除。",
                    "例如 `List<String>` 和 `List<Integer>` 运行期原始类型都是 `List`。",
                    "泛型擦除会导致不能直接 `new T()`、不能创建泛型数组、运行期无法直接判断具体泛型参数。",
                ],
            ),
            (
                "自动装箱与拆箱",
                [
                    "自动装箱是基本类型自动转换为包装类型，例如 `int` 到 `Integer`。",
                    "自动拆箱是包装类型自动转换为基本类型。",
                    "注意：包装类型为 null 时自动拆箱会触发 `NullPointerException`。",
                    "包装类型比较不要随意使用 `==`，应优先使用 `equals` 或先转基本类型。",
                ],
            ),
            (
                "变长参数",
                [
                    "变长参数本质是数组，方法内部按数组处理。",
                    "一个方法最多只能有一个变长参数，并且必须放在参数列表最后。",
                    "重载时变长参数可能造成调用歧义，公共 API 要谨慎设计。",
                ],
            ),
            (
                "增强 for 循环",
                [
                    "增强 for 是遍历数组或 `Iterable` 的简化语法。",
                    "遍历集合时底层通常使用 `Iterator`。",
                    "注意：增强 for 遍历集合时不要直接调用集合的 `remove`，否则可能触发 `ConcurrentModificationException`；需要删除时使用迭代器的 `remove`。",
                ],
            ),
            (
                "内部类",
                [
                    "内部类编译后会生成独立的 `.class` 文件，例如 `OuterClass$InnerClass.class`。",
                    "非静态内部类会持有外部类实例引用。",
                    "静态内部类不持有外部类实例引用，常用于 Builder、Holder 单例等场景。",
                ],
            ),
            (
                "枚举类",
                [
                    "`enum` 编译后本质上是继承 `java.lang.Enum` 的 final 类。",
                    "枚举实例是固定数量的静态常量，天然适合单例、状态、类型码等场景。",
                    "枚举可以定义字段、构造器和方法，也可以实现接口。",
                ],
            ),
            (
                "断言",
                [
                    "`assert` 用于开发和测试阶段校验不变量。",
                    "默认情况下 JVM 不启用断言，需要通过 `-ea` 或 `-enableassertions` 开启。",
                    "不要用断言替代业务参数校验，因为生产环境可能未启用断言。",
                ],
            ),
            (
                "Lambda 表达式",
                [
                    "Lambda 依赖函数式接口。",
                    "它不是简单地编译成匿名内部类，通常通过 `invokedynamic` 和 `LambdaMetafactory.metafactory` 在运行期动态生成调用逻辑。",
                    "Lambda 可以捕获 effectively final 的局部变量。",
                ],
            ),
            (
                "try-with-resources",
                [
                    "Java 7 引入，用于自动关闭实现 `AutoCloseable` 或 `Closeable` 的资源。",
                    "编译器会生成等价的 finally 关闭逻辑，并处理 suppressed exception。",
                    "适合文件流、网络连接、数据库连接等需要关闭的资源。",
                ],
            ),
            (
                "var 类型推断",
                [
                    "Java 10 引入 `var` 局部变量类型推断。",
                    "`var` 只能用于局部变量，不能用于字段、方法参数和返回值。",
                    "类型由初始化表达式在编译期确定，并不是动态类型。",
                    "类型明显时使用 `var` 可以减少冗余；类型不明显时滥用会降低可读性。",
                ],
            ),
            (
                "示例代码",
                [
                    {
                        "lang": "java",
                        "code": """import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.List;

public class SyntaxSugarDemo {
    public static void main(String[] args) throws IOException {
        // switch 支持字符串
        String type = "A";
        switch (type) {
            case "A" -> System.out.println("type A");
            case "B" -> System.out.println("type B");
            default -> System.out.println("unknown");
        }

        // 自动装箱与拆箱
        Integer count = 1; // int -> Integer
        int value = count; // Integer -> int

        // 增强 for 循环
        for (String item : List.of("java", "spring")) {
            System.out.println(item);
        }

        // try-with-resources
        try (BufferedReader reader = new BufferedReader(new FileReader("README.md"))) {
            System.out.println(reader.readLine());
        }

        // var 局部变量类型推断
        var message = "hello";
        System.out.println(message);
    }
}""",
                    }
                ],
            ),
            (
                "面试回答",
                [
                    "回答 Java 语法糖时，可以先说明它是编译器层面的便利语法，再举例说明增强 for、泛型擦除、自动装箱、枚举、try-with-resources、Lambda 等最终会被转换成什么。",
                    "重点不要只背语法，要能说出边界问题，例如拆箱 NPE、泛型擦除、增强 for 删除元素、finally 资源关闭、Lambda 捕获变量限制。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["反射"],
        [
            (
                "核心概念",
                [
                    "反射允许程序在运行期获取类信息并动态创建对象、访问字段、调用方法。",
                    "常用入口包括 `Class`、`Constructor`、`Field`、`Method`。",
                ],
            ),
            (
                "典型使用",
                [
                    "Spring IoC 根据类元信息创建 Bean 并注入依赖。",
                    "MyBatis 根据 Mapper 接口和结果映射动态调用。",
                    "序列化框架通过反射读取字段和构造对象。",
                ],
            ),
            (
                "注意事项",
                [
                    "反射绕过编译期检查，错误更容易在运行期暴露。",
                    "反射调用通常比直接调用慢，但现代 JVM 已做大量优化，实际要以场景和压测为准。",
                    "在 Java 9+ 模块系统下，强封装会影响对非公开成员的反射访问。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["注解"],
        [
            (
                "核心概念",
                [
                    "注解是附加在代码元素上的元数据，本身不直接改变程序逻辑，需要编译器、框架或运行期反射解析。",
                    "常见元注解包括 `@Target`、`@Retention`、`@Documented`、`@Inherited`、`@Repeatable`。",
                ],
            ),
            (
                "Retention",
                [
                    "`SOURCE`：只保留在源码，例如 `@Override`。",
                    "`CLASS`：进入 class 文件，但运行期不可反射读取。",
                    "`RUNTIME`：运行期可通过反射读取，框架注解通常使用它。",
                ],
            ),
            (
                "工程实践",
                [
                    "自定义注解通常配合 AOP、拦截器、BeanPostProcessor 或编译期处理器使用。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["序列化"],
        [
            (
                "核心概念",
                [
                    "序列化是把对象转换为可存储或可传输格式，反序列化是把数据恢复为对象。",
                    "Java 原生序列化依赖 `Serializable`，但性能、安全性和跨语言能力较弱。",
                ],
            ),
            (
                "常见方案",
                [
                    "JSON：可读性好，常用于 HTTP API，但体积较大。",
                    "Protobuf：体积小、跨语言、性能好，适合 RPC 和消息。",
                    "Kryo/Hessian：常见于 Java 生态 RPC 或缓存场景。",
                ],
            ),
            (
                "风险",
                [
                    "反序列化不可信数据可能造成安全漏洞。",
                    "类结构变更会带来兼容性问题，需要设计 schema 演进策略。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["动态代理"],
        [
            (
                "两类代理",
                [
                    "JDK 动态代理：基于接口生成代理类，目标类必须实现接口。",
                    "CGLIB：基于继承生成子类代理，不能代理 final 类和 final 方法。",
                ],
            ),
            (
                "典型应用",
                [
                    "Spring AOP、声明式事务、RPC 客户端、MyBatis Mapper 都大量使用代理思想。",
                ],
            ),
            (
                "面试重点",
                [
                    "Spring 默认在有接口时优先使用 JDK 动态代理，没有接口时使用 CGLIB。",
                    "代理增强发生在代理对象调用路径上，自调用绕过代理会导致事务、缓存、异步等注解失效。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["cas"],
        [
            (
                "核心概念",
                [
                    "CAS 是 Compare And Swap，比较内存中的旧值是否等于期望值，如果相等则更新为新值。",
                    "它是乐观锁思想，失败后通常自旋重试。",
                ],
            ),
            (
                "优点与问题",
                [
                    "优点：避免阻塞和线程挂起，低竞争下性能好。",
                    "ABA 问题：值从 A 变 B 又变 A，CAS 误以为没有变化，可用版本号或 `AtomicStampedReference` 解决。",
                    "自旋成本：高竞争下大量失败重试会浪费 CPU。",
                    "只能保证单个变量原子更新，复杂条件需要锁或更高层同步机制。",
                ],
            ),
            (
                "应用",
                [
                    "`AtomicInteger`、AQS 状态更新、ConcurrentHashMap 部分更新路径都会使用 CAS。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["volatile"],
        [
            (
                "核心语义",
                [
                    "可见性：一个线程修改 volatile 变量后，其他线程能及时看到。",
                    "有序性：volatile 读写会插入内存屏障，限制指令重排序。",
                    "不保证复合操作原子性，例如 `i++` 仍不是线程安全。",
                ],
            ),
            (
                "适用场景",
                [
                    "状态标记，例如线程停止标志。",
                    "双重检查锁中的单例引用，防止对象未初始化完成就被其他线程看到。",
                    "一写多读且写入不依赖旧值的场景。",
                ],
            ),
            (
                "面试重点",
                [
                    "volatile 解决可见性和有序性，不解决互斥。需要互斥修改共享状态时应使用 synchronized、Lock 或原子类。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["synchronized"],
        [
            (
                "核心语义",
                [
                    "`synchronized` 提供互斥、可见性和有序性。进入同步块需要获取对象监视器，退出同步块会释放锁。",
                    "修饰实例方法锁的是当前对象，修饰静态方法锁的是 Class 对象。",
                ],
            ),
            (
                "锁优化",
                [
                    "JVM 曾有偏向锁、轻量级锁、重量级锁等优化路径；新版本中偏向锁已被废弃或移除。",
                    "锁升级和锁消除、锁粗化等优化都由 JVM 根据运行情况处理。",
                ],
            ),
            (
                "实践建议",
                [
                    "锁粒度应尽量小，锁内避免 IO、RPC、数据库访问等慢操作。",
                    "多把锁同时使用时要固定加锁顺序，降低死锁风险。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["threadlocal"],
        [
            (
                "核心概念",
                [
                    "ThreadLocal 为每个线程保存一份独立变量副本，常用于线程上下文、traceId、用户信息、日期格式化对象等。",
                    "数据实际存放在线程对象的 ThreadLocalMap 中，key 是 ThreadLocal 的弱引用，value 是业务对象。",
                ],
            ),
            (
                "内存泄漏风险",
                [
                    "线程池中的线程会被复用，如果任务结束后不 remove，value 可能长期挂在线程上。",
                    "最佳实践是在 `finally` 中调用 `remove()`。",
                ],
            ),
            (
                "面试重点",
                [
                    "ThreadLocal 不是为了解决共享变量竞争，而是用线程隔离避免共享。在线程池、异步任务和父子线程传递场景要特别谨慎。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["aqs"],
        [
            (
                "核心概念",
                [
                    "AQS 是 AbstractQueuedSynchronizer，是构建锁和同步器的基础框架。",
                    "它用一个 volatile int `state` 表示同步状态，用 CLH 变体队列管理等待线程。",
                ],
            ),
            (
                "两种模式",
                [
                    "独占模式：同一时刻只允许一个线程获取，例如 ReentrantLock。",
                    "共享模式：允许多个线程同时获取，例如 Semaphore、CountDownLatch。",
                ],
            ),
            (
                "面试重点",
                [
                    "理解 AQS 要抓住 state、CAS 更新、等待队列、park/unpark、独占/共享模式这几个关键词。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["线程池"],
        [
            (
                "核心参数",
                [
                    "`corePoolSize`：核心线程数。",
                    "`maximumPoolSize`：最大线程数。",
                    "`workQueue`：任务队列。",
                    "`keepAliveTime`：非核心线程空闲存活时间。",
                    "`RejectedExecutionHandler`：拒绝策略。",
                ],
            ),
            (
                "执行流程",
                [
                    "线程数小于 core 时创建核心线程。",
                    "核心线程满后任务进入队列。",
                    "队列满后创建非核心线程，直到 maximum。",
                    "线程和队列都满时触发拒绝策略。",
                ],
            ),
            (
                "实践建议",
                [
                    "CPU 密集型任务线程数接近 CPU 核数。",
                    "IO 密集型任务可适当增大线程数，但要受下游容量约束。",
                    "不要使用无界队列承接不可控流量，否则可能导致内存膨胀和延迟失控。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["completablefuture", "future"],
        [
            (
                "核心区别",
                [
                    "Future 只能表示异步结果，组合能力弱，获取结果通常阻塞。",
                    "CompletableFuture 支持回调、编排、组合、异常处理，适合多个异步任务聚合。",
                ],
            ),
            (
                "实践建议",
                [
                    "显式传入业务线程池，避免默认 ForkJoinPool 被阻塞任务耗尽。",
                    "每个异步分支都要处理异常和超时。",
                    "聚合多个外部调用时要考虑降级和部分失败。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["simpledateformat"],
        [
            (
                "核心问题",
                [
                    "SimpleDateFormat 不是线程安全的，多线程共享同一个实例可能导致解析或格式化结果错误。",
                ],
            ),
            (
                "解决方案",
                [
                    "每次使用创建新实例，简单但有对象创建成本。",
                    "使用 ThreadLocal 保存每个线程独立实例，但线程池中要注意 remove。",
                    "优先使用 Java 8+ 的 `DateTimeFormatter`，它是不可变且线程安全的。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["java和c", "java和c的区别"],
        [
            (
                "核心区别",
                [
                    "Java 运行在 JVM 上，强调跨平台、自动内存管理和安全边界；C/C++ 更接近底层，允许直接操作内存，性能和控制力更强但风险也更高。",
                    "Java 不支持多继承类，但支持接口多继承；C++ 支持类多继承，因此也需要处理菱形继承等复杂问题。",
                    "Java 没有运算符重载和显式指针运算，降低了语言复杂度和内存错误概率。",
                ],
            ),
            (
                "面试表达",
                [
                    "回答时不要只背语法差异，可以从内存管理、运行时平台、继承模型、异常机制、泛型实现和生态定位几个角度比较。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["位移运算符"],
        [
            (
                "三类位移",
                [
                    "`<<`：左移，低位补 0，相当于在不溢出的情况下乘以 2 的幂。",
                    "`>>`：有符号右移，高位补符号位。",
                    "`>>>`：无符号右移，高位补 0。",
                ],
            ),
            (
                "注意点",
                [
                    "int 位移只取低 5 位，因此移动 32 位等价于移动 0 位；long 位移只取低 6 位。",
                    "位运算常用于状态标记、权限位、哈希扰动、网络协议和高性能编码。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["构造方法"],
        [
            (
                "核心规则",
                [
                    "构造方法名称与类名相同，没有返回值。",
                    "如果没有显式定义构造方法，编译器会生成默认无参构造。",
                    "一旦定义了任意构造方法，编译器不再自动生成无参构造。",
                    "子类构造方法默认先调用父类无参构造，也可以通过 `super(...)` 指定父类构造。",
                ],
            ),
            (
                "工程实践",
                [
                    "框架反射创建对象通常需要无参构造，例如部分 ORM、序列化工具。",
                    "构造器中不要启动线程或暴露 `this`，避免对象未完成初始化就被外部访问。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["常量"],
        [
            (
                "常量类型",
                [
                    '字面量常量：例如 `1`、`"abc"`。',
                    "`static final` 常量：属于类，常用于全局固定配置或枚举前的常量定义。",
                    "成员常量：定义在类中、方法外，使用 `final` 修饰，属于对象实例，每个对象都有自己的字段值且只能赋值一次。",
                    "局部 final 变量：方法内部只能赋值一次。",
                ],
            ),
            (
                "静态常量（类中）",
                [
                    "定义位置：类中、方法外。",
                    "修饰方式：通常使用 `public static final` 或 `private static final`。",
                    "归属：属于类本身，不依赖对象实例。",
                    "使用场景：全局固定配置、错误码、默认值、常量 key。",
                ],
            ),
            (
                "成员常量（类中）",
                [
                    "定义位置：类中、方法外。",
                    "修饰方式：使用 `final`，但不使用 `static`。",
                    "归属：属于对象实例。不同对象可以在构造时初始化为不同值，但初始化后不能再修改。",
                    "使用场景：对象创建后不应改变的实例属性，例如创建时间、业务编号、初始化配置。",
                ],
            ),
            (
                "局部常量（类方法中）",
                [
                    "定义位置：方法、构造器或代码块内部。",
                    "修饰方式：使用 `final` 修饰局部变量。",
                    "作用域：只在当前方法或代码块内有效。",
                    "使用场景：方法内部不希望被重新赋值的临时变量、Lambda 捕获变量。",
                ],
            ),
            (
                "编译期常量",
                [
                    "基本类型和 String 的 `static final` 常量如果在编译期可确定，可能会被编译器内联到使用方。",
                    "公共常量变更后，如果使用方未重新编译，可能仍然使用旧值。",
                ],
            ),
            (
                "示例代码",
                [
                    {
                        "lang": "java",
                        "code": """public class ConstantDemo {
    // 静态常量：类中，属于类本身，所有对象共享
    public static final String SYSTEM_NAME = \"order-service\";

    // 成员常量：类中，属于对象实例，每个对象初始化后不可变
    private final String orderNo;

    public ConstantDemo(String orderNo) {
        this.orderNo = orderNo;
    }

    public void printOrder() {
        // 局部常量：方法中，只在当前方法内有效，赋值后不能再改
        final int maxRetryTimes = 3;

        System.out.println(\"system=\" + SYSTEM_NAME);
        System.out.println(\"orderNo=\" + orderNo);
        System.out.println(\"maxRetryTimes=\" + maxRetryTimes);
    }

    public static void main(String[] args) {
        ConstantDemo demo = new ConstantDemo(\"ORDER_1001\");
        demo.printOrder();
    }
}""",
                    }
                ],
            ),
        ],
    ),
    (
        "Java",
        ["object常见方法"],
        [
            (
                "getClass()",
                [
                    "签名：`public final native Class<?> getClass()`。",
                    "作用：返回对象运行时的 `Class` 对象，用于获取类元信息。",
                    "特点：`final` 方法，子类不能重写；返回的是运行时实际类型，不是声明类型。",
                    "常见场景：反射、日志打印、框架类型判断、注解解析。",
                ],
            ),
            (
                "hashCode()",
                [
                    "签名：`public native int hashCode()`。",
                    "作用：返回对象的哈希码，主要服务于 `HashMap`、`HashSet`、`Hashtable` 等哈希容器。",
                    "默认实现通常与对象地址相关，但规范不要求必须等于内存地址。",
                    "注意：如果重写 `equals`，通常必须同时重写 `hashCode`，保证相等对象哈希值相同。",
                ],
            ),
            (
                "equals(Object obj)",
                [
                    "签名：`public boolean equals(Object obj)`。",
                    "作用：判断两个对象是否相等。Object 默认实现等价于 `this == obj`，即比较引用是否相同。",
                    "常见重写场景：值对象、DTO、业务唯一对象等需要按字段或业务主键判断相等。",
                    "注意：需要满足自反性、对称性、传递性、一致性和非空性。",
                ],
            ),
            (
                "clone()",
                [
                    "签名：`protected native Object clone() throws CloneNotSupportedException`。",
                    "作用：创建并返回当前对象的一个副本。",
                    "使用条件：类通常需要实现 `Cloneable` 接口，否则调用 `Object#clone` 会抛出 `CloneNotSupportedException`。",
                    "注意：默认是浅拷贝，引用字段仍指向原对象中的引用对象；深拷贝需要手动处理。",
                    "实践建议：业务代码更推荐拷贝构造器、静态工厂或映射工具，少直接依赖 `clone`。",
                ],
            ),
            (
                "toString()",
                [
                    "签名：`public String toString()`。",
                    "作用：返回对象的字符串表示。Object 默认格式通常是 `类名@哈希值十六进制`。",
                    "常见重写场景：日志、调试、错误定位、对象摘要展示。",
                    "注意：不要在 `toString` 中输出密码、token、身份证等敏感信息，也不要触发复杂远程调用或懒加载风暴。",
                ],
            ),
            (
                "notify()",
                [
                    "签名：`public final native void notify()`。",
                    "作用：随机唤醒一个正在该对象监视器上等待的线程。",
                    "使用条件：必须在持有该对象监视器时调用，即在 `synchronized(obj)` 或同步方法中调用。",
                    "注意：被唤醒线程不会立刻执行，需要重新竞争锁。",
                ],
            ),
            (
                "notifyAll()",
                [
                    "签名：`public final native void notifyAll()`。",
                    "作用：唤醒所有正在该对象监视器上等待的线程。",
                    "使用条件：同样必须在持有对象监视器时调用。",
                    "实践建议：条件复杂或多个线程等待不同条件时，`notifyAll` 通常比 `notify` 更安全，但会带来更多线程竞争。",
                ],
            ),
            (
                "wait(long timeout)",
                [
                    "签名：`public final native void wait(long timeout) throws InterruptedException`。",
                    "作用：让当前线程释放对象锁并进入等待，直到被唤醒、超时或中断。",
                    "使用条件：必须在持有对象监视器时调用。",
                    "注意：`timeout` 为 0 表示无限等待。",
                ],
            ),
            (
                "wait(long timeout, int nanos)",
                [
                    "签名：`public final void wait(long timeout, int nanos) throws InterruptedException`。",
                    "作用：在毫秒基础上增加纳秒级等待参数。",
                    "注意：实际唤醒精度受操作系统调度影响，不应依赖它实现严格纳秒级定时。",
                ],
            ),
            (
                "wait()",
                [
                    "签名：`public final void wait() throws InterruptedException`。",
                    "作用：无限期等待，直到其他线程调用同一对象的 `notify/notifyAll` 或当前线程被中断。",
                    "实践建议：调用 `wait` 应放在 while 条件循环中，防止虚假唤醒。",
                ],
            ),
            (
                "finalize()",
                [
                    "签名：`protected void finalize() throws Throwable`。",
                    "作用：对象被垃圾回收前可能被 JVM 调用，用于资源清理。",
                    "现状：`finalize` 已被废弃，不推荐使用，后续版本中会被移除。",
                    "原因：执行时机不确定、性能差、容易导致对象复活和资源泄漏。",
                    "替代方案：使用 `try-with-resources`、`AutoCloseable`、显式 `close`、Cleaner 或框架生命周期回调。",
                ],
            ),
            (
                "wait/notify 使用示例",
                [
                    {
                        "lang": "java",
                        "code": """public class WaitNotifyDemo {
    private final Object lock = new Object();
    private boolean ready = false;

    public void waitReady() throws InterruptedException {
        synchronized (lock) {
            while (!ready) { // 防止虚假唤醒
                lock.wait();
            }
            System.out.println(\"ready\");
        }
    }

    public void makeReady() {
        synchronized (lock) {
            ready = true;
            lock.notifyAll();
        }
    }
}""",
                    }
                ],
            ),
        ],
    ),
    (
        "Java",
        ["统计代码耗时"],
        [
            (
                "常用方式",
                [
                    "简单场景可用 `System.nanoTime()` 统计相对耗时，避免用 `currentTimeMillis()` 做精细耗时统计。",
                    "Spring 项目可使用 `StopWatch` 记录多阶段耗时。",
                    "线上接口耗时应接入 Micrometer、Prometheus、SkyWalking、OpenTelemetry 等监控体系。",
                ],
            ),
            (
                "实践建议",
                [
                    "性能测试要预热 JVM，避免 JIT、类加载、缓存冷启动影响结论。",
                    "微基准测试优先使用 JMH。",
                ],
            ),
            (
                "StopWatch 示例代码",
                [
                    {
                        "lang": "java",
                        "code": """import org.springframework.util.StopWatch;

public class StopWatchDemo {
    public static void main(String[] args) throws InterruptedException {
        StopWatch stopWatch = new StopWatch(\"order-service-cost\");

        stopWatch.start(\"query-user\");
        Thread.sleep(80);
        stopWatch.stop();

        stopWatch.start(\"query-order\");
        Thread.sleep(120);
        stopWatch.stop();

        stopWatch.start(\"build-response\");
        Thread.sleep(30);
        stopWatch.stop();

        System.out.println(stopWatch.prettyPrint());
        System.out.println(\"totalMillis=\" + stopWatch.getTotalTimeMillis());
    }
}""",
                    }
                ],
            ),
        ],
    ),
    (
        "Java",
        ["s1-1", "s1-", "s1"],
        [
            (
                "类型转换",
                [
                    "`s1 += 1` 隐含强制类型转换，等价于 `s1 = (short)(s1 + 1)`。",
                    "`s1 = s1 + 1` 中 `s1 + 1` 会先提升为 int，因此直接赋值给 short 会编译失败。",
                ],
            ),
            (
                "面试重点",
                [
                    "byte、short、char 参与算术运算时通常会提升为 int，这是 Java 数值提升规则的体现。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["跳出多层循环"],
        [
            (
                "常见方式",
                [
                    "使用带标签的 `break label` 跳出指定外层循环。",
                    "将循环逻辑抽成方法，通过 `return` 提前结束。",
                    "使用状态变量控制外层循环，但可读性通常较差。",
                ],
            ),
            (
                "实践建议",
                [
                    "业务代码中不要滥用 label，复杂循环更建议拆函数提升可读性。",
                ],
            ),
            (
                "示例代码",
                [
                    {
                        "lang": "java",
                        "code": """public class BreakOuterLoopDemo {
    public static void main(String[] args) {
        outer:
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                System.out.println(\"i=\" + i + \", j=\" + j);

                if (i == 1 && j == 1) {
                    break outer; // 跳出 outer 标记的外层循环
                }
            }
        }

        System.out.println(\"end\");
    }
}""",
                    }
                ],
            ),
        ],
    ),
    (
        "Java",
        ["main方法"],
        [
            (
                "基本规则",
                [
                    "标准入口是 `public static void main(String[] args)`。",
                    "`main` 可以重载，但 JVM 启动时只识别标准签名。",
                    "`main` 是静态方法，可以被继承但不存在运行期多态重写意义。",
                ],
            ),
            (
                "实践",
                [
                    "Spring Boot 的 main 方法主要负责调用 `SpringApplication.run` 启动应用上下文。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["可变长参数"],
        [
            (
                "核心规则",
                [
                    "可变长参数本质上是数组，方法内部按数组处理。",
                    "一个方法最多只能有一个可变长参数，并且必须放在参数列表最后。",
                    "重载时同时存在数组、固定参数和可变参数可能造成调用歧义。",
                ],
            ),
            (
                "实践建议",
                [
                    "公共 API 使用可变参数要注意 null、空数组和重载歧义。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["switch支持的数据类型"],
        [
            (
                "支持类型",
                [
                    "传统 switch 支持 byte、short、char、int 及其包装类型、enum、String。",
                    "不支持 long、float、double、boolean。",
                    "新版本 Java 引入 switch expression 和模式匹配能力，表达能力更强。",
                ],
            ),
            (
                "注意点",
                [
                    "String switch 底层会结合 hashCode 和 equals 判断，不能只理解成整数跳转。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["静态内部类和普通内部类区别"],
        [
            (
                "核心区别",
                [
                    "普通内部类持有外部类实例引用，可以访问外部类实例成员。",
                    "静态内部类不持有外部类实例引用，只能直接访问外部类静态成员。",
                    "创建普通内部类需要外部类实例，创建静态内部类不需要。",
                ],
            ),
            (
                "典型应用",
                [
                    "静态内部类常用于 Builder、枚举式分组、静态内部类单例模式。",
                    "非静态内部类如果被长生命周期对象引用，可能导致外部类实例无法释放。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["判断类或接口的派生关系"],
        [
            (
                "常用 API",
                [
                    "`instanceof`：判断对象是否是某类型实例。",
                    "`Class#isAssignableFrom`：判断一个 Class 是否可由另一个 Class 赋值。",
                    "`Class#isInstance`：反射版本的 instanceof。",
                ],
            ),
            (
                "示例理解",
                [
                    "`Parent.class.isAssignableFrom(Child.class)` 为 true，表示 Child 可以赋值给 Parent。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["创建对象方法"],
        [
            (
                "常见方式",
                [
                    "使用 `new` 调用构造方法。",
                    "使用反射 `Constructor#newInstance`。",
                    "使用 clone，但需要实现 `Cloneable` 且语义复杂。",
                    "通过反序列化恢复对象。",
                    "通过工厂方法、Builder、Spring 容器创建对象。",
                ],
            ),
            (
                "实践建议",
                [
                    "业务代码优先使用构造器、静态工厂或 Builder；框架层才大量使用反射和容器创建。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["exact:变量"],
        [
            (
                "变量分类",
                [
                    "局部变量：定义在方法、构造器或代码块中，必须显式初始化后才能使用。",
                    "成员变量：定义在类中、方法外，属于对象实例，有默认值。",
                    "静态变量：使用 `static` 修饰，属于类本身，所有实例共享。",
                ],
            ),
            (
                "作用域与生命周期",
                [
                    "局部变量随方法调用入栈创建，方法结束后失效。",
                    "成员变量随对象创建而存在，对象被 GC 后释放。",
                    "静态变量随类加载初始化，通常随 Class 卸载才释放。",
                ],
            ),
            (
                "示例代码",
                [
                    {
                        "lang": "java",
                        "code": """public class VariableDemo {
    private static int staticCount = 0; // 静态变量：类共享
    private String name;               // 成员变量：对象独有

    public void setName(String name) { // 参数也是局部变量
        int length = name.length();    // 局部变量：方法内有效
        this.name = name;
        staticCount++;
        System.out.println(length);
    }
}""",
                    }
                ],
            ),
        ],
    ),
    (
        "Java",
        ["重写和重载"],
        [
            (
                "重载 Overload",
                [
                    "发生在同一个类中，方法名相同，参数列表不同。",
                    "参数列表不同包括参数个数、类型或顺序不同。",
                    "仅返回值不同不能构成重载。",
                    "重载是编译期确定，属于静态分派。",
                ],
            ),
            (
                "重写 Override",
                [
                    "发生在父子类之间，子类重新实现父类可继承的方法。",
                    "方法名、参数列表需要相同，返回值类型可以是协变返回。",
                    "访问权限不能比父类更严格，抛出的受检异常不能比父类更宽。",
                    "重写是运行期根据实际对象类型确定，属于动态分派。",
                ],
            ),
            (
                "示例代码",
                [
                    {
                        "lang": "java",
                        "code": """class Animal {
    void speak() {
        System.out.println(\"animal\");
    }
}

class Dog extends Animal {
    @Override
    void speak() { // 重写
        System.out.println(\"dog\");
    }

    void speak(String prefix) { // 重载
        System.out.println(prefix + \" dog\");
    }
}""",
                    }
                ],
            ),
        ],
    ),
    (
        "Java",
        ["erro和exception", "error和exception"],
        [
            (
                "Throwable 体系",
                [
                    "`Throwable` 是 Java 异常体系根类，下面主要分为 `Error` 和 `Exception`。",
                    "`Error` 表示严重错误，通常程序无法恢复，例如 `OutOfMemoryError`、`StackOverflowError`。",
                    "`Exception` 表示程序可以捕获和处理的异常。",
                ],
            ),
            (
                "受检与非受检异常",
                [
                    "受检异常：继承 `Exception` 但不继承 `RuntimeException`，编译器要求处理或声明抛出。",
                    "非受检异常：`RuntimeException` 及其子类，通常表示编程错误或运行期异常。",
                    "业务异常通常可以设计为 RuntimeException，但要有统一异常处理和错误码。",
                ],
            ),
            (
                "实践建议",
                [
                    "不要捕获 `Throwable` 或 `Error` 后继续正常执行，除非是在框架边界做日志和隔离。",
                    "不要空 catch，至少记录上下文。",
                    "对外接口应统一异常响应，避免把内部堆栈直接暴露给调用方。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["包装类"],
        [
            (
                "核心概念",
                [
                    "包装类是基本类型的对象形式，例如 `int` 对应 `Integer`，`long` 对应 `Long`。",
                    "包装类可用于泛型、集合、反射、空值表达等基本类型不能直接使用的场景。",
                ],
            ),
            (
                "缓存机制",
                [
                    "`Integer` 默认缓存 `-128` 到 `127` 范围内的对象。",
                    "`Byte`、`Short`、`Long`、`Character` 也有类似缓存范围。",
                    "不要依赖 `==` 比较包装类数值，应使用 `equals` 或转成基本类型。",
                ],
            ),
            (
                "拆箱 NPE",
                [
                    "包装类型为 null 时自动拆箱会抛出 `NullPointerException`。",
                    "数据库字段、JSON 入参、RPC DTO 中的包装类型要特别注意 null。",
                ],
            ),
            (
                "示例代码",
                [
                    {
                        "lang": "java",
                        "code": """Integer a = 127;
Integer b = 127;
System.out.println(a == b); // true，命中缓存

Integer c = 128;
Integer d = 128;
System.out.println(c == d); // false，通常未命中缓存

Integer value = null;
// int n = value; // 自动拆箱会抛 NullPointerException""",
                    }
                ],
            ),
        ],
    ),
    (
        "Java",
        ["exact:字符串"],
        [
            (
                "不可变性",
                [
                    "`String` 是不可变类，内部字符内容创建后不能修改。",
                    "不可变性带来线程安全、可缓存 hashCode、适合作为 Map key 等优势。",
                    "字符串拼接会产生新字符串或由编译器/JVM 优化成其他形式。",
                ],
            ),
            (
                "字符串常量池",
                [
                    "字符串字面量会进入字符串常量池。",
                    '`new String("abc")` 会创建堆对象，字面量 `"abc"` 仍在常量池。',
                    "`intern()` 会尝试返回常量池中的字符串引用。",
                ],
            ),
            (
                "String/StringBuilder/StringBuffer",
                [
                    "`String`：不可变，适合少量字符串和常量。",
                    "`StringBuilder`：可变，非线程安全，适合单线程大量拼接。",
                    "`StringBuffer`：可变，方法加 synchronized，线程安全但性能开销更高。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["接口和抽象类区别"],
        [
            (
                "核心区别",
                [
                    "抽象类表达 is-a 关系，适合沉淀公共状态和公共实现。",
                    "接口表达 can-do 能力，适合定义行为契约和扩展点。",
                    "Java 类只能继承一个父类，但可以实现多个接口。",
                ],
            ),
            (
                "成员能力",
                [
                    "抽象类可以有成员变量、构造器、普通方法、抽象方法。",
                    "接口可以有抽象方法、默认方法、静态方法、私有方法，字段默认是 `public static final`。",
                ],
            ),
            (
                "选择建议",
                [
                    "需要共享状态或模板方法时用抽象类。",
                    "需要定义能力、插件扩展、跨层契约时用接口。",
                    "面向框架设计时，接口通常更利于解耦和测试。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["exact:泛型"],
        [
            (
                "核心概念",
                [
                    "泛型用于把类型参数化，让编译器在编译期做类型检查。",
                    "Java 泛型通过类型擦除实现，运行期大部分泛型信息不可见。",
                ],
            ),
            (
                "通配符",
                [
                    "`? extends T`：上界通配符，适合读取，表示 T 或 T 的子类。",
                    "`? super T`：下界通配符，适合写入，表示 T 或 T 的父类。",
                    "口诀 PECS：Producer Extends，Consumer Super。",
                ],
            ),
            (
                "常见限制",
                [
                    "不能直接 `new T()`。",
                    "不能创建泛型数组，例如 `new List<String>[10]`。",
                    "运行期不能直接用 `instanceof List<String>` 判断具体泛型参数。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["jdk8提供的内置的函数式接口"],
        [
            (
                "常见函数式接口",
                [
                    "`Function<T,R>`：接收 T，返回 R。",
                    "`Consumer<T>`：接收 T，无返回值。",
                    "`Supplier<T>`：无入参，返回 T。",
                    "`Predicate<T>`：接收 T，返回 boolean。",
                    "`UnaryOperator<T>`：接收 T，返回 T。",
                    "`BinaryOperator<T>`：接收两个 T，返回 T。",
                ],
            ),
            (
                "示例代码",
                [
                    {
                        "lang": "java",
                        "code": """Function<String, Integer> length = String::length;
Predicate<String> notBlank = s -> s != null && !s.isBlank();
Consumer<String> printer = System.out::println;
Supplier<Long> now = System::currentTimeMillis;

if (notBlank.test("java")) {
    printer.accept("len=" + length.apply("java"));
}""",
                    }
                ],
            ),
        ],
    ),
    (
        "Java",
        ["exact:stream"],
        [
            (
                "核心概念",
                [
                    "Stream 是 Java 8 引入的声明式数据处理 API，用于对集合、数组、IO 等数据源进行流水线处理。",
                    "Stream 不存储数据，通常由数据源创建，经中间操作转换，最后由终止操作触发执行。",
                ],
            ),
            (
                "操作类型",
                [
                    "中间操作：`map`、`filter`、`flatMap`、`sorted`、`distinct`、`peek`。",
                    "终止操作：`collect`、`forEach`、`reduce`、`count`、`findFirst`、`anyMatch`。",
                    "中间操作通常是惰性的，只有遇到终止操作才执行。",
                ],
            ),
            (
                "实践注意",
                [
                    "Stream 只能消费一次。",
                    "避免在 Stream 中写复杂副作用逻辑。",
                    "parallelStream 不一定更快，可能带来线程池竞争、顺序问题和上下文丢失。",
                ],
            ),
            (
                "示例代码",
                [
                    {
                        "lang": "java",
                        "code": """List<String> names = users.stream()
    .filter(user -> user.getAge() >= 18)
    .map(User::getName)
    .distinct()
    .sorted()
    .toList();""",
                    }
                ],
            ),
        ],
    ),
    (
        "Java",
        ["exact:unsafe"],
        [
            (
                "核心概念",
                [
                    "`Unsafe` 是 JDK 内部提供的底层能力类，可以直接操作内存、对象字段、CAS、线程挂起恢复等。",
                    "它绕过了 Java 的部分安全检查，因此名字叫 Unsafe。",
                ],
            ),
            (
                "常见能力",
                [
                    "堆外内存分配和释放。",
                    "CAS 原子操作。",
                    "按字段偏移量读写对象字段。",
                    "线程 park/unpark。",
                    "绕过构造器创建对象。",
                ],
            ),
            (
                "实践建议",
                [
                    "业务代码不应直接使用 Unsafe。",
                    "并发工具、Netty、序列化框架等底层组件可能间接使用它。",
                    "现代 Java 更推荐使用 VarHandle、ByteBuffer、Foreign Function & Memory API 等替代方向。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["深拷贝浅拷贝"],
        [
            (
                "核心区别",
                [
                    "浅拷贝只复制对象本身，引用字段仍指向原来的对象。",
                    "深拷贝会递归复制引用对象，新旧对象之间不共享可变内部状态。",
                ],
            ),
            (
                "实现方式",
                [
                    "手写拷贝构造或转换方法，最清晰可控。",
                    "序列化再反序列化可实现深拷贝，但性能和兼容性一般。",
                    "使用 MapStruct、BeanUtils 等工具时要明确它们默认多为浅层复制。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["yyyy与yyyy", "日期格式"],
        [
            (
                "核心区别",
                [
                    "`yyyy` 表示自然年 year-of-era。",
                    "`YYYY` 表示 week-based-year，即周所属的年份。",
                    "跨年周附近使用 `YYYY` 可能把日期格式化到相邻年份，导致线上日期分区或报表错误。",
                ],
            ),
            (
                "实践建议",
                [
                    "业务日期格式化通常使用 `yyyy-MM-dd`，不要误用 `YYYY-MM-dd`。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["repeatable"],
        [
            (
                "核心概念",
                [
                    "`@Repeatable` 允许同一个注解在同一元素上重复使用。",
                    "需要定义一个容器注解来承载多个重复注解。",
                ],
            ),
            (
                "典型场景",
                [
                    "同一方法配置多条规则、多个权限、多个路由或多个校验条件。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["spi"],
        [
            (
                "核心概念",
                [
                    "SPI 是 Service Provider Interface，用于面向接口发现实现类。",
                    "JDK SPI 通过 `META-INF/services/接口全限定名` 配置实现类，再用 `ServiceLoader` 加载。",
                ],
            ),
            (
                "应用场景",
                [
                    "JDBC Driver、日志框架、Dubbo 扩展点、序列化插件等都体现了 SPI 思想。",
                ],
            ),
            (
                "注意点",
                [
                    "JDK SPI 会一次性加载并实例化实现类，按需加载和扩展能力相对较弱；Dubbo SPI 做了更丰富的增强。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["进程间通信"],
        [
            (
                "常见方式",
                [
                    "管道、消息队列、共享内存、信号量、Socket、文件、RPC、HTTP、消息中间件。",
                    "后端分布式系统中更常见的是 HTTP/RPC、消息队列、数据库和缓存作为进程间协作方式。",
                ],
            ),
            (
                "面试重点",
                [
                    "线程间通信共享同一进程内存，进程间通信需要借助操作系统或网络机制。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["守护线程"],
        [
            (
                "核心概念",
                [
                    "守护线程是为用户线程服务的后台线程。",
                    "当 JVM 中只剩守护线程时，JVM 会退出。",
                    "典型守护线程包括 GC 相关线程、监控或后台清理线程。",
                ],
            ),
            (
                "注意点",
                [
                    "守护线程不适合承载必须完成的数据写入、文件关闭、事务提交等关键任务。",
                    "必须在线程启动前调用 `setDaemon(true)`。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["线程顺序执行的方法"],
        [
            (
                "常见方式",
                [
                    "使用 `Thread#join` 等待前一个线程结束。",
                    "使用 `CountDownLatch` 控制阶段顺序。",
                    "使用单线程线程池保证任务按提交顺序执行。",
                    "使用 `CompletableFuture` 编排依赖关系。",
                ],
            ),
            (
                "实践建议",
                [
                    "如果只是任务编排，优先使用线程池和 Future/CompletableFuture，而不是手动创建多个 Thread。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["线程异常处理"],
        [
            (
                "处理方式",
                [
                    "线程内部 try-catch，最直接可靠。",
                    "设置 `UncaughtExceptionHandler` 捕获未处理异常。",
                    "线程池中通过 `Future#get` 获取任务异常。",
                    "重写 `ThreadPoolExecutor#afterExecute` 做统一记录。",
                ],
            ),
            (
                "实践建议",
                [
                    "线程池任务异常必须记录日志和指标，否则任务失败可能被静默吞掉。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["线程终止"],
        [
            (
                "推荐方式",
                [
                    "使用共享停止标志，例如 volatile boolean。",
                    "使用 `interrupt` 中断阻塞或协作式停止。",
                    "线程池使用 `shutdown` 或 `shutdownNow`，并配合超时等待。",
                ],
            ),
            (
                "不推荐方式",
                [
                    "不要使用 `Thread.stop`，它会强制释放锁，可能破坏对象一致性。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["线程异步"],
        [
            (
                "常见方式",
                [
                    "线程池提交任务。",
                    "Future/CompletableFuture。",
                    "Spring `@Async`。",
                    "消息队列异步解耦。",
                ],
            ),
            (
                "实践建议",
                [
                    "异步任务必须考虑线程池隔离、异常处理、超时、重试、幂等和上下文传递。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["sleep和wait"],
        [
            (
                "核心区别",
                [
                    "`sleep` 是 Thread 的静态方法，不释放对象锁。",
                    "`wait` 是 Object 方法，必须在 synchronized 中调用，调用后会释放对象锁并进入等待队列。",
                    "`wait` 需要通过 `notify/notifyAll` 或超时唤醒，唤醒后还要重新竞争锁。",
                ],
            ),
            (
                "实践建议",
                [
                    "生产代码中更推荐使用 `CountDownLatch`、`Condition`、BlockingQueue 等更高层并发工具。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["reentrantlock"],
        [
            (
                "核心能力",
                [
                    "ReentrantLock 是可重入独占锁，基于 AQS 实现。",
                    "支持公平锁/非公平锁、可中断加锁、超时加锁和多个 Condition 队列。",
                ],
            ),
            (
                "与 synchronized",
                [
                    "synchronized 语法简单，由 JVM 管理释放。",
                    "ReentrantLock 功能更丰富，但必须在 finally 中手动 unlock。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["reentrantreadwritelock"],
        [
            (
                "核心概念",
                [
                    "读写锁将读和写分离，允许多个读线程并发，写线程独占。",
                    "适合读多写少且读操作耗时明显的场景。",
                ],
            ),
            (
                "注意点",
                [
                    "写锁可以降级为读锁，读锁不能直接升级为写锁，否则可能死锁。",
                    "如果写操作频繁，读写锁收益可能不明显，甚至更复杂。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["线程同步"],
        [
            (
                "同步手段",
                [
                    "内置锁：synchronized。",
                    "显式锁：ReentrantLock、ReadWriteLock、StampedLock。",
                    "原子类：AtomicInteger、AtomicReference。",
                    "同步器：CountDownLatch、CyclicBarrier、Semaphore。",
                    "阻塞队列：BlockingQueue。",
                ],
            ),
            (
                "选择建议",
                [
                    "简单互斥优先 synchronized；需要超时、中断、公平性或多个条件队列时考虑 Lock；计数和状态流转考虑 AQS 同步器。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["runnable和callable"],
        [
            (
                "核心区别",
                [
                    "Runnable 的 `run` 没有返回值，不能直接抛出受检异常。",
                    "Callable 的 `call` 有返回值，可以抛出异常，通常配合 Future 使用。",
                ],
            ),
            (
                "实践",
                [
                    "需要异步结果或异常传递时使用 Callable/Future/CompletableFuture。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["execute和submit"],
        [
            (
                "核心区别",
                [
                    "`execute` 提交 Runnable，没有返回 Future，异常通常由线程的异常处理器处理。",
                    "`submit` 返回 Future，任务异常会封装在 Future 中，调用 `get` 时抛出。",
                ],
            ),
            (
                "实践建议",
                [
                    "如果使用 submit 但从不调用 Future#get，异常可能不明显，需要统一 afterExecute 或日志处理。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["shutdown和shutdwonnow", "shutdown和shutdownnow"],
        [
            (
                "核心区别",
                [
                    "`shutdown`：停止接收新任务，已提交任务继续执行。",
                    "`shutdownNow`：尝试中断正在执行的任务，并返回队列中尚未执行的任务。",
                ],
            ),
            (
                "实践建议",
                [
                    "优雅停机通常先 shutdown，再 awaitTermination，超时后再 shutdownNow。任务本身也要响应中断。",
                ],
            ),
        ],
    ),
    (
        "Java",
        ["isterminated和isshutdown"],
        [
            (
                "核心区别",
                [
                    "`isShutdown` 表示线程池已经开始关闭，不再接收新任务。",
                    "`isTerminated` 表示线程池关闭流程完成，所有任务都已结束。",
                ],
            ),
            (
                "实践",
                [
                    "判断线程池是否完全退出应使用 `awaitTermination` 或 `isTerminated`，不能只看 `isShutdown`。",
                ],
            ),
        ],
    ),
]


BIGDATA_DOCS = [
    (
        "大数据求职路线",
        "11-bigdata/README.md",
        """# 大数据方向知识库

本目录补充后端找工作常见的大数据能力栈，重点覆盖离线存储、批处理、实时计算、OLAP 分析、数仓建模和数据链路治理。

## 适合岗位

- Java 后端开发：掌握 HDFS、Hive、Kafka、Flink、ClickHouse 的基本原理和工程使用即可明显加分。
- 数据平台后端：需要理解任务调度、元数据、血缘、数据质量、权限、资源队列和多租户治理。
- 大数据开发：需要深入 Spark/Flink/Hive SQL 优化、数仓建模、实时链路和存储选型。
- 推荐/广告/搜索/风控后端：重点关注日志采集、用户行为流、实时特征、离线画像和 OLAP 查询。

## 学习优先级

1. HDFS、YARN、MapReduce：理解 Hadoop 基础设施。
2. Hive：掌握离线数仓 SQL、分区分桶、小文件治理和 SQL 优化。
3. Kafka + Flink：掌握实时数据流、状态、Checkpoint、Exactly Once。
4. Spark：掌握批处理、Shuffle、内存模型和 Spark SQL 优化。
5. HBase、ClickHouse：理解宽表 KV 和 OLAP 列式分析场景。
6. 数仓建模、CDC、湖仓：能讲清 ODS/DWD/DWS/ADS、维度建模和数据同步链路。

## 面试表达模板

- 这个组件解决什么问题？
- 架构里有哪些核心角色？
- 写入和读取链路是什么？
- 如何保证可靠性和一致性？
- 常见性能瓶颈是什么？
- 线上如何排障和优化？
- 在项目中如何落地？

## 目录

- [Hadoop 总览](hadoop/README.md)
- [HDFS](hadoop/hdfs.md)
- [YARN](hadoop/yarn.md)
- [MapReduce](hadoop/mapreduce.md)
- [Hive](hive/README.md)
- [Hive SQL 优化](hive/sql-optimization.md)
- [Spark](spark/README.md)
- [Spark Shuffle](spark/shuffle.md)
- [Flink](flink/README.md)
- [Flink Checkpoint](flink/checkpoint.md)
- [Flink Exactly Once](flink/exactly-once.md)
- [HBase](hbase/README.md)
- [HBase RowKey 设计](hbase/rowkey-design.md)
- [ClickHouse](clickhouse/README.md)
- [MergeTree](clickhouse/mergetree.md)
- [数仓建模](data-warehouse/README.md)
- [ODS/DWD/DWS/ADS](data-warehouse/ods-dwd-dws-ads.md)
- [数据链路与湖仓](data-pipeline/README.md)
- [实时数仓](data-warehouse/realtime-warehouse.md)
- [Apache Doris](olap/doris.md)
- [Trino/Presto](olap/trino.md)
- [Apache Iceberg](lakehouse/iceberg.md)
- [Apache Hudi](lakehouse/hudi.md)
- [Flink CDC](data-pipeline/flink-cdc.md)
- [数据倾斜治理](optimization/data-skew.md)
- [小文件治理](optimization/small-files.md)
- [任务调度系统](platform/scheduler.md)
- [元数据与血缘](governance/metadata-lineage.md)
- [数据质量](governance/data-quality.md)
- [数据安全与权限](governance/security.md)
- [资源与成本治理](platform/resource-cost.md)
- [大数据项目面试模板](project-experience.md)
- [大数据基础概念](fundamentals/basic-concepts.md)
- [批处理与流处理](fundamentals/batch-vs-stream.md)
- [数据格式与压缩](fundamentals/file-format-compression.md)
- [Hive 分区与分桶](hive/partition-bucket.md)
- [Hive Metastore](hive/metastore.md)
- [Spark RDD/DataFrame/Dataset](spark/rdd-dataframe-dataset.md)
- [Spark 内存与 OOM](spark/memory-oom.md)
- [Flink Window 与 Watermark](flink/window-watermark.md)
- [Flink State Backend](flink/state-backend.md)
- [HBase Compaction 与 Region](hbase/compaction-region.md)
- [ClickHouse 查询优化](clickhouse/query-optimization.md)
- [数据采集与日志链路](data-pipeline/log-collection.md)
- [数据同步工具](data-pipeline/sync-tools.md)
- [指标体系与口径治理](data-warehouse/metrics.md)
- [维度建模与拉链表](data-warehouse/dimensional-modeling.md)
- [湖仓选型对比](lakehouse/table-format-comparison.md)
- [大数据线上排障手册](operations/troubleshooting.md)
- [大数据学习路线](learning-path.md)
""",
    ),
    (
        "Hadoop 总览",
        "11-bigdata/hadoop/README.md",
        """# Hadoop 总览

Hadoop 是大数据基础设施的经典体系，核心包括 HDFS、YARN、MapReduce，以及围绕它构建的 Hive、HBase、Spark 等生态组件。

## 核心组件

- HDFS：分布式文件系统，负责大文件高吞吐存储。
- YARN：资源管理与任务调度，负责集群资源分配。
- MapReduce：批处理计算模型，适合大规模离线计算。

## 当前定位

- Hadoop 仍是理解大数据底层的基础，但新项目可能更多使用对象存储、Kubernetes、云数仓和湖仓表格式。
- 面试中 Hadoop 常作为基础题，重点考 HDFS 架构、YARN 调度、MapReduce Shuffle 和容错机制。

## 常见面试问题

- HDFS 为什么适合大文件而不适合小文件？
- NameNode 宕机如何恢复？
- YARN 的 ResourceManager 和 NodeManager 分别做什么？
- MapReduce 的 Shuffle 为什么是性能瓶颈？
- Hadoop 和 Spark/Flink 的关系是什么？

## 阅读顺序

1. [HDFS](hdfs.md)
2. [YARN](yarn.md)
3. [MapReduce](mapreduce.md)
""",
    ),
    (
        "HDFS",
        "11-bigdata/hadoop/hdfs.md",
        """# HDFS

HDFS 是 Hadoop Distributed File System，面向大文件、高吞吐、一次写入多次读取的分布式文件系统。

## 核心架构

- NameNode：管理文件系统命名空间、目录树、文件到 Block 的映射、Block 到 DataNode 的位置。
- DataNode：存储真实数据块，定期向 NameNode 发送心跳和块汇报。
- SecondaryNameNode：负责辅助 Checkpoint，不是 NameNode 的热备。
- JournalNode：HA 模式下保存共享 EditLog。
- ZKFC：基于 ZooKeeper 做 NameNode 主备选举和故障切换。

## Block 机制

- HDFS 文件会被切分为多个 Block，常见块大小是 128MB 或 256MB。
- 每个 Block 默认 3 副本，副本放置通常跨机架，兼顾可靠性和网络成本。
- Block 大可以减少 NameNode 元数据压力，也适合顺序读写。

## 写入流程

1. Client 向 NameNode 请求创建文件。
2. NameNode 检查权限和路径，返回可写 DataNode 列表。
3. Client 将数据切成 packet，通过 pipeline 写入多个 DataNode。
4. DataNode 按链式复制写入并逐级 ack。
5. Client 完成所有 Block 后通知 NameNode 关闭文件。

## 读取流程

1. Client 向 NameNode 获取文件 Block 位置信息。
2. Client 优先选择就近 DataNode 读取。
3. 读取失败时切换到其他副本。
4. NameNode 不参与真实数据传输，只返回元数据。

## 元数据机制

- FsImage：某一时刻完整的文件系统元数据快照。
- EditLog：FsImage 之后的增量变更日志。
- Checkpoint：合并 FsImage 和 EditLog，避免 EditLog 无限增长。

## 高可用

- Active NameNode 处理读写请求。
- Standby NameNode 同步 EditLog 并维护接近实时的元数据状态。
- JournalNode 保存共享日志，通常要求多数派写入成功。
- ZKFC 负责健康检查、主备选举和 fencing，避免脑裂。

## 小文件问题

- 每个文件和 Block 都会占用 NameNode 内存元数据。
- 大量小文件会导致 NameNode 内存压力、RPC 压力和任务调度开销。
- 解决方案：SequenceFile、HAR、CombineInputFormat、合并入 Hive 分区、使用对象存储或湖仓表格式治理。

## 容错机制

- 心跳：判断 DataNode 是否存活。
- 块汇报：同步 DataNode 上的 Block 列表。
- 副本恢复：副本数低于阈值时自动复制。
- 安全模式：NameNode 启动后等待足够 Block 汇报，期间限制写操作。

## 新特性与趋势

- Federation：多个 NameNode 管理不同命名空间，缓解单 NameNode 元数据瓶颈。
- Erasure Coding：纠删码降低存储成本，适合冷数据。
- 对象存储替代：云上常用 S3/OSS/COS 替代 HDFS，但一致性、rename 成本和元数据能力不同。

## 面试重点

- SecondaryNameNode 不是热备。
- NameNode 内存决定可管理文件数量上限。
- HDFS 适合大文件顺序读写，不适合低延迟随机读写和大量小文件。
- HDFS HA 依赖 JournalNode、ZooKeeper 和 fencing。

## 项目表达

可以这样说：日志原始数据先落 HDFS 的 ODS 层，按日期和业务线分区；小文件通过定时合并治理；冷热数据用不同副本策略或纠删码降低成本；NameNode 监控关注 Heap、RPC 延迟、Block 数量和 Under Replicated Blocks。
""",
    ),
    (
        "YARN",
        "11-bigdata/hadoop/yarn.md",
        """# YARN

YARN 是 Hadoop 的资源管理和任务调度系统，用于在集群中统一管理 CPU、内存等资源，并调度 MapReduce、Spark、Flink 等任务。

## 核心角色

- ResourceManager：全局资源管理和调度。
- NodeManager：单节点资源管理、容器启动、资源上报。
- ApplicationMaster：每个应用一个，负责应用内部任务调度和状态协调。
- Container：资源分配单位，包含 CPU、内存等资源描述。

## 任务提交流程

1. Client 提交应用到 ResourceManager。
2. ResourceManager 分配第一个 Container 启动 ApplicationMaster。
3. ApplicationMaster 向 ResourceManager 申请更多 Container。
4. NodeManager 在对应节点启动任务。
5. ApplicationMaster 跟踪任务状态并完成应用。

## 调度器

- FIFO Scheduler：按提交顺序执行，简单但不适合多租户。
- Capacity Scheduler：按队列容量分配资源，适合多部门共享集群。
- Fair Scheduler：尽量让任务公平获得资源。

## 资源治理

- 队列隔离：不同业务线配置不同资源队列。
- 资源上限：限制单队列、单用户最大资源占用。
- 优先级：重要任务优先调度。
- 抢占：低优任务释放资源给高优任务。

## 常见问题

- 任务长时间 ACCEPTED：队列资源不足、AM 资源不足或队列限制。
- Container 被 kill：内存超限、节点异常、磁盘问题。
- 资源利用率低：队列配置不合理、小任务过多、数据倾斜。

## 面试重点

- ResourceManager 管全局资源，不负责每个 Task 的细粒度调度。
- ApplicationMaster 是应用级调度核心。
- YARN 通过 Container 抽象资源，支持多计算框架共存。
""",
    ),
    (
        "MapReduce",
        "11-bigdata/hadoop/mapreduce.md",
        """# MapReduce

MapReduce 是经典离线批处理模型，将计算拆成 Map、Shuffle、Reduce 三个核心阶段。

## 执行流程

1. InputFormat 将输入数据切分为 Split。
2. MapTask 读取 Split 并输出 key-value。
3. Map 端按分区、排序、溢写生成中间文件。
4. Reduce 端拉取各 Map 输出，这一步称为 Shuffle。
5. Reduce 按 key 聚合处理并输出结果。

## Shuffle 机制

- Partition：决定 key 进入哪个 Reduce。
- Sort：Map 端和 Reduce 端都会按 key 排序。
- Spill：Map 输出缓冲区达到阈值后溢写磁盘。
- Merge：多个溢写文件合并。
- Fetch：Reduce 从多个 Map 节点拉取数据。

## 性能瓶颈

- Shuffle 大量网络和磁盘 IO。
- Reduce 数据倾斜导致少数任务拖慢整体作业。
- 小文件导致 Split 过多，任务启动开销大。
- 序列化和压缩配置不合理。

## 优化手段

- 使用 Combiner 减少 Map 输出。
- 合理设置 Reduce 数量。
- 对倾斜 key 做打散、预聚合或单独处理。
- 启用中间结果压缩。
- 使用 CombineInputFormat 合并小文件。

## 当前定位

MapReduce 原生 API 已较少直接编写，但它的 Shuffle、分区、排序、容错思想仍是理解 Hive、Spark 的基础。
""",
    ),
    (
        "Hive",
        "11-bigdata/hive/README.md",
        """# Hive

Hive 是构建在 Hadoop 生态上的数据仓库工具，通过 SQL 方式处理 HDFS 上的大规模数据。

## 核心架构

- HiveServer2：对外提供 JDBC/ODBC 查询服务。
- Driver：解析 SQL、生成执行计划、提交任务。
- Metastore：存储库、表、分区、字段、位置等元数据。
- Execution Engine：可使用 MapReduce、Tez、Spark 等执行引擎。
- Storage：通常是 HDFS、对象存储或湖仓表格式。

## 表类型

- 内部表：Hive 管理数据生命周期，删表会删除数据。
- 外部表：Hive 只管理元数据，删表通常不删除底层数据。
- 分区表：按日期、业务线等字段拆目录，提高裁剪效率。
- 分桶表：按字段 hash 到固定 bucket，利于采样和 Join 优化。

## 文件格式

- TextFile：简单但性能差。
- ORC：Hive 常用列式格式，支持压缩、索引和谓词下推。
- Parquet：生态通用列式格式，Spark/Presto/Trino 常用。
- Avro：适合 schema 演进和行式交换。

## 常见场景

- 离线数仓 ETL。
- 日志分析和报表统计。
- 用户画像和宽表构建。
- 大规模明细数据归档查询。

## 面试重点

- Metastore 的作用。
- 分区和分桶的区别。
- 小文件治理。
- Hive SQL 执行流程。
- Map Join、Bucket Join、Sort Merge Bucket Join。
- ORC/Parquet 的优势。

## 相关文档

- [Hive SQL 优化](sql-optimization.md)
""",
    ),
    (
        "Hive SQL 优化",
        "11-bigdata/hive/sql-optimization.md",
        """# Hive SQL 优化

Hive SQL 优化目标是减少扫描数据量、减少 Shuffle、降低小文件和数据倾斜影响。

## 分区裁剪

- 查询条件必须带上分区字段。
- 避免对分区字段使用函数导致无法裁剪。
- 常见分区字段：dt、hour、region、biz_type。

## 列裁剪和谓词下推

- 使用 ORC/Parquet 等列式格式，只读取需要的列。
- where 条件尽量提前过滤。
- 避免 `select *`。

## Join 优化

- Map Join：小表加载到内存，大表 Map 端直接 Join，避免 Reduce Shuffle。
- Bucket Join：两表按 Join key 分桶，减少 Shuffle。
- Sort Merge Bucket Join：分桶且排序后可高效 Join。
- 大表 Join 大表：关注 key 分布和倾斜。

## 数据倾斜

- 现象：少数 Reduce 执行极慢。
- 原因：热点 key、空值 key、业务分布不均。
- 解决：热点 key 单独处理、随机前缀打散、两阶段聚合、过滤无效 key。

## 小文件治理

- 小文件会增加 NameNode 压力和任务启动开销。
- 写入阶段控制 Reducer 数量。
- 定期 compaction 或 insert overwrite 合并。
- 使用 ORC/Parquet 并设置合理文件大小。

## 参数方向

- 开启并行执行。
- 开启 CBO 成本优化。
- 配置自动 Map Join 阈值。
- 配置输出文件合并。

## 面试回答模板

Hive SQL 慢时，我会先看执行计划，确认是否命中分区裁剪和列裁剪；再看 Join 是否产生大 Shuffle；然后检查是否有数据倾斜和小文件；最后结合 ORC/Parquet、Map Join、两阶段聚合和文件合并进行优化。
""",
    ),
    (
        "Spark",
        "11-bigdata/spark/README.md",
        """# Spark

Spark 是通用大数据计算引擎，适合批处理、交互式分析、机器学习和部分流式处理场景。

## 核心概念

- Driver：运行用户程序，生成 DAG，调度任务。
- Executor：执行 Task，缓存数据，返回结果。
- RDD：弹性分布式数据集，Spark 的底层抽象。
- DataFrame/Dataset：结构化 API，支持 Catalyst 优化。
- DAG：由依赖关系构成的有向无环图。
- Stage：遇到宽依赖 Shuffle 时切分 Stage。
- Task：最小执行单元，对应分区上的计算。

## RDD、DataFrame、Dataset

- RDD：类型灵活，控制力强，优化能力弱。
- DataFrame：结构化数据，优化器可优化，性能通常更好。
- Dataset：类型安全，兼顾结构化优化和强类型能力。

## 执行流程

1. 用户代码构建逻辑计划。
2. Catalyst 优化生成物理计划。
3. DAGScheduler 切分 Stage。
4. TaskScheduler 分发 Task 到 Executor。
5. Executor 执行并返回结果。

## 重点能力

- Spark SQL 优化。
- Shuffle 调优。
- Cache/Persist/Checkpoint。
- 广播变量和累加器。
- AQE 自适应执行。

## 常见面试问题

- 宽依赖和窄依赖区别。
- Spark 为什么比 MapReduce 快？
- Shuffle 过程和优化方式。
- Cache、Persist、Checkpoint 区别。
- Spark OOM 如何排查？

## 相关文档

- [Spark Shuffle](shuffle.md)
""",
    ),
    (
        "Spark Shuffle",
        "11-bigdata/spark/shuffle.md",
        """# Spark Shuffle

Shuffle 是 Spark 中跨分区、跨节点重分布数据的过程，常见于 groupByKey、reduceByKey、join、distinct、repartition 等操作。

## 为什么产生 Shuffle

- 相同 key 的数据需要汇聚到同一个分区。
- Join 两侧数据需要按 key 重新分布。
- 全局排序或去重需要跨分区协调。

## 执行机制

- Map 端将输出按 Reduce 分区写入本地 Shuffle 文件。
- Reduce 端从多个 Executor 拉取属于自己的数据块。
- 拉取后进行聚合、排序或 Join。

## 性能问题

- 网络 IO 大。
- 磁盘 IO 大。
- 序列化成本高。
- 数据倾斜导致部分 Task 极慢。
- 分区数不合理导致小任务过多或单任务过大。

## 优化策略

- 优先使用 reduceByKey/aggregateByKey，避免 groupByKey。
- Join 小表时使用 Broadcast Join。
- 合理设置 `spark.sql.shuffle.partitions`。
- 开启 AQE，让 Spark 自动合并小分区、处理倾斜 Join。
- 对热点 key 做打散或单独处理。
- 使用 Kryo 序列化和高效列式格式。

## 数据倾斜处理

- 过滤异常 key。
- 热点 key 单独计算。
- 随机前缀打散，两阶段聚合。
- Broadcast Join 替代 Shuffle Join。
- AQE skew join 自动优化。

## 面试重点

回答 Spark Shuffle 时，要讲清“为什么产生、怎么写、怎么拉、为什么慢、如何优化”。不要只背宽依赖和窄依赖定义。
""",
    ),
    (
        "Flink",
        "11-bigdata/flink/README.md",
        """# Flink

Flink 是面向有状态流处理的分布式计算引擎，适合实时计算、实时数仓、风控、监控告警和事件驱动场景。

## 核心概念

- JobManager：负责任务调度、Checkpoint 协调和故障恢复。
- TaskManager：执行算子任务，管理 slot。
- Slot：资源调度单位。
- Operator：流处理算子。
- State：有状态计算的数据。
- Checkpoint：一致性快照，用于故障恢复。
- Watermark：衡量事件时间进度，处理乱序数据。

## 时间语义

- Processing Time：处理时间，延迟低但结果受处理速度影响。
- Event Time：事件发生时间，适合乱序和迟到数据。
- Ingestion Time：进入 Flink 的时间。

## Window

- 滚动窗口：固定大小、不重叠。
- 滑动窗口：固定大小、按步长滑动，可重叠。
- 会话窗口：按用户活动间隔切分。
- 全局窗口：需要自定义触发器。

## 状态管理

- Keyed State：按 key 隔离，最常用。
- Operator State：算子级状态。
- State Backend：HashMap、RocksDB、Changelog 等。

## 常见面试问题

- Flink 和 Spark Streaming 的区别。
- Checkpoint 如何实现一致性。
- Exactly Once 如何保证。
- Watermark 如何处理乱序。
- 反压如何定位。

## 相关文档

- [Checkpoint](checkpoint.md)
- [Exactly Once](exactly-once.md)
""",
    ),
    (
        "Flink Checkpoint",
        "11-bigdata/flink/checkpoint.md",
        """# Flink Checkpoint

Checkpoint 是 Flink 容错机制的核心，通过周期性生成分布式一致性快照，在故障后恢复状态和消费位置。

## 核心原理

- JobManager 周期性触发 Checkpoint。
- Source 接收 Checkpoint Barrier，并将 Barrier 注入数据流。
- Barrier 随数据流经过各个算子。
- 算子收到所有上游 Barrier 后对状态做快照。
- 所有算子完成快照后，Checkpoint 成功。

## Barrier 对齐

- 对齐 Checkpoint：多输入算子等待所有输入流的 Barrier 到齐，保证一致性。
- 非对齐 Checkpoint：将输入缓冲中的数据也纳入快照，适合反压严重场景。

## State Backend

- HashMapStateBackend：状态在 JVM 堆内，适合小状态、低延迟。
- EmbeddedRocksDBStateBackend：状态在 RocksDB，适合大状态，但读写有序列化和磁盘成本。
- Changelog State Backend：减少大状态 Checkpoint 成本。

## Checkpoint 配置

- 间隔：不能过短，否则影响吞吐。
- 超时时间：状态大或外部存储慢时需要调大。
- 最小间隔：避免 Checkpoint 堆积。
- 并发数：通常设置为 1，降低复杂度。
- Externalized Checkpoint：作业取消后保留快照。

## 常见问题

- Checkpoint 超时：状态过大、反压、外部存储慢、Barrier 对齐慢。
- Checkpoint 失败：状态序列化错误、权限问题、存储不可用。
- 恢复慢：状态大、RocksDB 文件多、网络或对象存储慢。

## 面试重点

Checkpoint 不是简单定时保存数据，它是基于 Barrier 的分布式一致性快照，配合 Source offset 和 Sink 事务能力，才能支撑端到端一致性。
""",
    ),
    (
        "Flink Exactly Once",
        "11-bigdata/flink/exactly-once.md",
        """# Flink Exactly Once

Flink 的 Exactly Once 指在故障恢复后，状态计算结果不重复、不丢失。端到端 Exactly Once 还要求 Source 和 Sink 配合。

## 层次区分

- 状态 Exactly Once：Flink 内部状态通过 Checkpoint 保证一致恢复。
- Source Exactly Once：Source 需要可重放并能保存消费位置，例如 Kafka offset。
- Sink Exactly Once：Sink 需要事务、幂等或两阶段提交能力。

## Kafka Source

- Checkpoint 成功时提交 offset。
- 故障恢复时从 Checkpoint 中的 offset 继续消费。
- 如果处理成功但 Checkpoint 未完成，恢复后可能重新消费，但状态会回滚到一致点。

## 两阶段提交 Sink

1. 开启事务并写入临时结果。
2. Checkpoint 触发时预提交事务。
3. Checkpoint 成功后正式提交事务。
4. Checkpoint 失败或任务失败时回滚事务。

## 常见 Sink 方案

- Kafka：事务 Producer 支持 Exactly Once。
- 数据库：可通过幂等主键、事务表、批次号保证最终一致。
- 文件系统：先写临时文件，Checkpoint 成功后提交文件。
- ClickHouse/ES：通常依赖幂等写入或去重策略，严格 Exactly Once 较难。

## 常见误区

- Flink 开启 Checkpoint 不等于端到端 Exactly Once。
- Exactly Once 不代表外部系统看不到中间状态，取决于 Sink 提交语义。
- 幂等写入常比强事务更实用，但需要业务主键和去重策略。

## 面试回答模板

Flink 内部通过 Barrier 和 Checkpoint 保证状态一致性；Source 通过保存 offset 支持重放；Sink 通过两阶段提交或幂等写入保证外部结果一致。因此端到端 Exactly Once 是 Source、Flink 状态和 Sink 三者共同完成的。
""",
    ),
    (
        "HBase",
        "11-bigdata/hbase/README.md",
        """# HBase

HBase 是基于 HDFS 的分布式、列族式、宽表 NoSQL 数据库，适合海量稀疏数据和按 RowKey 的低延迟随机读写。

## 核心架构

- HMaster：管理表、Region 分配、故障恢复。
- RegionServer：承载 Region，处理读写请求。
- Region：表按 RowKey 范围切分的分片。
- MemStore：内存写缓冲。
- HFile：落盘后的不可变存储文件。
- WAL：预写日志，用于故障恢复。
- ZooKeeper：协调 Master、RegionServer 状态。

## 写入流程

1. Client 根据 RowKey 定位 RegionServer。
2. 写 WAL，保证故障可恢复。
3. 写 MemStore。
4. MemStore 达到阈值 flush 为 HFile。
5. 后台执行 Compaction 合并 HFile。

## 读取流程

- 先查 MemStore 和 BlockCache。
- 再查 HFile。
- 多版本数据根据时间戳和版本策略过滤。

## 适合场景

- 用户画像宽表。
- 设备/账号维度明细查询。
- 风控特征存储。
- 海量稀疏 KV 数据。

## 不适合场景

- 复杂 SQL 查询。
- 多字段任意组合查询。
- 强事务关系模型。
- 高效聚合分析。

## 相关文档

- [RowKey 设计](rowkey-design.md)
""",
    ),
    (
        "HBase RowKey 设计",
        "11-bigdata/hbase/rowkey-design.md",
        """# HBase RowKey 设计

RowKey 是 HBase 查询和分布的核心，设计不好会导致热点、扫描低效和 Region 不均衡。

## 设计原则

- 查询优先：RowKey 应匹配最核心的查询路径。
- 离散均匀：避免单调递增导致写热点。
- 长度适中：过长增加存储和网络成本。
- 可排序：利用字典序支持范围扫描。
- 避免频繁变更：RowKey 一旦写入不适合修改。

## 常见方案

- Hash 前缀：对用户 ID、设备 ID hash 后加前缀，打散写入。
- 反转 Key：手机号、时间戳等单调字段可反转降低热点。
- Salt：加随机或 hash salt 分散 Region。
- 业务维度组合：例如 `hash(userId)#userId#reverseTs`。
- 时间倒排：最近数据优先查询时使用反向时间戳。

## 热点问题

- 原因：RowKey 单调递增或热点用户集中写入。
- 表现：单个 RegionServer QPS、延迟、Compaction 压力明显高。
- 解决：预分区、加盐、hash 前缀、热点 key 拆分。

## 查询模式

- 点查：RowKey 精确命中，性能最好。
- 范围扫描：需要 RowKey 前缀和排序设计支持。
- 多条件查询：通常需要二级索引、冗余表或借助 ES/ClickHouse。

## 面试重点

RowKey 设计不是越随机越好。随机可以打散写入，但会破坏范围扫描。好的设计需要在写入均衡和查询效率之间取舍。
""",
    ),
    (
        "ClickHouse",
        "11-bigdata/clickhouse/README.md",
        """# ClickHouse

ClickHouse 是高性能列式 OLAP 数据库，适合大宽表、明细分析、报表、日志分析和用户行为分析。

## 为什么快

- 列式存储：只读取查询需要的列。
- 向量化执行：批量处理数据，提高 CPU 利用率。
- 数据压缩：列式数据相似度高，压缩率好。
- 稀疏索引：通过排序键快速跳过无关数据块。
- 分区裁剪：按分区过滤减少扫描范围。
- 并行执行：充分利用多核和分布式资源。

## 核心概念

- MergeTree：最核心的表引擎家族。
- Partition：分区，通常按日期或业务周期划分。
- ORDER BY：排序键，决定数据物理排序和稀疏索引。
- Primary Key：主键索引，ClickHouse 中不保证唯一。
- Part：每次写入形成的数据片段，后台合并。

## 适合场景

- 实时报表。
- 用户行为分析。
- 日志检索和聚合。
- 大宽表多维分析。
- 替代部分 Hive 离线查询和 MySQL 报表查询。

## 不适合场景

- 高频小事务更新。
- OLTP 强一致交易。
- 多表复杂事务。
- 低延迟点查不是它的主要优势。

## 查询优化

- 分区键用于裁剪数据目录。
- 排序键按高频过滤条件和聚合维度设计。
- 避免过多小批量写入。
- 使用物化视图预聚合。
- 控制高基数字段 group by。

## 相关文档

- [MergeTree](mergetree.md)
""",
    ),
    (
        "MergeTree",
        "11-bigdata/clickhouse/mergetree.md",
        """# MergeTree

MergeTree 是 ClickHouse 最重要的表引擎家族，负责列式存储、分区、排序、索引和后台合并。

## 核心结构

- Partition：按分区表达式拆分数据。
- Part：一次写入生成一个或多个数据片段。
- Mark：稀疏索引标记，定位数据块。
- ORDER BY：决定数据在 Part 内的排序方式。
- Primary Key：用于构建稀疏索引，通常与 ORDER BY 相同或是其前缀。

## 写入机制

- 数据批量写入形成 Part。
- Part 内按 ORDER BY 排序。
- 后台 Merge 任务合并多个小 Part。
- 过多小 Part 会影响查询和合并性能。

## 分区键设计

- 常用日期分区，例如 `toYYYYMM(dt)` 或 `toDate(event_time)`。
- 分区不宜过细，否则 Part 数量暴增。
- 查询条件应尽量带分区字段。

## 排序键设计

- 优先放高频过滤字段。
- 再放常用聚合维度。
- 低基数字段放前面通常有利于压缩和过滤。
- 排序键不是唯一约束，不要当 MySQL 主键理解。

## 常见表引擎

- MergeTree：基础引擎。
- ReplacingMergeTree：按版本或最终合并去重，适合 CDC 明细去重。
- SummingMergeTree：按排序键聚合数值列。
- AggregatingMergeTree：存储聚合状态，适合预聚合。
- CollapsingMergeTree：通过 sign 字段折叠数据。

## 面试重点

ClickHouse 快不是因为“有索引”这么简单，而是分区裁剪、排序键、稀疏索引、列式压缩、向量化执行和后台合并共同作用。
""",
    ),
    (
        "数仓建模",
        "11-bigdata/data-warehouse/README.md",
        """# 数仓建模

数据仓库用于把分散的业务数据转化为统一、稳定、可分析的数据资产。

## 分层模型

- ODS：原始数据层，尽量保持源系统原貌。
- DWD：明细数据层，清洗、规范化、去重、补充维度键。
- DWS：汇总数据层，面向主题域做公共聚合。
- ADS：应用数据层，面向报表、产品、运营、算法等具体应用。

## 建模方法

- 维度建模：事实表 + 维度表，适合分析型查询。
- 星型模型：事实表直接关联多个维表，查询简单。
- 雪花模型：维表继续规范化，冗余少但查询复杂。
- Data Vault：适合复杂企业数据集成和历史追踪。

## 常见表

- 事实表：交易、点击、支付、退款等可度量事件。
- 维度表：用户、商品、门店、地区等描述性实体。
- 快照表：周期性保存状态。
- 拉链表：记录维度历史变化。

## 质量治理

- 完整性：数据是否缺失。
- 准确性：数据是否符合业务规则。
- 一致性：多个口径是否统一。
- 及时性：数据是否按 SLA 产出。
- 唯一性：是否重复。

## 面试重点

- 为什么要分层？
- ODS、DWD、DWS、ADS 各层职责。
- 宽表和维度建模的取舍。
- 拉链表如何处理历史变化。
- 指标口径如何治理。

## 相关文档

- [ODS/DWD/DWS/ADS](ods-dwd-dws-ads.md)
""",
    ),
    (
        "ODS/DWD/DWS/ADS",
        "11-bigdata/data-warehouse/ods-dwd-dws-ads.md",
        """# ODS/DWD/DWS/ADS

数仓分层的核心目标是解耦数据接入、清洗建模、公共汇总和应用服务，降低重复开发和口径混乱。

## ODS 原始数据层

- 保留源系统原始数据。
- 通常按业务系统、表名、日期分区。
- 少做业务加工，只做必要格式转换和入湖入仓。
- 用于追溯和重新加工。

## DWD 明细数据层

- 做清洗、去重、脱敏、字段标准化。
- 统一时间、ID、枚举、币种、状态等口径。
- 构建业务过程事实表。
- 保持明细粒度，不做过度聚合。

## DWS 汇总数据层

- 围绕主题域沉淀公共汇总。
- 例如用户日汇总、商品日汇总、交易日汇总。
- 服务多个 ADS 应用，避免重复计算。
- 指标口径应统一管理。

## ADS 应用数据层

- 面向具体报表、接口、应用和算法。
- 可以根据查询性能做宽表、预聚合和冗余。
- 生命周期通常跟业务需求强相关。

## 分层收益

- 降低重复 ETL。
- 提升指标一致性。
- 方便数据血缘追踪。
- 支持故障回溯和重跑。
- 便于权限和成本治理。

## 常见问题

- 层级过多导致链路长、延迟高。
- ADS 口径私有化，导致指标不一致。
- DWD 过度宽表化，复用性下降。
- ODS 缺少原始保留，无法追溯。

## 面试表达

我会把原始业务表或日志先进入 ODS；在 DWD 做清洗、去重和业务过程建模；在 DWS 沉淀公共主题汇总；最后在 ADS 面向报表和接口做应用层宽表或预聚合。这样可以保证复用、口径统一和问题可追溯。
""",
    ),
    (
        "数据链路与湖仓",
        "11-bigdata/data-pipeline/README.md",
        """# 数据链路与湖仓

数据链路关注数据从业务系统、日志、消息队列进入数仓或湖仓，并最终服务分析、检索、推荐和风控的全过程。

## 常见链路

- 业务库 CDC -> Kafka -> Flink -> Hudi/Iceberg/ClickHouse。
- 日志采集 -> Kafka -> Flink/Spark -> Hive/ClickHouse/ES。
- MySQL -> DataX/Sqoop -> Hive 离线同步。
- Kafka -> Flink -> Redis/HBase，用于实时特征。

## CDC

- CDC 是 Change Data Capture，捕获数据库变更。
- MySQL 常基于 binlog，例如 Canal、Debezium、Flink CDC。
- 需要处理全量同步、增量同步、断点续传、DDL 变更和乱序。

## Lambda 与 Kappa

- Lambda：离线链路 + 实时链路，两套计算结果合并，稳定但复杂。
- Kappa：只保留流式链路，通过重放消息修正结果，架构简单但依赖消息保留和流计算能力。

## 湖仓表格式

- Hudi：强调 upsert、增量查询和近实时入湖。
- Iceberg：强调开放表格式、快照、Schema 演进和多引擎兼容。
- Delta Lake：Databricks 生态成熟，支持 ACID 和流批统一。

## 数据治理

- 元数据：表、字段、分区、负责人、生命周期。
- 血缘：字段和任务依赖关系。
- 质量：空值、重复、波动、枚举、主键唯一。
- 权限：库表、列级、行级和脱敏策略。
- 成本：存储生命周期、计算资源、冷热分层。

## 面试重点

- CDC 如何保证不丢不重？
- Flink 写湖仓如何保证一致性？
- Hudi、Iceberg、Delta Lake 区别？
- 实时数仓如何分层？
- 数据质量和血缘如何建设？

## 项目表达

可以描述一个实时数仓链路：MySQL binlog 通过 Flink CDC 进入 Kafka，Flink 做清洗和维表关联后写入 Iceberg DWD；DWS 通过 Flink SQL 做实时聚合；ADS 写入 ClickHouse 支撑报表查询，同时用数据质量任务监控延迟、重复和指标波动。
""",
    ),
    (
        "实时数仓",
        "11-bigdata/data-warehouse/realtime-warehouse.md",
        """# 实时数仓

实时数仓用于把业务事件、日志、CDC 数据在秒级或分钟级加工成可查询、可分析、可告警的数据资产。

## 常见架构

- Source：业务库 CDC、埋点日志、服务日志、MQ 事件。
- Buffer：Kafka/Pulsar，承担削峰、解耦和可重放。
- Compute：Flink/Flink SQL，完成清洗、维表关联、聚合和状态计算。
- Storage：Kafka、Hudi、Iceberg、ClickHouse、Doris、Redis、HBase。
- Serving：BI 报表、实时大屏、风控接口、推荐特征、告警系统。

## 分层方式

- ODS：原始实时数据，通常保留 Kafka 原始 Topic 或入湖原始表。
- DWD：实时明细层，做清洗、去重、标准化、宽化。
- DWS：实时汇总层，按主题域做窗口聚合或累计指标。
- ADS：应用层，写入 ClickHouse/Doris/Redis 支撑查询和服务。

## 关键问题

- 乱序与迟到：使用 Event Time、Watermark、Allowed Lateness。
- 去重：基于业务唯一键、状态 TTL、幂等 Sink。
- 维表关联：广播维表、异步 IO、Temporal Join、维表缓存。
- 一致性：Checkpoint、两阶段提交、幂等写入、批次号。
- 回溯重算：保留 Kafka 数据、支持 Savepoint、湖仓快照和任务版本管理。

## Lambda 与 Kappa

- Lambda 架构：离线链路保证准确性，实时链路保证时效性，缺点是两套逻辑维护成本高。
- Kappa 架构：以流处理为主，通过消息重放修正历史，架构简单但对流引擎和数据保留要求高。

## 面试重点

- 实时数仓如何分层？
- 如何处理迟到数据？
- 如何保证端到端一致性？
- 维表 Join 如何做？
- 实时指标和离线指标不一致如何排查？

## 项目表达

可以描述为：用户行为日志进入 Kafka，Flink 清洗后形成 DWD 明细流，关联 MySQL 维表生成宽表，再按事件时间窗口聚合到 DWS，最终写入 Doris/ClickHouse 提供实时看板；通过 Checkpoint、幂等主键和数据质量规则保证链路稳定。
""",
    ),
    (
        "Apache Doris",
        "11-bigdata/olap/doris.md",
        """# Apache Doris

Apache Doris 是高性能实时分析数据库，适合报表分析、用户行为分析、实时数仓 ADS 层和多维 OLAP 查询。

## 核心架构

- FE：Frontend，负责元数据、SQL 解析、优化、调度和集群管理。
- BE：Backend，负责数据存储、计算执行和副本管理。
- Tablet：数据分片单位。
- Stream Load/Routine Load/Broker Load：常见导入方式。

## 数据模型

- Duplicate Key：明细模型，保留重复数据，适合日志明细。
- Aggregate Key：聚合模型，导入时按 key 聚合指标。
- Unique Key：唯一模型，适合主键更新场景。
- Primary Key：更适合高频更新和部分列更新的新模型。

## 为什么适合实时数仓

- 支持高并发低延迟 OLAP 查询。
- 支持 Kafka Routine Load 实时导入。
- 支持物化视图、分区、分桶和向量化执行。
- SQL 兼容性较好，易服务 BI 和报表。

## 设计重点

- 分区：通常按日期分区，便于冷热管理和分区裁剪。
- 分桶：按高频过滤或 Join 字段 hash 分桶，避免数据倾斜。
- Key 模型：根据明细、聚合、更新需求选择。
- 副本：根据可用性和成本设置副本数。

## 常见问题

- 导入失败：字段类型不匹配、脏数据、版本堆积、内存限制。
- 查询慢：分区未裁剪、分桶不合理、大宽表扫描、高基数聚合。
- Compaction 压力：小批量写入过多或更新频繁。

## Doris 与 ClickHouse

- Doris 更强调实时导入、MPP 查询、易用性和 MySQL 协议兼容。
- ClickHouse 在列式压缩、单表明细分析和生态成熟度上有优势。
- 选型要看写入频率、查询并发、更新需求、运维能力和团队熟悉度。
""",
    ),
    (
        "Trino/Presto",
        "11-bigdata/olap/trino.md",
        """# Trino/Presto

Trino 是分布式 SQL 查询引擎，适合跨数据源交互式查询和湖仓分析。Presto 是其前身生态之一。

## 核心架构

- Coordinator：解析 SQL、生成执行计划、调度 Worker。
- Worker：执行 Task，读取数据源并交换中间结果。
- Connector：连接 Hive、Iceberg、MySQL、Kafka、ClickHouse、ES 等数据源。
- Catalog：数据源配置入口。

## 适合场景

- 数据湖交互式查询。
- 多数据源联邦查询。
- Ad-hoc 分析。
- 替代部分 Hive MR/Tez 慢查询。

## 不适合场景

- 大规模复杂 ETL 长任务。
- 高频小事务写入。
- 强一致 OLTP。

## 性能优化

- 使用列式格式 ORC/Parquet。
- 保证分区裁剪和谓词下推。
- 合理控制 Join 顺序和广播 Join。
- 避免跨源大表 Join。
- 使用动态过滤减少 Probe 侧扫描。
- 控制查询内存和并发。

## 与 Hive/Spark 的区别

- Hive 更偏离线数仓和批处理 SQL。
- Spark 更适合复杂 ETL、机器学习和批流统一计算。
- Trino 更适合低延迟交互式 SQL 和联邦查询。

## 面试重点

Trino 本身不存储数据，核心价值是通过 Connector 连接多种存储，并用 MPP 执行引擎提供交互式 SQL 查询能力。
""",
    ),
    (
        "Apache Iceberg",
        "11-bigdata/lakehouse/iceberg.md",
        """# Apache Iceberg

Iceberg 是开放湖仓表格式，解决 Hive 表在大规模数据湖中的元数据、事务、Schema 演进和多引擎一致性问题。

## 核心能力

- ACID 事务：通过快照提交保证原子性。
- Snapshot：每次提交生成新快照，支持时间旅行和回滚。
- Schema Evolution：支持字段新增、删除、重命名和类型演进。
- Partition Evolution：支持分区策略演进，不需要重写全表。
- Hidden Partition：查询无需显式感知物理分区字段。

## 元数据结构

- Catalog：管理表位置和当前元数据指针。
- Metadata File：记录表 schema、分区、快照等。
- Manifest List：记录本次快照涉及的 manifest。
- Manifest File：记录数据文件和统计信息。
- Data File：真实 Parquet/ORC/Avro 数据文件。

## 查询优化

- 分区裁剪。
- 文件级统计信息裁剪。
- 列式格式谓词下推。
- Snapshot 隔离减少读写冲突。

## 适合场景

- 多引擎共享数据湖：Spark、Flink、Trino、Hive。
- 大规模离线和近实时数仓。
- 需要 schema/分区演进的长期数据资产。
- 需要时间旅行和回滚的场景。

## 面试重点

Iceberg 不是计算引擎，也不是存储系统，它是表格式。它通过元数据和快照机制，让对象存储/HDFS 上的数据具备接近数仓表的管理能力。
""",
    ),
    (
        "Apache Hudi",
        "11-bigdata/lakehouse/hudi.md",
        """# Apache Hudi

Hudi 是湖仓表格式，重点解决数据湖中的 upsert、增量消费、近实时入湖和小文件管理问题。

## 表类型

- Copy On Write：写入时生成新的列式文件，读性能好，写放大较高。
- Merge On Read：增量写入 log 文件，读时合并 base file 和 log，写入延迟低。

## 核心概念

- Record Key：记录唯一键。
- Precombine Field：同一 key 多条记录时选择最新记录。
- Partition Path：分区路径。
- Timeline：记录 commit、clean、compaction 等操作。
- Index：定位记录所在文件，支持 upsert。

## 写入模式

- Insert：只新增。
- Upsert：按主键更新或插入。
- Bulk Insert：大批量初始化导入。
- Delete：删除记录。

## 适合场景

- CDC 入湖。
- 需要增量查询的离线/准实时链路。
- 用户画像、订单状态、维表快照。
- 需要处理更新和删除的数据湖。

## Hudi 与 Iceberg

- Hudi 更强调 upsert、增量拉取和写入服务。
- Iceberg 更强调开放标准、多引擎兼容、快照和分区演进。
- 选型要看是否高频更新、是否需要增量消费、查询引擎生态和团队经验。

## 面试重点

Hudi 的核心不是“把文件放到 HDFS”，而是通过 Timeline、Index、Record Key 和表服务，让数据湖支持更新、增量和近实时消费。
""",
    ),
    (
        "Flink CDC",
        "11-bigdata/data-pipeline/flink-cdc.md",
        """# Flink CDC

Flink CDC 基于数据库日志捕获变更，并将全量和增量数据以 Flink Source 的方式接入实时链路。

## 核心流程

1. 全量阶段：并行读取表快照数据。
2. 增量阶段：读取 binlog/WAL 等变更日志。
3. 切换阶段：保证全量快照和增量日志无缝衔接。
4. 下游写入：写 Kafka、湖仓、Doris、ClickHouse、ES 等。

## 关键能力

- Snapshot 读取。
- Binlog 增量订阅。
- Checkpoint 记录位点。
- Exactly Once Source 语义。
- 支持 DDL 变更同步。

## 常见问题

- 全量阶段对源库压力大。
- 大表快照耗时长。
- DDL 变更导致下游 schema 不兼容。
- binlog 保留时间不足导致断点丢失。
- 主键缺失影响去重和更新语义。

## 生产建议

- 大表分片读取，控制并发和限速。
- 源库开启合适 binlog 格式和保留周期。
- 下游设计主键和幂等写入。
- 建立 DDL 变更流程和 schema registry。
- 监控延迟、位点、失败重启和脏数据。

## 面试重点

Flink CDC 的难点不是“读 binlog”，而是全量和增量一致衔接、Checkpoint 位点恢复、DDL 兼容、下游幂等和源库压力控制。
""",
    ),
    (
        "数据倾斜治理",
        "11-bigdata/optimization/data-skew.md",
        """# 数据倾斜治理

数据倾斜是大数据任务中最常见的性能问题，表现为少数 Task 处理数据远多于其他 Task，导致整体任务被拖慢。

## 常见场景

- group by 热点 key。
- join 某些 key 数据量极大。
- 空值或默认值集中。
- 分区字段选择不合理。
- Kafka 分区 key 不均衡。

## 定位方法

- 查看 Spark/Flink UI 中 Task 输入数据量、执行时间和 Shuffle Read/Write。
- 查看 Reduce 或 SubTask 是否明显拖尾。
- 统计 key 分布 TopN。
- 检查空值、未知值、默认值比例。

## 处理方案

- 过滤无效 key：例如 null、unknown。
- 热点 key 单独处理：拆成独立任务或特殊逻辑。
- 加随机前缀打散：先局部聚合，再去前缀二次聚合。
- Broadcast Join：小表广播避免大 Shuffle。
- AQE Skew Join：让 Spark 自动拆分倾斜分区。
- 重新设计分区键：避免按低基数字段分区。

## 面试表达

我会先通过任务 UI 和 key 分布确认是否是少数 key 导致拖尾；如果是聚合倾斜，用随机前缀做两阶段聚合；如果是 Join 倾斜，小表用广播，热点 key 单独处理；同时把空值和异常值提前过滤。
""",
    ),
    (
        "小文件治理",
        "11-bigdata/optimization/small-files.md",
        """# 小文件治理

小文件会增加 NameNode/Metastore 压力，也会导致计算任务 Split 过多、调度开销高、查询性能下降。

## 产生原因

- 上游并发写入过高，每个并发生成小文件。
- Flink/Spark checkpoint 或滚动策略过频。
- Hive 动态分区过多。
- Kafka 分区过多或批次太小。
- 频繁小批量导入湖仓表。

## 影响

- NameNode 元数据内存压力大。
- 查询需要打开大量文件，IO 开销高。
- Hive/Spark 任务数量过多。
- 湖仓表 manifest/metadata 膨胀。
- ClickHouse/Doris compaction 压力上升。

## 治理方案

- 写入端控制并发和滚动文件大小。
- 定期 compaction 合并小文件。
- Hive 使用 insert overwrite 合并分区。
- Spark 使用 coalesce/repartition 控制输出文件数。
- Iceberg/Hudi 使用表服务合并文件。
- Flink FileSink 配置合理 rolling policy。

## 面试重点

小文件治理要从源头和后处理两端做：源头控制写入并发、批次和滚动策略；后处理通过 compaction、分区合并和生命周期治理降低长期成本。
""",
    ),
    (
        "任务调度系统",
        "11-bigdata/platform/scheduler.md",
        """# 任务调度系统

任务调度系统负责组织数据任务的依赖、定时、补数、失败重试、告警和权限，是数据平台后端的重要能力。

## 常见系统

- DolphinScheduler：国内常用，支持可视化 DAG、多租户、工作流调度。
- Airflow：Python 生态强，适合代码化 DAG。
- Azkaban：较经典，功能相对简单。
- Oozie：Hadoop 生态老牌调度系统。

## 核心能力

- DAG 依赖管理。
- 定时调度和周期实例。
- 失败重试和告警。
- 补数和重跑。
- 参数传递和日期变量。
- 多租户、权限和资源队列。
- 任务日志和运行状态追踪。

## 设计重点

- 调度器高可用。
- Worker 心跳和任务认领。
- 任务幂等和重试安全。
- 大规模 DAG 实例生成性能。
- 补数不能冲垮集群。
- 告警收敛和升级策略。

## 面试重点

数据调度不是简单 crontab。核心是 DAG 依赖、实例状态机、失败恢复、补数、权限、多租户和资源隔离。
""",
    ),
    (
        "元数据与血缘",
        "11-bigdata/governance/metadata-lineage.md",
        """# 元数据与血缘

元数据和血缘用于回答数据资产“有什么、在哪里、谁负责、从哪里来、到哪里去、被谁使用”。

## 元数据类型

- 技术元数据：库、表、字段、类型、分区、存储位置。
- 业务元数据：指标口径、业务含义、负责人、使用场景。
- 操作元数据：任务运行记录、产出时间、访问热度、数据量。
- 权限元数据：用户、角色、授权范围、敏感级别。

## 血缘类型

- 表级血缘：表到表的依赖关系。
- 字段级血缘：字段如何从上游字段计算而来。
- 任务血缘：任务之间的依赖和产出。
- 应用血缘：报表、接口、模型对数据的使用关系。

## 建设方式

- 解析 SQL 获取输入输出表和字段表达式。
- 接入调度系统获取任务依赖。
- 接入 Metastore/Catalog 获取表结构。
- 接入查询日志统计使用情况。
- 使用 OpenLineage、DataHub、Atlas 等生态。

## 价值

- 变更影响分析。
- 故障定位和数据回溯。
- 指标口径治理。
- 数据资产盘点。
- 权限和合规审计。

## 面试重点

字段级血缘比表级血缘更难，因为需要解析 SQL 表达式、UDF、临时表、视图和多引擎语法差异。
""",
    ),
    (
        "数据质量",
        "11-bigdata/governance/data-quality.md",
        """# 数据质量

数据质量用于保障数据可信，避免报表错误、指标波动、模型误判和业务决策失真。

## 质量维度

- 完整性：数据是否缺失。
- 准确性：数据是否符合真实业务。
- 一致性：同一指标在不同系统是否一致。
- 唯一性：主键或业务键是否重复。
- 及时性：是否在 SLA 内产出。
- 有效性：字段是否符合枚举、范围、格式规则。

## 常见规则

- 表行数波动。
- 空值率检查。
- 主键唯一检查。
- 枚举值合法性。
- 金额非负。
- 分区是否产出。
- 同比/环比波动阈值。

## 质量链路

1. 规则配置。
2. 任务运行。
3. 质量结果入库。
4. 告警通知。
5. 阻断或降级。
6. 问题复盘和规则优化。

## 生产实践

- 核心链路设置强规则，失败阻断下游。
- 非核心链路设置弱规则，只告警不阻断。
- 质量规则与表负责人、SLA、血缘联动。
- 指标异常要能追溯到上游分区和任务。

## 面试重点

数据质量不是写几个 SQL 检查，而是规则体系、调度集成、告警分级、血缘影响分析和问题闭环。
""",
    ),
    (
        "数据安全与权限",
        "11-bigdata/governance/security.md",
        """# 数据安全与权限

数据安全关注敏感数据识别、访问控制、脱敏、审计和合规，是数据平台必备能力。

## 敏感数据

- 身份信息：姓名、身份证、手机号、邮箱。
- 金融信息：银行卡、账户、交易流水。
- 位置数据：GPS、地址。
- 设备信息：IMEI、IDFA、IP。
- 行为数据：浏览、点击、购买、搜索。

## 权限模型

- 库表权限。
- 列级权限。
- 行级权限。
- 标签权限。
- 角色权限 RBAC。
- 属性权限 ABAC。

## 脱敏方式

- 静态脱敏：数据落地前处理。
- 动态脱敏：查询时按权限展示。
- 加密存储：敏感字段密文保存。
- Token 化：用 token 替代真实敏感值。

## 审计

- 谁访问了什么数据。
- 访问时间、来源、查询条件。
- 是否导出大量敏感数据。
- 是否越权访问。

## 面试重点

数据权限不能只靠应用层判断。成熟方案需要 Catalog/权限中心/查询引擎联动，支持列级、行级、动态脱敏和审计。
""",
    ),
    (
        "资源与成本治理",
        "11-bigdata/platform/resource-cost.md",
        """# 资源与成本治理

大数据平台成本通常来自计算、存储、网络和低效任务。资源治理是数据平台后端的重要工作。

## 计算治理

- YARN/K8s 队列和命名空间隔离。
- 任务优先级和资源上限。
- 大任务审批。
- 空跑任务清理。
- SQL 自动诊断和拦截。

## 存储治理

- 冷热分层。
- 生命周期管理。
- 分区过期清理。
- 副本数和纠删码策略。
- 小文件合并。
- 无人使用表下线。

## 成本指标

- 表存储大小和增长趋势。
- 任务 CPU/内存使用量。
- 查询扫描字节数。
- 任务运行时长。
- 失败重试次数。
- 数据访问热度。

## 优化手段

- 将高频报表预聚合。
- 使用列式格式和压缩。
- 调整分区和排序键。
- 限制无分区条件扫描。
- 对低频历史数据归档。

## 面试重点

成本治理要用数据驱动：先采集任务、表、查询、存储的成本指标，再做规则、配额、生命周期和优化建议闭环。
""",
    ),
    (
        "大数据项目面试模板",
        "11-bigdata/project-experience.md",
        """# 大数据项目面试模板

找工作时，大数据知识最好落到项目表达，而不是只背组件原理。

## 项目一：实时数仓链路

### 背景

业务需要分钟级查看交易、用户行为或风控指标，原离线 T+1 报表无法满足运营和告警需求。

### 架构

- MySQL binlog 通过 Flink CDC 采集。
- 行为日志进入 Kafka。
- Flink 做清洗、去重、维表 Join 和窗口聚合。
- 明细写入 Iceberg/Hudi，聚合结果写入 Doris/ClickHouse。
- 调度和质量平台监控延迟、空值、重复和指标波动。

### 难点

- 全量和增量一致衔接。
- 迟到数据修正。
- 维表 Join 性能。
- 端到端幂等。
- 实时与离线指标对齐。

### 指标

- 端到端延迟从 T+1 降到 1 分钟内。
- 核心指标准确率和离线对账差异控制在阈值内。
- 查询 P95 控制在秒级。

## 项目二：数据治理平台

### 背景

表越来越多，指标口径混乱，数据质量问题频繁，变更影响不可控。

### 架构

- 接入 Hive Metastore/Iceberg Catalog 获取元数据。
- 解析 SQL 和调度 DAG 生成血缘。
- 配置数据质量规则并接入调度。
- 建立权限、负责人、生命周期和成本看板。

### 难点

- 多引擎 SQL 解析。
- 字段级血缘准确性。
- 质量规则误报和漏报。
- 告警收敛和责任人定位。

## 面试回答结构

1. 业务背景和痛点。
2. 技术架构和组件选型。
3. 核心链路和数据流。
4. 你负责的模块。
5. 遇到的故障和优化。
6. 量化结果。
7. 复盘和后续改进。
""",
    ),
    (
        "大数据基础概念",
        "11-bigdata/fundamentals/basic-concepts.md",
        """# 大数据基础概念

如果你没有大数据基础，先把“大数据系统在解决什么问题”理解清楚。它不是单个数据库或单个框架，而是一整套处理海量数据的存储、计算、调度和治理体系。

## 为什么需要大数据系统

传统单机数据库适合在线交易和低延迟点查，但当数据量达到 TB/PB 级、查询需要扫描大量历史数据、计算需要跨多台机器并行时，就需要大数据系统。

典型问题包括：

- 数据太大，单机存不下。
- 查询太重，单库扛不住。
- 任务太慢，需要并行计算。
- 数据来源复杂，需要统一治理。
- 历史数据多，需要低成本存储。

## OLTP 与 OLAP

- OLTP：在线事务处理，例如下单、支付、库存扣减，关注低延迟、强一致、并发写。
- OLAP：在线分析处理，例如报表、留存、漏斗、画像，关注大扫描、聚合、多维分析。

后端开发常接触 MySQL/Redis 属于 OLTP 或在线服务体系；Hive、ClickHouse、Doris、Trino 更偏 OLAP。

## 离线与实时

- 离线：按小时、天批量处理，吞吐高，延迟高，适合历史报表和大规模重算。
- 实时：秒级或分钟级处理，延迟低，状态和一致性更复杂，适合监控、风控、实时看板。

## 存储与计算分离

现代大数据系统常把存储和计算解耦：数据放在 HDFS、对象存储或湖仓表中，计算由 Spark、Flink、Trino 等引擎完成。

优点：

- 多计算引擎共享同一份数据。
- 存储可独立扩容。
- 计算资源按需弹性使用。

挑战：

- 元数据一致性。
- 小文件治理。
- 权限和血缘统一。
- 多引擎读写兼容。

## 一条典型数据链路

1. 业务系统产生订单、支付、用户行为数据。
2. MySQL binlog 或日志采集进入 Kafka。
3. Flink 实时清洗、去重、聚合。
4. 原始和明细数据进入 HDFS/Iceberg/Hudi。
5. 汇总结果进入 Doris/ClickHouse。
6. BI、报表、风控、推荐系统消费结果。

## 后端开发需要掌握到什么程度

- 能理解数据链路和组件职责。
- 能讲清 HDFS、Hive、Spark、Flink、Kafka、ClickHouse 的定位。
- 能知道数据延迟、重复、丢失、倾斜、小文件如何处理。
- 能在项目中解释为什么选某个存储或计算引擎。

## 面试表达

大数据系统解决的是海量数据的低成本存储、批量/实时计算和统一治理问题。和在线系统相比，它更关注吞吐、可扩展、容错、数据一致性、任务调度和指标口径。
""",
    ),
    (
        "批处理与流处理",
        "11-bigdata/fundamentals/batch-vs-stream.md",
        """# 批处理与流处理

批处理和流处理是大数据计算的两种基本模式。理解它们的区别，是理解 Hive、Spark、Flink 的基础。

## 批处理

批处理把一段时间内的数据作为一个整体处理，例如每天凌晨计算昨天的订单报表。

特点：

- 数据边界清晰。
- 吞吐高。
- 延迟较高。
- 适合复杂历史计算和重跑。

常见技术：Hive、Spark Batch、MapReduce、Doris/ClickHouse 批量导入。

## 流处理

流处理把数据看作持续不断的事件流，来一条处理一条或按窗口聚合。

特点：

- 延迟低。
- 状态管理复杂。
- 需要处理乱序、迟到、重复。
- 需要 Checkpoint 和容错。

常见技术：Flink、Kafka Streams、Spark Structured Streaming。

## Mini-batch

Spark Streaming 早期模型是 mini-batch，即把短时间内的数据聚成小批次处理。它比纯批处理延迟低，但通常不如 Flink 这类原生流处理灵活。

## 流批一体

流批一体希望同一套 API 或引擎同时处理实时和离线数据。

实现方式包括：

- Flink 批流统一运行时。
- Spark Structured Streaming。
- Iceberg/Hudi/Delta Lake 提供统一表格式。

## 选择建议

- 报表 T+1：优先 Hive/Spark 离线。
- 实时大屏：Flink + Kafka + Doris/ClickHouse。
- 历史重算：Spark/Hive。
- 低延迟风控：Flink + Redis/HBase/在线服务。
- 临时分析：Trino/ClickHouse/Doris。

## 面试重点

批处理关注吞吐、成本和可重跑；流处理关注延迟、状态、一致性和乱序。两者不是替代关系，很多公司会同时保留离线链路和实时链路。
""",
    ),
    (
        "数据格式与压缩",
        "11-bigdata/fundamentals/file-format-compression.md",
        """# 数据格式与压缩

数据格式直接影响存储成本、查询性能、Schema 演进和多引擎兼容性。

## 行式与列式

行式存储把一行数据连续存放，适合写入和点查。

列式存储把同一列连续存放，适合分析查询。

OLAP 查询通常只读取少量列，因此列式格式能显著减少 IO。

## 常见格式

### Text/CSV

- 优点：可读性好，简单通用。
- 缺点：体积大，不支持类型，不适合高性能分析。

### JSON

- 优点：半结构化，适合日志和事件。
- 缺点：解析成本高，字段冗余，压缩和查询效率较低。

### Avro

- 行式二进制格式，支持 Schema 演进。
- 常用于 Kafka 消息、数据交换和 CDC。

### ORC

- 列式格式，Hive 生态常用。
- 支持压缩、索引、谓词下推和统计信息。

### Parquet

- 列式格式，Spark、Trino、Flink、Iceberg 常用。
- 生态通用性强，适合湖仓。

## 压缩算法

- Snappy：压缩比一般，但速度快，适合计算中间数据。
- Gzip：压缩比高，但不可切分，读取并行度差。
- LZO：可切分，速度较快，但需要额外索引。
- ZSTD：压缩比和速度平衡较好，现代系统常用。

## 选择建议

- Hive 离线数仓：ORC 或 Parquet。
- Spark/湖仓：Parquet 常见。
- Kafka 消息：Avro/JSON/Protobuf，配合 Schema Registry 更好。
- 临时导入：CSV/Text 可用，但不建议长期存储。

## 面试重点

列式格式快的原因是列裁剪、压缩率高、统计信息和谓词下推。压缩算法要在压缩比、CPU 成本和是否可切分之间取舍。
""",
    ),
    (
        "Hive 分区与分桶",
        "11-bigdata/hive/partition-bucket.md",
        """# Hive 分区与分桶

分区和分桶是 Hive 表设计中最基础也最常考的两个概念。

## 分区

分区本质是 HDFS 目录拆分，常见目录形态：`dt=2026-06-03/hour=10`。

优点：

- 查询时通过分区裁剪减少扫描数据。
- 便于按时间生命周期管理。
- 便于增量写入和重跑。

常见分区字段：日期、小时、地区、业务线。

## 分区设计误区

- 分区过粗：每次查询扫描过多数据。
- 分区过细：产生大量小文件和元数据压力。
- 查询不带分区条件：分区设计失效。
- 对分区字段使用函数：可能无法分区裁剪。

## 分桶

分桶是按字段 hash 后写入固定数量文件。

优点：

- 支持采样。
- 有利于 Bucket Join。
- 数据分布更可控。

## 分区与分桶区别

- 分区是目录级裁剪，减少扫描范围。
- 分桶是文件级组织，优化 Join、采样和数据分布。
- 分区字段通常是低基数时间/业务字段，分桶字段通常是 Join key 或高基数字段。

## 设计建议

- 大表按日期分区。
- 高频 Join key 可考虑分桶。
- 控制单分区文件数量和大小。
- 结合 ORC/Parquet 使用列式存储。

## 面试重点

分区解决“读哪些目录”，分桶解决“目录内数据如何组织”。分区裁剪是 Hive 查询优化最基础的手段。
""",
    ),
    (
        "Hive Metastore",
        "11-bigdata/hive/metastore.md",
        """# Hive Metastore

Hive Metastore 是 Hive 的元数据服务，保存库、表、字段、分区、存储位置、文件格式等信息。

## 保存什么

- Database 信息。
- Table 信息。
- Column 字段和类型。
- Partition 分区信息。
- StorageDescriptor：路径、格式、压缩、SerDe。
- 权限和统计信息。

## 为什么重要

计算引擎并不直接从 HDFS 目录猜测表结构，而是通过 Metastore 获取表元数据。

很多组件都会访问 Metastore：

- Hive
- Spark SQL
- Presto/Trino
- Flink SQL
- Impala

## 常见部署

- 元数据存储在 MySQL/PostgreSQL。
- Metastore Service 对外提供 Thrift 接口。
- 多计算引擎共享同一个 Metastore。

## 常见问题

- 分区太多导致 Metastore 查询慢。
- 元数据库连接池不足。
- 表结构变更未同步。
- 多引擎写元数据不一致。
- 权限和 Catalog 治理混乱。

## 与湖仓 Catalog

Iceberg/Hudi/Delta Lake 通常也需要 Catalog 管理表元数据。Hive Metastore 可以作为 Iceberg Catalog 的一种实现，但现代架构也会使用 REST Catalog、Glue、Nessie 等。

## 面试重点

Metastore 是数据湖/数仓的“表目录”。没有它，计算引擎很难知道数据在哪里、字段是什么、分区有哪些。
""",
    ),
    (
        "Spark RDD/DataFrame/Dataset",
        "11-bigdata/spark/rdd-dataframe-dataset.md",
        """# Spark RDD/DataFrame/Dataset

RDD、DataFrame、Dataset 是 Spark 的三个核心抽象。

## RDD

RDD 是弹性分布式数据集，代表分布在集群中的不可变数据集合。

特点：

- 强类型。
- API 底层，控制力强。
- 支持 lineage 容错。
- 优化器能力弱。

适合：自定义复杂计算、非结构化数据处理、需要底层控制的场景。

## DataFrame

DataFrame 是带 schema 的分布式表。

特点：

- 类似关系型表。
- 支持 Catalyst 优化。
- 支持 Tungsten 执行优化。
- API 更接近 SQL。

适合：结构化 ETL、SQL 分析、数仓计算。

## Dataset

Dataset 在 JVM 语言中提供类型安全，同时具备结构化优化能力。

特点：

- 类型安全。
- 支持编译期检查。
- 相比 DataFrame 编码和对象转换成本可能更高。

## Catalyst 优化器

Catalyst 会进行：

- 解析 SQL。
- 生成逻辑计划。
- 规则优化。
- 成本优化。
- 生成物理计划。

## 选择建议

- 优先使用 Spark SQL/DataFrame。
- 只有在需要底层控制时使用 RDD。
- Dataset 根据团队语言和类型安全需求选择。

## 面试重点

RDD 更底层，DataFrame/Dataset 更结构化且可被优化器优化。Spark SQL 性能通常更好，是因为 Catalyst 和 Tungsten 可以做执行计划和内存布局优化。
""",
    ),
    (
        "Spark 内存与 OOM",
        "11-bigdata/spark/memory-oom.md",
        """# Spark 内存与 OOM

Spark OOM 是生产中高频问题，通常与数据倾斜、缓存过大、Shuffle、并发任务数和对象膨胀有关。

## 内存区域

- Execution Memory：Shuffle、Join、Sort、Aggregation 使用。
- Storage Memory：Cache/Persist 使用。
- User Memory：用户对象、UDF、数据结构。
- Reserved Memory：系统保留。

## 常见 OOM 场景

- 单个分区数据过大。
- groupByKey 拉取全量 value。
- collect 把大数据拉回 Driver。
- 广播表过大。
- cache 大表且未释放。
- UDF 创建大量对象。
- 数据倾斜导致少数 Task 内存爆掉。

## Driver OOM

常见原因：

- collect/toPandas 大量数据。
- 任务元数据过多。
- 分区数或文件数过多。
- 广播变量过大。

## Executor OOM

常见原因：

- Shuffle 分区过大。
- Join/Aggregation 内存不足。
- 缓存过多。
- 数据倾斜。

## 排查步骤

1. 看 Spark UI 失败 Task 和 Stage。
2. 看是否集中在少数 Task。
3. 看 Shuffle Read/Write 和输入记录数。
4. 看 Driver/Executor 日志。
5. 检查 collect、cache、join、groupByKey 等高危操作。

## 优化方式

- 增加分区数，降低单分区大小。
- 使用 reduceByKey 替代 groupByKey。
- 开启 AQE 和 skew join。
- 小表广播，大表避免全量 shuffle。
- 控制 cache，并及时 unpersist。
- 避免 collect 大数据。

## 面试重点

Spark OOM 不应只回答“加内存”。正确思路是判断 Driver 还是 Executor，定位具体 Stage 和 Task，再结合分区大小、Shuffle、Join、缓存和数据倾斜处理。
""",
    ),
    (
        "Flink Window 与 Watermark",
        "11-bigdata/flink/window-watermark.md",
        """# Flink Window 与 Watermark

Window 和 Watermark 是 Flink 处理无界流的核心机制。

## 为什么需要 Window

流是无界的，不能等所有数据到齐后再计算。Window 用来把无界流切成有限范围，例如每 5 分钟统计一次 PV。

## Window 类型

- Tumbling Window：滚动窗口，固定长度，不重叠。
- Sliding Window：滑动窗口，固定长度，按步长滑动，窗口可重叠。
- Session Window：会话窗口，根据事件间隔动态切分。
- Global Window：全局窗口，需要自定义触发器。

## 时间语义

- Processing Time：机器处理时间，实现简单但结果不稳定。
- Event Time：事件发生时间，适合乱序数据。
- Ingestion Time：进入 Flink 的时间。

## Watermark

Watermark 是事件时间进度的标记，表示系统认为早于该时间的数据基本都到了。

例如 Watermark = 10:00:00，表示 10:00:00 之前的数据大概率已经到齐，可以触发窗口计算。

## 乱序与迟到

- 乱序：事件到达顺序和发生顺序不一致。
- 迟到：事件到达时，对应窗口已经触发。
- Allowed Lateness：允许窗口关闭后一段时间继续接收迟到数据。
- Side Output：严重迟到数据输出到侧流。

## 常见问题

- Watermark 推进太慢：窗口迟迟不触发。
- Watermark 推进太快：迟到数据被丢弃。
- 某些分区无数据：可能拖慢整体 Watermark。

## 面试重点

Watermark 不是当前最大事件时间，而是“当前最大事件时间减去允许乱序时间”。它是在准确性和延迟之间做权衡。
""",
    ),
    (
        "Flink State Backend",
        "11-bigdata/flink/state-backend.md",
        """# Flink State Backend

State Backend 决定 Flink 状态如何存储、访问和做 Checkpoint。

## 为什么需要状态

很多流计算不是单条事件独立处理，而是需要记住历史：

- 去重。
- 窗口聚合。
- Join。
- 规则匹配。
- 用户会话。

## 状态类型

- ValueState：保存单个值。
- ListState：保存列表。
- MapState：保存 Map。
- ReducingState/AggregatingState：保存聚合结果。
- BroadcastState：广播配置或规则。

## Backend 类型

### HashMapStateBackend

- 状态存储在 JVM 堆内。
- 访问速度快。
- 适合小状态和低延迟任务。
- 大状态容易 GC 压力大。

### EmbeddedRocksDBStateBackend

- 状态存储在 RocksDB。
- 支持大状态。
- 读写需要序列化和本地磁盘 IO。
- 调优复杂度更高。

## TTL

状态 TTL 用于清理长期不用的状态，避免状态无限增长。

注意：TTL 清理不一定实时发生，具体取决于访问、快照和后台清理策略。

## 常见问题

- 状态过大导致 Checkpoint 慢。
- RocksDB 写放大导致磁盘 IO 高。
- TTL 设置不合理导致状态泄漏或结果不准确。
- 状态序列化变更导致恢复失败。

## 面试重点

小状态、低延迟优先 HashMap；大状态优先 RocksDB。状态设计要关注 key 粒度、TTL、序列化兼容和 Checkpoint 成本。
""",
    ),
    (
        "HBase Compaction 与 Region",
        "11-bigdata/hbase/compaction-region.md",
        """# HBase Compaction 与 Region

HBase 的性能和稳定性很大程度取决于 Region 分布、MemStore flush、HFile 数量和 Compaction。

## Region

Region 是 HBase 表按 RowKey 范围切分后的分片。

- 一个表由多个 Region 组成。
- Region 分布在多个 RegionServer 上。
- Region 过大时会 split。
- Region 分布不均会导致热点。

## Flush

写入先进入 MemStore 和 WAL。当 MemStore 达到阈值时，会 flush 成 HFile。

Flush 太频繁会产生大量小 HFile，增加 Compaction 压力。

## Compaction

Compaction 是合并 HFile 的后台过程。

- Minor Compaction：合并少量小 HFile。
- Major Compaction：合并一个 Store 下所有 HFile，并清理删除标记和过期版本。

## Compaction 影响

- 降低读放大。
- 清理删除和过期数据。
- 但会消耗 CPU、磁盘 IO 和网络资源。
- Major Compaction 过重可能影响线上读写。

## 热点问题

原因：

- RowKey 单调递增。
- 热点用户或热点设备集中写入。
- Region 未预分区。

解决：

- 预分区。
- RowKey 加 salt/hash。
- 热点 key 拆分。
- 调整 Region 大小和 split 策略。

## 面试重点

HBase 写入快是因为先写 WAL 和 MemStore，但后台 flush 和 compaction 如果治理不好，会转化为读放大、写放大和 IO 抖动。
""",
    ),
    (
        "ClickHouse 查询优化",
        "11-bigdata/clickhouse/query-optimization.md",
        """# ClickHouse 查询优化

ClickHouse 查询优化要围绕“少读数据、少做计算、并行执行、提前聚合”展开。

## 表设计

- 分区键用于裁剪数据范围，常用日期分区。
- ORDER BY 决定物理排序和稀疏索引效果。
- 高频过滤字段应尽量靠前。
- 避免分区过细导致 part 数量过多。

## 查询写法

- 必须带时间范围或分区条件。
- 避免 `select *`。
- 避免对过滤字段使用复杂函数。
- 高基数字段 group by 要谨慎。
- Join 前尽量过滤和裁剪列。

## 数据跳过索引

适合在某些字段分布具备局部性的情况下减少扫描。

常见类型：

- minmax。
- set。
- bloom_filter。
- tokenbf_v1。

## 物化视图

物化视图可以在写入时预计算聚合结果，适合固定报表和高频指标。

注意：

- 会增加写入成本。
- 口径变更需要重建。
- 明细和聚合结果一致性要关注。

## 常见慢查询原因

- 分区未裁剪。
- ORDER BY 设计不匹配查询。
- 扫描列太多。
- 小 part 过多。
- 大 Join 或高基数聚合。
- 后台 merge 压力大。

## 面试重点

ClickHouse 优化不是简单加索引，而是表模型、分区、排序键、列裁剪、预聚合和写入批次共同设计。
""",
    ),
    (
        "数据采集与日志链路",
        "11-bigdata/data-pipeline/log-collection.md",
        """# 数据采集与日志链路

日志采集是大数据链路的入口，常用于用户行为分析、系统监控、搜索推荐和风控。

## 常见来源

- 前端埋点。
- App 埋点。
- 服务端业务日志。
- Nginx/网关访问日志。
- 系统指标和 Trace。

## 常见组件

- Filebeat：轻量日志采集。
- Flume：Hadoop 生态传统日志采集。
- Logstash：日志解析和处理能力强。
- Kafka：日志缓冲和解耦。
- Flink/Spark：实时或离线清洗。

## 链路示例

1. 应用输出 JSON 日志到本地文件。
2. Filebeat 采集日志发送到 Kafka。
3. Flink 消费 Kafka 做解析、过滤、补充字段。
4. 明细写入 HDFS/Iceberg，聚合写入 ClickHouse/Doris。
5. 质量任务检查延迟、丢失和字段合法性。

## 关键问题

- 日志格式统一。
- traceId/requestId 贯穿链路。
- 采集端限速和重试。
- Kafka Topic 和分区设计。
- 脏数据进入侧输出。
- 数据延迟和丢失监控。

## 面试重点

日志采集要保证可重放、可追踪、可治理。Kafka 在链路中通常承担缓冲、削峰、解耦和故障恢复作用。
""",
    ),
    (
        "数据同步工具",
        "11-bigdata/data-pipeline/sync-tools.md",
        """# 数据同步工具

数据同步负责把业务库、日志、文件、消息队列中的数据同步到数仓、湖仓或分析数据库。

## 常见方式

- 全量同步：定期完整导入。
- 增量同步：按更新时间、ID 或日志位点同步。
- CDC：基于数据库日志捕获变更。
- 批流一体同步：全量 + 增量无缝衔接。

## 常见工具

- DataX：离线批量同步工具，常用于 MySQL 到 Hive/ClickHouse。
- Sqoop：Hadoop 生态老牌关系库同步工具。
- Canal：解析 MySQL binlog，常用于缓存更新或数据同步。
- Debezium：CDC 平台，支持多种数据库。
- Flink CDC：全量和增量一体化接入 Flink。

## 同步难点

- 全量和增量切换一致性。
- 删除事件同步。
- DDL 变更。
- 脏数据处理。
- 断点续传。
- 幂等写入。
- 源库压力控制。

## 设计建议

- 同步链路要有唯一业务主键。
- 下游写入要支持幂等。
- 记录同步位点和批次号。
- 建立延迟和失败告警。
- 对大表做分片和限速。

## 面试重点

数据同步不能只说“定时抽数”。生产链路要考虑一致性、位点、DDL、删除、重试、源库压力和下游幂等。
""",
    ),
    (
        "指标体系与口径治理",
        "11-bigdata/data-warehouse/metrics.md",
        """# 指标体系与口径治理

指标体系用于统一业务分析语言，避免不同团队对同一指标算出不同结果。

## 指标分类

- 原子指标：不可再拆的基础度量，例如支付金额、订单数。
- 派生指标：原子指标 + 统计周期 + 维度 + 修饰词，例如最近 7 天新用户支付金额。
- 复合指标：由多个指标计算得到，例如转化率、客单价。

## 指标组成

- 业务过程：下单、支付、退款、发货。
- 度量：金额、次数、人数、时长。
- 维度：时间、地区、渠道、商品、用户。
- 统计周期：日、周、月、实时窗口。
- 过滤条件：成功订单、有效用户、剔除测试数据。

## 口径治理

- 明确定义指标负责人。
- 指标公式统一沉淀。
- 指标和数据表血缘关联。
- 指标变更有审批和版本。
- 核心指标做一致性校验。

## 常见问题

- “订单数”是否包含取消订单。
- “GMV”是否包含退款。
- “活跃用户”按登录、访问还是行为计算。
- 实时和离线指标窗口不一致。
- 测试数据或机器人流量未剔除。

## 面试重点

数仓价值不只是产出表，更重要是统一业务指标口径。指标治理要结合元数据、血缘、质量和权限一起建设。
""",
    ),
    (
        "维度建模与拉链表",
        "11-bigdata/data-warehouse/dimensional-modeling.md",
        """# 维度建模与拉链表

维度建模是数仓建模的核心方法，用事实表记录业务过程，用维度表描述分析视角。

## 事实表

事实表记录可度量的业务事件。

常见类型：

- 事务事实表：一笔订单、一笔支付。
- 周期快照事实表：每天账户余额、库存快照。
- 累积快照事实表：订单从创建到完成的生命周期。

## 维度表

维度表描述业务实体，例如用户、商品、门店、地区。

维度字段用于 group by、where 和报表筛选。

## 星型与雪花

- 星型模型：事实表直接关联多个维表，查询简单，冗余较多。
- 雪花模型：维度继续拆分，冗余少，但查询复杂。

## 缓慢变化维

维度属性会变化，例如用户等级、商品类目、门店状态。

处理方式：

- Type 1：直接覆盖，不保留历史。
- Type 2：新增一条版本记录，保留历史。
- Type 3：增加字段保存前一个状态。

## 拉链表

拉链表通过开始时间和结束时间保存历史版本。

常见字段：

- business_id
- start_date
- end_date
- is_current
- version

## 面试重点

拉链表适合保存维度历史变化，能回答“某个历史时间点用户/商品是什么状态”。代价是查询和维护复杂度更高。
""",
    ),
    (
        "湖仓选型对比",
        "11-bigdata/lakehouse/table-format-comparison.md",
        """# 湖仓选型对比

湖仓表格式用于让 HDFS/对象存储上的文件具备表管理、事务、快照和多引擎访问能力。

## Iceberg

优势：

- 表格式开放，设计清晰。
- 多引擎兼容好。
- Snapshot、Schema Evolution、Partition Evolution 能力强。
- 隐藏分区降低使用复杂度。

适合：多引擎数据湖、长期数据资产、复杂表演进。

## Hudi

优势：

- Upsert 能力强。
- 增量查询成熟。
- 适合 CDC 入湖。
- 表服务能力丰富。

适合：近实时入湖、更新删除多、增量消费链路。

## Delta Lake

优势：

- Databricks/Spark 生态强。
- ACID、Schema Enforcement、Time Travel 成熟。
- 与 Spark 集成体验好。

适合：Databricks 生态或 Spark 为主的数据湖。

## 选型维度

- 是否高频 upsert。
- 是否需要多引擎读写。
- 是否需要增量消费。
- 是否依赖 Spark/Trino/Flink。
- Catalog 和权限生态。
- 团队运维经验。

## 面试重点

湖仓表格式解决的是文件湖缺少事务、元数据、快照、演进和多引擎一致性的问题。Iceberg、Hudi、Delta Lake 的差异主要在 upsert、增量、开放性和生态集成。
""",
    ),
    (
        "大数据线上排障手册",
        "11-bigdata/operations/troubleshooting.md",
        """# 大数据线上排障手册

大数据排障要从数据链路、任务运行、资源、存储和质量五个层面定位。

## 数据延迟

可能原因：

- Kafka 积压。
- Flink 反压。
- Checkpoint 超时。
- 下游 Sink 写入慢。
- 调度资源不足。

排查：

- 看 Kafka consumer lag。
- 看 Flink backpressure 和 busy time。
- 看 Checkpoint duration。
- 看下游写入 QPS 和错误。

## 任务失败

可能原因：

- 数据格式异常。
- Schema 变更。
- 权限不足。
- 资源不足。
- 外部系统不可用。

排查：

- 先看第一条异常，而不是最后的失败汇总。
- 对比最近发布和上游变更。
- 检查失败是否集中在某个分区或字段。

## 指标异常

可能原因：

- 上游数据缺失。
- 去重逻辑变化。
- 维表未更新。
- 时间窗口不一致。
- 口径变更未同步。

排查：

- 从 ADS 反查 DWS、DWD、ODS。
- 对比离线和实时链路。
- 检查分区产出、行数、空值率和 TopN。

## 查询慢

可能原因：

- 未命中分区裁剪。
- 小文件过多。
- 数据倾斜。
- Join 策略错误。
- OLAP 表排序键不合理。

## 面试表达

线上排障我会先止血，再定位。止血包括降级、暂停下游、切离线结果、扩容；定位按链路从 Source、Kafka、Compute、Storage、Serving、Quality 逐层排查，最后复盘补监控和规则。
""",
    ),
    (
        "大数据学习路线",
        "11-bigdata/learning-path.md",
        """# 大数据学习路线

如果你没有大数据基础，建议按“概念 -> 存储 -> 计算 -> 数仓 -> 实时 -> OLAP -> 治理 -> 项目”学习。

## 第一阶段：建立概念

- OLTP 与 OLAP。
- 离线与实时。
- 批处理与流处理。
- 存储与计算分离。
- 数据湖、数仓、湖仓。

建议阅读：

- [大数据基础概念](fundamentals/basic-concepts.md)
- [批处理与流处理](fundamentals/batch-vs-stream.md)

## 第二阶段：Hadoop 基础

- HDFS 架构和读写流程。
- YARN 资源调度。
- MapReduce Shuffle。

建议阅读：

- [HDFS](hadoop/hdfs.md)
- [YARN](hadoop/yarn.md)
- [MapReduce](hadoop/mapreduce.md)

## 第三阶段：Hive 和数仓

- Hive 架构。
- 分区分桶。
- SQL 优化。
- ODS/DWD/DWS/ADS。
- 指标口径。

## 第四阶段：Spark 和 Flink

- Spark Shuffle、内存、SQL 优化。
- Flink Window、Watermark、State、Checkpoint、Exactly Once。

## 第五阶段：查询与服务

- ClickHouse/Doris。
- HBase。
- Trino。

## 第六阶段：治理和项目

- 调度系统。
- 元数据血缘。
- 数据质量。
- 权限安全。
- 成本治理。
- 项目面试表达。

## 找工作建议

Java 后端不需要一开始掌握所有大数据组件，但要能讲清一条完整链路：数据从哪里来，如何进入 Kafka，如何用 Flink/Spark 处理，如何进入湖仓或 OLAP，如何保证质量、延迟和一致性。
""",
    ),
]


JAVA_VERSION_DOCS = [
    (
        "Java 版本新特性总览",
        "01-java/java-version-features/README.md",
        """# Java 版本新特性总览

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
""",
    ),
    (
        "Java 8 新特性",
        "01-java/java-version-features/java-8.md",
        """# Java 8 新特性

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
""",
    ),
    (
        "Java 9-11 新特性",
        "01-java/java-version-features/java-9-11.md",
        """# Java 9-11 新特性

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
""",
    ),
    (
        "Java 12-17 新特性",
        "01-java/java-version-features/java-12-17.md",
        """# Java 12-17 新特性

Java 12 到 Java 17 引入了很多现代语法能力。Java 17 是 LTS，也是 Spring Boot 3 和 Spring Framework 6 的最低 Java 版本要求。

## Switch 表达式

Java 14 标准化 Switch 表达式。

```java
String type = switch (status) {
    case 1 -> "NEW";
    case 2 -> "PAID";
    case 3 -> "CLOSED";
    default -> "UNKNOWN";
};
```

优势：

- 可以作为表达式返回值。
- 避免传统 switch 忘记 `break` 的问题。
- 语义更清晰。

## Text Blocks 文本块

Java 15 标准化文本块。

```java
String sql = \"\"\"
    select id, name
    from user
    where status = 'ACTIVE'
    \"\"\";
```

适合：

- SQL。
- JSON。
- HTML。
- 多行模板。

## Record

Java 16 标准化 Record。

```java
public record UserDTO(Long id, String name) {}
```

自动生成：

- 构造方法。
- accessor。
- `equals`
- `hashCode`
- `toString`

适合：

- DTO。
- 值对象。
- 查询结果投影。
- 不可变数据载体。

不适合：

- JPA Entity 这类需要无参构造、延迟加载和可变状态的对象。

## instanceof 模式匹配

Java 16 标准化 instanceof 模式匹配。

```java
if (obj instanceof String s) {
    System.out.println(s.length());
}
```

优势：

- 减少强制类型转换。
- 降低样板代码。

## Sealed Classes

Java 17 标准化密封类。

```java
public sealed interface PayCommand permits CreatePay, CancelPay {}
public final class CreatePay implements PayCommand {}
public final class CancelPay implements PayCommand {}
```

作用：

- 限制继承层级。
- 让编译器知道所有可能子类型。
- 适合领域模型、状态机、指令类型建模。

## Java 17 LTS 意义

Java 17 是重要长期支持版本。

对后端影响：

- Spring Boot 3 要求 Java 17+。
- 很多中间件和框架开始以 Java 17 为新基线。
- G1、ZGC 等 JVM 能力更成熟。
- 现代语法提升 DTO、状态模型和配置代码可读性。

## 面试回答模板

Java 12 到 17 的重点是现代语法和 Java 17 LTS。Switch 表达式、文本块、Record、instanceof 模式匹配、Sealed Classes 都在减少样板代码并增强建模能力。Java 17 也是 Spring Boot 3 的基础版本，升级时要关注依赖兼容和 Jakarta 迁移。
""",
    ),
    (
        "Java 18-21 新特性",
        "01-java/java-version-features/java-18-21.md",
        """# Java 18-21 新特性

Java 18 到 Java 21 的重点是虚拟线程、模式匹配增强、Record Pattern、Sequenced Collections 和新一代并发编程模型。Java 21 是 LTS。

## Java 21：虚拟线程 Virtual Threads

虚拟线程是 Java 21 最重要的服务端特性之一，来自 Project Loom。

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 1000).forEach(i -> executor.submit(() -> callRemote(i)));
}
```

### 解决什么问题

传统平台线程与操作系统线程一一对应，数量昂贵。大量阻塞 IO 会占用大量线程资源。

虚拟线程由 JVM 调度，创建和切换成本低，适合大量阻塞 IO 任务。

### 适合场景

- HTTP/RPC 阻塞调用。
- 数据库访问。
- 文件/网络 IO。
- 高并发但大部分时间在等待外部系统的业务接口。

### 不适合场景

- CPU 密集型任务。
- 需要严格限制下游并发的场景，仍然需要连接池、限流和舱壁隔离。
- 长时间持有 synchronized 或 native 阻塞导致 pinning 的场景需要关注。

### 面试重点

虚拟线程提升的是阻塞 IO 场景的并发承载能力，不会让 CPU 计算变快，也不能替代限流、连接池和超时控制。

## 结构化并发 Structured Concurrency

结构化并发用于把一组相关并发任务作为一个整体管理，便于取消、异常传播和生命周期控制。

它仍处于预览/孵化阶段，需要关注具体 JDK 版本状态。

## Scoped Values

Scoped Values 用于在线程调用链中安全传递上下文，被视为 ThreadLocal 的现代替代方向之一。

优势：

- 不易泄漏。
- 适合虚拟线程。
- 作用域明确。

## Pattern Matching for switch

Java 21 标准化 switch 模式匹配。

```java
String text = switch (obj) {
    case Integer i -> "int: " + i;
    case String s -> "str: " + s;
    case null -> "null";
    default -> "unknown";
};
```

价值：

- 按类型分支更清晰。
- 与 sealed class 搭配可做穷尽性检查。
- 适合领域模型和状态机分发。

## Record Patterns

Java 21 标准化 Record Patterns。

```java
record Point(int x, int y) {}

if (obj instanceof Point(int x, int y)) {
    System.out.println(x + y);
}
```

价值：

- 解构 record。
- 与模式匹配组合，减少样板代码。

## Sequenced Collections

Java 21 引入有序集合统一接口。

核心接口：

- `SequencedCollection`
- `SequencedSet`
- `SequencedMap`

常用能力：

- 获取第一个元素。
- 获取最后一个元素。
- 反向视图。

## Java 21 LTS 意义

Java 21 是继 Java 17 后的新 LTS。

对后端影响：

- 虚拟线程可能改变传统“一请求一线程”的成本模型。
- 现代模式匹配能力增强领域建模表达力。
- Spring Boot 3.2+ 已开始支持虚拟线程相关配置。

## 面试回答模板

Java 21 最值得关注的是虚拟线程，它让阻塞 IO 场景能以更低线程成本承载高并发；但它不是性能银弹，CPU 密集型任务、连接池容量、限流和超时仍然要治理。同时 Java 21 的模式匹配、Record Patterns、Sequenced Collections 提升了代码表达力。
""",
    ),
    (
        "LTS 版本选型与升级",
        "01-java/java-version-features/lts-upgrade.md",
        """# LTS 版本选型与升级

Java 后端项目常见 LTS 版本是 Java 8、11、17、21。找工作时不只要知道新特性，还要理解版本选型和升级风险。

## LTS 版本对比

### Java 8

优势：

- 存量系统最多。
- 生态兼容性好。
- Lambda、Stream、CompletableFuture 已足够现代化。

问题：

- 版本较老。
- 新框架逐步不再支持。
- JVM 和 GC 新能力不足。

### Java 11

优势：

- LTS。
- 从 Java 8 升级成本相对可控。
- HTTP Client、String API、容器感知等能力增强。

问题：

- 相比 Java 17，现代语言特性少。

### Java 17

优势：

- LTS。
- Spring Boot 3/Spring 6 基线。
- Record、Sealed Classes、Pattern Matching 等能力成熟。
- JVM 性能和 GC 能力更好。

问题：

- 从 Java 8 升级跨度大，需要处理依赖、反射、模块封装、Jakarta 迁移等问题。",

### Java 21

优势：

- LTS。
- 虚拟线程正式可用。
- 现代模式匹配能力增强。
- 适合新项目和高并发 IO 服务探索。

问题：

- 部分企业生态仍在验证中。
- 老中间件、Agent、监控工具需要确认兼容性。

## Java 8 升级到 Java 17 常见问题

- 依赖库版本过旧。
- 非法反射访问失败或告警。
- JAXB/JAX-WS 等 Java EE 模块被移除，需要显式依赖。
- Spring Boot 2 到 3 涉及 `javax.*` 到 `jakarta.*` 迁移。
- Lombok、Mockito、ByteBuddy、ASM 等字节码工具需要升级。
- GC 参数变化，部分旧参数废弃。

## 升级步骤建议

1. 梳理当前 JDK、框架、中间件、构建插件和 Agent 版本。
2. 先升级依赖到支持目标 JDK 的版本。
3. 本地编译和单元测试。
4. 处理非法反射、废弃 API 和模块缺失。
5. 压测关键接口，比较 GC、RT、CPU、内存。
6. 灰度发布，观察错误率、延迟和资源指标。
7. 完成回滚预案。

## 版本选型建议

- 存量保守系统：Java 8 或 Java 11，优先稳定。
- 新 Spring Boot 项目：Java 17 起步。
- 高并发 IO 新服务：可评估 Java 21 虚拟线程。
- 中间件/基础设施项目：根据生态兼容性选择 17 或 21。

## 面试表达

如果被问“为什么升级 Java 17/21”，不要只说新特性。要从 LTS 支持、框架基线、性能、GC、语言表达力、安全更新和生态兼容性回答，并说明升级前要做依赖扫描、兼容性测试、压测和灰度。
""",
    ),
]


SPRING_BOOT_VERSION_DOCS = [
    (
        "Spring Boot 版本新特性总览",
        "06-framework/spring-boot-version-features/README.md",
        """# Spring Boot 版本新特性总览

本目录整理 Spring Boot 1.x、2.x、3.x 的关键变化，重点服务后端面试、项目升级和技术选型。

## 为什么要单独整理版本特性

- Spring Boot 1.x 是早期自动配置和 Starter 体系的成型阶段，很多老系统仍能看到它的影子。
- Spring Boot 2.x 是企业存量项目最常见版本线，包含 WebFlux、Actuator 2、Micrometer、配置机制变化等重要内容。
- Spring Boot 3.x 基于 Spring Framework 6 和 Java 17，涉及 Jakarta EE 迁移、AOT、Native Image、Observability 等重大变化。

## 阅读顺序

1. [Spring Boot 1.x 到 2.x](spring-boot-1-to-2.md)
2. [Spring Boot 2.0 到 2.3](spring-boot-2-0-to-2-3.md)
3. [Spring Boot 2.4 到 2.7](spring-boot-2-4-to-2-7.md)
4. [Spring Boot 3.x](spring-boot-3.md)
5. [版本升级路线](upgrade-guide.md)

## 面试重点

- Spring Boot 的核心价值：自动配置、Starter、外部化配置、Actuator、内嵌容器。
- Spring Boot 2.x：响应式 WebFlux、Micrometer、Actuator 端点模型变化、配置加载机制调整。
- Spring Boot 2.4：`ConfigData` 配置加载机制，引入 `spring.config.import`。
- Spring Boot 2.6：默认禁止循环依赖，路径匹配策略变化。
- Spring Boot 3.x：Java 17、Spring 6、Jakarta EE、AOT、GraalVM Native Image、Observability。

## 找工作建议

- 存量项目面试：重点准备 Spring Boot 2.x、自动配置原理、Actuator、配置加载、循环依赖变化。
- 新项目面试：重点准备 Spring Boot 3.x、Java 17、Jakarta 迁移、Micrometer Tracing、AOT/Native。
- 如果简历写过升级项目，要能讲清依赖兼容、配置变更、自动配置差异、压测和灰度方案。
""",
    ),
    (
        "Spring Boot 1.x 到 2.x",
        "06-framework/spring-boot-version-features/spring-boot-1-to-2.md",
        """# Spring Boot 1.x 到 2.x

Spring Boot 2.0 是一次重要版本升级，底层升级到 Spring Framework 5，引入响应式编程支持，并重构了 Actuator 和监控体系。

## 基线变化

- Spring Boot 1.x 基于 Spring Framework 4.x。
- Spring Boot 2.0 基于 Spring Framework 5.x。
- Java 基线从 Java 7/8 时代逐步转向 Java 8+。

## WebFlux

Spring Boot 2.0 引入对 Spring WebFlux 的自动配置支持。

WebFlux 特点：

- 基于 Reactor。
- 支持非阻塞响应式编程模型。
- 可运行在 Netty、Servlet 3.1+ 容器上。

适合场景：

- 高并发 IO。
- 流式响应。
- API Gateway。

不适合场景：

- 传统阻塞 JDBC 调用较多的业务系统。
- 团队不熟悉响应式链路和调试方式。

## Actuator 2 重构

Spring Boot 2 对 Actuator 做了较大调整：

- endpoint 路径从 `/metrics` 等变化为 `/actuator/metrics` 等。
- 暴露端点需要显式配置。
- Endpoint 注解模型变化。
- 安全配置方式变化。

常用配置：

```properties
management.endpoints.web.exposure.include=health,info,metrics,prometheus
```

## Micrometer

Spring Boot 2 引入 Micrometer 作为指标门面。

它的定位类似日志中的 SLF4J：

- 应用使用统一指标 API。
- 后端可接 Prometheus、Datadog、Graphite、InfluxDB 等。

## 配置属性绑定变化

Spring Boot 2 增强了 Binder 机制和类型安全配置绑定。

常用方式：

```java
@ConfigurationProperties(prefix = "app")
public class AppProperties {
    private String name;
}
```

## 迁移注意事项

- Actuator endpoint 路径和暴露配置变化。
- Spring Security 配置方式变化。
- 部分自动配置属性名变化。
- 第三方 Starter 需要确认是否兼容 Boot 2。
- 响应式和 Servlet 栈不要混用到难以维护。

## 面试回答模板

Spring Boot 2 相比 1.x 的核心变化是升级到 Spring 5，引入 WebFlux 响应式支持，Actuator 端点模型重构，并引入 Micrometer 作为统一指标门面。升级时要重点检查 Actuator 路径、安全配置、配置属性和第三方 Starter 兼容性。
""",
    ),
    (
        "Spring Boot 2.0 到 2.3",
        "06-framework/spring-boot-version-features/spring-boot-2-0-to-2-3.md",
        """# Spring Boot 2.0 到 2.3

Spring Boot 2.0 到 2.3 主要围绕响应式体系、可观测性、容器化和优雅停机增强。

## Spring Boot 2.1

重点变化：

- 支持 Java 11。
- 改进应用启动性能和自动配置报告。
- Bean 覆盖默认被禁用，避免无意覆盖同名 Bean。

相关配置：

```properties
spring.main.allow-bean-definition-overriding=true
```

实践意义：

- 老项目中如果存在同名 Bean，升级后可能启动失败。
- 需要通过重命名、条件装配或显式允许覆盖解决。

## Spring Boot 2.2

重点变化：

- 支持 Java 13。
- 延迟初始化支持。
- Actuator 和 Micrometer 持续增强。

延迟初始化：

```properties
spring.main.lazy-initialization=true
```

优点：

- 减少启动时间。
- 开发和测试环境更轻量。

风险：

- 部分 Bean 初始化错误会延迟到运行期暴露。
- 首次请求可能变慢。

## Spring Boot 2.3

重点变化：

- 支持构建 OCI 镜像。
- 引入 graceful shutdown 优雅停机。
- 健康检查增强，支持 Kubernetes probes。

优雅停机：

```properties
server.shutdown=graceful
spring.lifecycle.timeout-per-shutdown-phase=30s
```

Kubernetes 探针：

```properties
management.endpoint.health.probes.enabled=true
```

## 容器化支持

Spring Boot 2.3 开始强化云原生部署体验：

- Buildpacks 构建镜像。
- 分层 jar，提升 Docker 镜像缓存效率。
- readiness/liveness 健康检查。

## 面试重点

Spring Boot 2.0 到 2.3 的变化重点是：Bean 覆盖保护、延迟初始化、Micrometer 增强、优雅停机、Kubernetes 探针和容器镜像构建支持。这些变化体现了 Spring Boot 从单体快速开发走向云原生运行治理。
""",
    ),
    (
        "Spring Boot 2.4 到 2.7",
        "06-framework/spring-boot-version-features/spring-boot-2-4-to-2-7.md",
        """# Spring Boot 2.4 到 2.7

Spring Boot 2.4 到 2.7 是从 2.x 走向 3.x 的过渡阶段，配置加载机制、循环依赖、路径匹配和安全配置都有重要变化。

## Spring Boot 2.4：ConfigData

Spring Boot 2.4 引入新的配置加载机制 `ConfigData`。

核心变化：

- 支持 `spring.config.import`。
- 更清晰地处理 profile 配置。
- 对配置文件加载顺序做了调整。

示例：

```properties
spring.config.import=optional:nacos:example.yaml
```

升级风险：

- 老项目依赖旧的 profile 激活方式时，配置加载顺序可能变化。
- Spring Cloud 配置中心需要匹配对应版本。

## Spring Boot 2.5

重点变化：

- SQL 初始化配置调整。
- Docker 镜像构建增强。
- Actuator 和 metrics 持续增强。

SQL 初始化相关配置从早期 `spring.datasource.initialization-mode` 逐步迁移到：

```properties
spring.sql.init.mode=always
```

## Spring Boot 2.6：循环依赖默认禁用

Spring Boot 2.6 默认不允许 Bean 循环依赖。

如果存在循环依赖，可能启动失败。

临时兼容配置：

```properties
spring.main.allow-circular-references=true
```

实践建议：

- 不建议长期依赖该开关。
- 应通过拆分职责、事件、懒加载或重构依赖方向解决。

## Spring Boot 2.6：路径匹配策略变化

Spring MVC 默认路径匹配从 `AntPathMatcher` 转向 `PathPatternParser`。

可能影响：

- Swagger/Springfox 兼容问题。
- 部分路径匹配规则行为变化。

兼容配置：

```properties
spring.mvc.pathmatch.matching-strategy=ant_path_matcher
```

## Spring Boot 2.7

Spring Boot 2.7 是 2.x 到 3.x 的过渡版本。

重点：

- 提前适配部分 3.x 迁移路径。
- Spring Security 新配置方式更常见。
- 建议用它作为升级到 3.x 前的中间版本。

## 面试重点

Spring Boot 2.4 到 2.7 最容易问的是配置加载机制变化、循环依赖默认禁用、路径匹配策略变化，以及 2.7 作为升级 3.x 的过渡版本。回答时要能结合真实升级问题说明风险和解决方案。
""",
    ),
    (
        "Spring Boot 3.x",
        "06-framework/spring-boot-version-features/spring-boot-3.md",
        """# Spring Boot 3.x

Spring Boot 3 是一次重大升级，基于 Spring Framework 6，要求 Java 17+，并迁移到 Jakarta EE 9+ 命名空间。

## 基线变化

- Java 17+。
- Spring Framework 6+。
- Jakarta EE 9+。
- GraalVM Native Image 支持增强。

## javax 到 jakarta 迁移

最重要的破坏性变化是包名迁移：

```java
import javax.servlet.http.HttpServletRequest;
```

变为：

```java
import jakarta.servlet.http.HttpServletRequest;
```

影响范围：

- Servlet API。
- JPA。
- Validation。
- JAXB。
- WebSocket。
- 第三方库和 Starter。

## AOT 与 Native Image

Spring Boot 3 强化 AOT 编译和 GraalVM Native Image 支持。

收益：

- 启动更快。
- 内存占用更低。
- 适合 Serverless、CLI、小型微服务。

限制：

- 反射、动态代理、资源加载需要元数据提示。
- 部分第三方库兼容性需要验证。
- 构建链路更复杂。

## Observability

Spring Boot 3 用 Micrometer Observation 统一指标、日志、Tracing 的观测模型。

相关组件：

- Micrometer Metrics。
- Micrometer Tracing。
- OpenTelemetry Bridge。
- Actuator。

迁移注意：

- Spring Cloud Sleuth 不再作为新版本主线。
- 新项目通常使用 Micrometer Tracing + OpenTelemetry。

## 自动配置机制变化

Spring Boot 3 使用新的自动配置声明方式：

```text
META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
```

旧的 `spring.factories` 仍在部分场景中存在，但自动配置主路径已变化。

## Spring Security 配置变化

老式 `WebSecurityConfigurerAdapter` 已被移除。

新方式通常声明 `SecurityFilterChain` Bean：

```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
    return http.authorizeHttpRequests(auth -> auth.anyRequest().authenticated()).build();
}
```

## Java 17 带来的影响

可以更自然使用：

- Record。
- Sealed Classes。
- Pattern Matching。
- Text Blocks。

## 面试重点

Spring Boot 3 的核心变化可以概括为：Java 17 基线、Spring 6、Jakarta 迁移、AOT/Native Image、Observability、自动配置声明变化和 Spring Security 新配置模型。升级时最大风险是第三方依赖和 `javax` 包兼容性。
""",
    ),
    (
        "Spring Boot 升级路线",
        "06-framework/spring-boot-version-features/upgrade-guide.md",
        """# Spring Boot 升级路线

Spring Boot 升级不能只改版本号，要按依赖、配置、代码、测试、压测和灰度逐步推进。

## 推荐路线

### 1.x 到 2.x

重点检查：

- Spring Framework 5 兼容性。
- Actuator endpoint 变化。
- Spring Security 配置。
- 第三方 Starter 版本。
- Micrometer 指标接入。

### 2.0-2.3 到 2.7

建议先升级到 2.7，作为进入 3.x 前的过渡版本。

重点检查：

- 配置属性废弃项。
- 循环依赖。
- 路径匹配策略。
- Spring Security 新写法。
- Spring Cloud 版本矩阵。

### 2.7 到 3.x

重点检查：

- JDK 升级到 17+。
- `javax.*` 到 `jakarta.*`。
- 第三方库是否支持 Jakarta。
- Spring Security 配置迁移。
- 自动配置声明方式。
- 观测链路从 Sleuth 迁移到 Micrometer Tracing/OpenTelemetry。

## 升级前清单

- 梳理 Spring Boot、Spring Cloud、JDK、Tomcat/Jetty、ORM、连接池、日志、监控 Agent 版本。
- 检查 Spring Boot 官方 compatibility matrix。
- 扫描废弃配置和废弃 API。
- 梳理自定义 Starter 和自动配置。
- 准备回滚方案。

## 升级中检查

- 编译错误。
- 单元测试和集成测试。
- 启动日志中的 deprecated 配置。
- 自动配置条件报告。
- Actuator endpoint 是否正常。
- 接口兼容性。

## 升级后验证

- 核心接口 P95/P99。
- JVM GC 和内存。
- 线程池、连接池和请求错误率。
- 日志、指标、链路追踪。
- 灰度流量和回滚演练。

## 面试回答模板

如果被问 Spring Boot 升级，我会先说明目标版本和原因，再讲风险点：依赖兼容、配置变化、自动配置变化、Jakarta 迁移、Security 迁移和观测链路变化。执行上按“依赖扫描 -> 编译修复 -> 自动化测试 -> 压测 -> 灰度 -> 回滚预案”推进。
""",
    ),
]


STATIC_DOCS = BIGDATA_DOCS + JAVA_VERSION_DOCS + SPRING_BOOT_VERSION_DOCS


def slug(text):
    text = text.strip().lower()
    text = re.sub(r"[\s_/&]+", "-", text)
    text = re.sub(r"[^\w\u4e00-\u9fff\-]+", "", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "topic"


def clean_title(title):
    return " ".join(str(title or "").replace("\n", " ").split())


def children_json(topic):
    children = topic.get("children", {}) or {}
    result = []
    for kind in ("attached", "detached"):
        result.extend(children.get(kind, []) or [])
    return result


def parse_json_xmind(path):
    with zipfile.ZipFile(path) as z:
        data = json.loads(z.read("content.json"))
    sheets = data if isinstance(data, list) else [data]

    def convert(topic):
        return {
            "title": clean_title(topic.get("title")),
            "children": [convert(c) for c in children_json(topic)],
        }

    return [convert(sheet.get("rootTopic", {})) for sheet in sheets]


def local_name(tag):
    return tag.split("}", 1)[-1]


def parse_xml_xmind(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("content.xml")
    root = ET.fromstring(xml)

    def title_of(elem):
        for child in elem:
            if local_name(child.tag) == "title":
                return clean_title("".join(child.itertext()))
        return ""

    def convert(topic):
        node = {"title": title_of(topic), "children": []}
        for child in topic:
            if local_name(child.tag) != "children":
                continue
            for topics in child:
                if (
                    local_name(topics.tag) == "topics"
                    and topics.attrib.get("type") == "attached"
                ):
                    for sub in topics:
                        if local_name(sub.tag) == "topic":
                            node["children"].append(convert(sub))
        return node

    roots = []
    for elem in root.iter():
        if local_name(elem.tag) == "sheet":
            for child in elem:
                if local_name(child.tag) == "topic":
                    roots.append(convert(child))
                    break
    return roots


def parse_xmind(rel_path):
    path = ROOT / rel_path
    if not path.exists():
        return []
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
    if "content.json" in names:
        return parse_json_xmind(path)
    return parse_xml_xmind(path)


def render_tree(node, level=2, seen=None):
    seen = seen if seen is not None else defaultdict(set)
    title = clean_title(node.get("title"))
    if not title:
        return []

    lines = []
    children = node.get("children", [])
    if level <= 4:
        if title in seen[level]:
            suffix = len(seen[level]) + 1
            title = f"{title} ({suffix})"
        seen[level].add(title)
        lines.append(f"{'#' * level} {title}")
        lines.append("")
        for child in children:
            if lines and lines[-1] != "":
                lines.append("")
            lines.extend(render_tree(child, level + 1, seen))
    else:
        lines.append(f"{'  ' * (level - 5)}- {title}")
        for child in children:
            lines.extend(render_tree(child, level + 1, seen))
    return lines


def render_notes(key):
    notes = EXPERT_NOTES.get(key, {})
    lines = []
    for section in ("核心认知", "面试重点", "实践检查点"):
        items = notes.get(section, [])
        if not items:
            continue
        lines.append(f"## {section}")
        lines.append("")
        for item in items:
            lines.append(f"- {item}")
        lines.append("")
    trends = TOPIC_TRENDS.get(key, [])
    if trends:
        lines.append("## 版本与趋势")
        lines.append("")
        for item in trends:
            lines.append(f"- {item}")
        lines.append("")
    return lines


OVERVIEW_LINKS = [
    (
        "Java 与 JVM",
        [
            ("Java 语言基础", "../../01-java/java/README.md"),
            ("Java 版本新特性", "../../01-java/java-version-features/README.md"),
            ("JVM", "../../01-java/jvm/README.md"),
        ],
    ),
    (
        "数据库",
        [
            ("MySQL", "../../02-database/mysql/README.md"),
            ("MongoDB", "../../02-database/mongodb.md"),
        ],
    ),
    (
        "缓存",
        [
            ("Redis", "../../03-cache/redis/README.md"),
        ],
    ),
    (
        "搜索",
        [
            ("Elasticsearch", "../../04-search/elasticsearch/README.md"),
        ],
    ),
    (
        "消息队列",
        [
            ("消息队列总览", "../../05-mq/mq-overview/README.md"),
            ("Kafka", "../../05-mq/kafka/README.md"),
            ("RocketMQ", "../../05-mq/rocketmq/README.md"),
        ],
    ),
    (
        "开发框架",
        [
            ("Spring", "../../06-framework/spring/README.md"),
            ("Spring Boot", "../../06-framework/spring-boot/README.md"),
            (
                "Spring Boot 版本新特性",
                "../../06-framework/spring-boot-version-features/README.md",
            ),
            ("Spring MVC", "../../06-framework/spring-mvc/README.md"),
            ("MyBatis", "../../06-framework/mybatis/README.md"),
        ],
    ),
    (
        "微服务",
        [
            ("Spring Cloud", "../../07-microservices/spring-cloud/README.md"),
            ("Spring Cloud Alibaba", "../../07-microservices/spring-cloud-alibaba.md"),
            ("Nacos", "../../07-microservices/nacos/README.md"),
        ],
    ),
    (
        "分布式与网络",
        [
            ("Dubbo", "../../08-distributed/dubbo/README.md"),
            ("ZooKeeper", "../../08-distributed/zookeeper/README.md"),
            ("Netty", "../../09-network/netty/README.md"),
        ],
    ),
    (
        "大数据",
        [
            ("大数据方向知识库", "../../11-bigdata/README.md"),
            ("HDFS", "../../11-bigdata/hadoop/hdfs.md"),
            ("Hive", "../../11-bigdata/hive/README.md"),
            ("Spark", "../../11-bigdata/spark/README.md"),
            ("Flink", "../../11-bigdata/flink/README.md"),
            ("ClickHouse", "../../11-bigdata/clickhouse/README.md"),
        ],
    ),
]


def render_overview_outline(sources):
    lines = []
    for source in sources:
        roots = parse_xmind(source)
        if not roots:
            continue
        lines.append(f"### {source}")
        lines.append("")
        for root in roots:
            for child in root.get("children", []):
                title = clean_title(child.get("title"))
                if not title:
                    continue
                children = [
                    clean_title(c.get("title")) for c in child.get("children", [])
                ]
                children = [c for c in children if c]
                if children:
                    lines.append(f"- {title}：{', '.join(children[:12])}")
                else:
                    lines.append(f"- {title}")
        lines.append("")
    return lines


def write_overview_doc(key, folder, title, sources):
    base_dir = OUT / folder / FILE_NAMES.get(key, slug(title))
    base_dir.mkdir(parents=True, exist_ok=True)
    readme = base_dir / "README.md"

    lines = [f"# {title}", "", f"> 来源：{', '.join(sources)}", ""]
    lines.extend(render_notes(key))
    lines.extend(
        [
            "## 使用方式",
            "",
            "- 本页只保留知识地图和详细文档入口，避免与各专题文档重复。",
            "- 需要深入复习时，直接进入下方详细专题链接。",
            "- 原脑图主干保留为概要，帮助快速定位知识范围。",
            "",
            "## 详细专题入口",
            "",
        ]
    )
    for group, links in OVERVIEW_LINKS:
        lines.append(f"### {group}")
        lines.append("")
        for text, href in links:
            lines.append(f"- [{text}]({href})")
        lines.append("")
    lines.extend(["## 原脑图主干", ""])
    lines.extend(render_overview_outline(sources))
    readme.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return readme


def normalize_match_text(text):
    return str(text or "").lower().replace(" ", "")


def section_notes(topic_title, section_title):
    topic = normalize_match_text(topic_title)
    section = normalize_match_text(section_title)
    for rule_topic, keywords, notes in SECTION_RULES:
        if normalize_match_text(rule_topic) not in topic:
            continue
        if any(normalize_match_text(keyword) in section for keyword in keywords):
            return notes
    return DEFAULT_SECTION_NOTES


def detail_sections(topic_title, section_title):
    topic = normalize_match_text(topic_title)
    section = normalize_match_text(section_title)
    matched = []
    for rule_topic, keywords, blocks in DETAIL_SECTION_RULES:
        if normalize_match_text(rule_topic) not in topic:
            continue
        matched_keyword = False
        for keyword in keywords:
            keyword_text = normalize_match_text(keyword)
            if keyword_text.startswith("exact:"):
                matched_keyword = section == keyword_text.removeprefix("exact:")
            else:
                matched_keyword = keyword_text in section
            if matched_keyword:
                break
        if matched_keyword:
            matched.extend(blocks)
    if matched:
        return matched

    title = clean_title(section_title)
    topic_name = clean_title(topic_title)
    return [
        (
            "是什么",
            [
                f"`{title}` 是 `{topic_name}` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。",
                "如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。",
            ],
        ),
        (
            "为什么重要",
            [
                "这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。",
                "准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。",
            ],
        ),
        (
            "实践关注",
            [
                "整理至少一个业务或框架中的使用场景。",
                "补充常见坑点、异常表现、排查手段和优化方向。",
                "如果涉及配置或参数，记录默认值、调优依据和风险边界。",
            ],
        ),
        (
            "面试表达",
            [
                f"回答 `{title}` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。",
                "如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。",
            ],
        ),
    ]


def render_section_notes(topic_title, section_title):
    lines = ["## 补充与实践", ""]
    for item in section_notes(topic_title, section_title):
        lines.append(f"- {item}")
    lines.append("")
    details = detail_sections(topic_title, section_title)
    if details:
        lines.append("## 详细说明")
        lines.append("")
        for heading, items in details:
            lines.append(f"### {heading}")
            lines.append("")
            for item in items:
                if isinstance(item, dict) and "code" in item:
                    lang = item.get("lang", "")
                    lines.append(f"```{lang}")
                    lines.append(item["code"].rstrip())
                    lines.append("```")
                else:
                    lines.append(f"- {item}")
            lines.append("")
        lines.append("### 复习检查")
        lines.append("")
        lines.append(
            f"- 能用自己的话解释 `{clean_title(section_title)}`，而不是只复述标题。"
        )
        lines.append("- 能说出至少一个生产场景、一个常见坑点和一个排查方向。")
        lines.append("")
    return lines


def unique_path(directory, base_name, used, order):
    base = slug(base_name)
    name = f"{order:02d}-{base}"
    index = 2
    while name in used:
        name = f"{order:02d}-{base}-{index}"
        index += 1
    used.add(name)
    return directory / f"{name}.md"


def unique_dir(directory, base_name, used, order):
    base = slug(base_name)
    name = f"{order:02d}-{base}"
    index = 2
    while name in used:
        name = f"{order:02d}-{base}-{index}"
        index += 1
    used.add(name)
    return directory / name


def collect_sections(title, sources):
    sections = []
    for source in sources:
        roots = parse_xmind(source)
        for root in roots:
            children = root.get("children", [])
            for child in children:
                child_title = clean_title(child.get("title"))
                if title == "Java 语言基础" and child_title == "新特性":
                    continue
                sections.append((child_title, source, [child]))
    return sections


def render_nodes(nodes):
    lines = []
    for node in nodes:
        lines.extend(render_tree(node, 2))
        if lines and lines[-1] != "":
            lines.append("")
    return lines


def collect_node_titles(node, depth=0, max_depth=3, limit=40):
    titles = []
    if depth > 0:
        title = clean_title(node.get("title"))
        if title:
            titles.append((depth, title))
    if depth >= max_depth or len(titles) >= limit:
        return titles[:limit]
    for child in node.get("children", []):
        titles.extend(
            collect_node_titles(child, depth + 1, max_depth, limit - len(titles))
        )
        if len(titles) >= limit:
            break
    return titles[:limit]


def render_mindmap_insights(topic_title, section_title, nodes):
    extracted = []
    for node in nodes:
        extracted.extend(collect_node_titles(node))
    seen = set()
    titles = []
    for depth, title in extracted:
        if title == section_title or title in seen:
            continue
        seen.add(title)
        titles.append((depth, title))

    if not titles:
        return []

    top = [title for depth, title in titles if depth == 1]
    second = [title for depth, title in titles if depth == 2]
    third = [title for depth, title in titles if depth >= 3]
    focus = (top or second or [title for _, title in titles])[:8]

    lines = ["## 脑图解读", ""]
    lines.append(
        f"- 本节脑图围绕 `{clean_title(section_title)}` 展开，属于 `{clean_title(topic_title)}` 的复习范围。"
    )
    lines.append(f"- 建议优先掌握：{', '.join(focus)}。")
    if second:
        lines.append(f"- 二级节点提示了主要拆分角度：{', '.join(second[:10])}。")
    if third:
        lines.append(
            f"- 三级节点通常对应具体细节、API、机制或易错点：{', '.join(third[:10])}。"
        )
    lines.append("")
    lines.append("### 复习追问")
    lines.append("")
    for title in focus[:5]:
        lines.append(
            f"- `{title}` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？"
        )
    lines.append("")
    return lines


def write_section_entry(
    base_dir, topic_title, section_title, source, nodes, order, used
):
    content = render_nodes(nodes)
    can_split = len(nodes) == 1 and nodes[0].get("children")

    if len(content) > MAX_SECTION_LINES and can_split:
        section_dir = unique_dir(base_dir, section_title, used, order)
        section_dir.mkdir(parents=True, exist_ok=True)
        child_used = set()
        child_entries = []

        for child_order, child in enumerate(nodes[0].get("children", []), 1):
            child_title = clean_title(child.get("title"))
            if not child_title:
                continue
            child_path = write_section_entry(
                section_dir,
                topic_title,
                child_title,
                source,
                [child],
                child_order,
                child_used,
            )
            child_entries.append((child_title, child_path))

        readme = section_dir / "README.md"
        lines = [
            f"# {section_title}",
            "",
            f"> 专题：{topic_title}",
            f"> 来源：{source}",
            "",
        ]
        lines.extend(render_section_notes(topic_title, section_title))
        lines.extend(["## 子章节", ""])
        for child_title, child_path in child_entries:
            rel = child_path.relative_to(section_dir).as_posix()
            lines.append(f"- [{child_title}]({rel})")
        readme.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        return readme

    target = unique_path(base_dir, section_title, used, order)
    lines = [
        f"# {section_title}",
        "",
        f"> 专题：{topic_title}",
        f"> 来源：{source}",
        "",
    ]
    lines.extend(render_section_notes(topic_title, section_title))
    lines.extend(render_mindmap_insights(topic_title, section_title, nodes))
    lines.extend(["## 脑图内容", ""])
    lines.extend(content)
    target.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return target


def write_split_doc(key, folder, title, sources):
    base_dir = OUT / folder / FILE_NAMES.get(key, slug(title))
    base_dir.mkdir(parents=True, exist_ok=True)
    used = set()
    entries = []

    for order, (section_title, source, nodes) in enumerate(
        collect_sections(title, sources), 1
    ):
        if not section_title:
            continue
        target = write_section_entry(
            base_dir, title, section_title, source, nodes, order, used
        )
        entries.append((section_title, target, source))

    readme = base_dir / "README.md"
    lines = [f"# {title}", "", f"> 来源：{', '.join(sources)}", ""]
    lines.extend(render_notes(key))
    lines.append("## 章节目录")
    lines.append("")
    current_source = None
    for section_title, target, source in entries:
        if len(sources) > 1 and source != current_source:
            current_source = source
            lines.append(f"### {source}")
            lines.append("")
        rel = target.relative_to(base_dir).as_posix()
        lines.append(f"- [{section_title}]({rel})")
    if not entries:
        lines.append("暂无可抽取内容。")
    lines.append("")
    readme.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return readme


def write_doc(key, folder, title, sources):
    if key == "Summary":
        return write_overview_doc(key, folder, title, sources)

    if key in SPLIT_DOCS:
        return write_split_doc(key, folder, title, sources)

    target_dir = OUT / folder
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{FILE_NAMES.get(key, slug(title))}.md"

    lines = [f"# {title}", "", f"> 来源：{', '.join(sources)}", ""]
    lines.extend(render_notes(key))
    lines.append("## 脑图内容整理")
    lines.append("")

    has_content = False
    for source in sources:
        roots = parse_xmind(source)
        if not roots:
            continue
        has_content = True
        tree_level = 2
        if len(sources) > 1:
            lines.append(f"## 来源：{source}")
            lines.append("")
            tree_level = 3
        for root in roots:
            children = root.get("children", [])
            root_title = clean_title(root.get("title"))
            if root_title and root_title != title and len(sources) == 1:
                lines.append(f"## {root_title}")
                lines.append("")
                tree_level = 3
            for child in children:
                child_title = clean_title(child.get("title"))
                if child_title:
                    lines.extend(render_section_notes(title, child_title))
                    lines.extend(render_mindmap_insights(title, child_title, [child]))
                lines.extend(render_tree(child, tree_level))
                if lines and lines[-1] != "":
                    lines.append("")

    if not has_content:
        lines.append("暂无可抽取内容。")
        lines.append("")

    text = "\n".join(lines).rstrip() + "\n"
    target.write_text(text, encoding="utf-8")
    return target


def write_index(files):
    OUT.mkdir(parents=True, exist_ok=True)
    folder_titles = {
        "00-overview": "总览",
        "01-java": "Java 与 JVM",
        "02-database": "数据库",
        "03-cache": "缓存",
        "04-search": "搜索引擎",
        "05-mq": "消息队列",
        "06-framework": "开发框架",
        "07-microservices": "微服务",
        "08-distributed": "分布式协调与 RPC",
        "09-network": "网络通信",
        "10-php": "PHP",
        "11-bigdata": "大数据",
    }
    grouped = defaultdict(list)
    for title, path in files:
        rel_parent = path.parent.relative_to(OUT)
        folder = rel_parent.parts[0] if rel_parent.parts else path.parent.name
        grouped[folder].append((title, path))

    lines = [
        "# 技术知识库",
        "",
        "本目录由原始 XMind 脑图整理为 Markdown，并按技术主题补充了核心认知、面试重点、实践检查点、版本趋势和章节实践建议。",
        "",
        "## 阅读路径",
        "",
        "- 先阅读 `00-overview/summary/README.md` 建立全局地图。",
        "- Java 后端方向建议依次阅读 Java/JVM、数据库、缓存、消息队列、Spring、微服务、分布式协调与网络通信。",
        "- 专题 `README.md` 提供全局框架和版本趋势，章节文档提供补充实践建议和脑图原始内容整理。",
        "",
        "## 目录",
        "",
    ]
    for folder in sorted(grouped):
        lines.append(f"### {folder_titles.get(folder, folder)}")
        lines.append("")
        for title, path in sorted(grouped[folder], key=lambda x: x[0]):
            rel = path.relative_to(OUT).as_posix()
            lines.append(f"- [{title}]({rel})")
        lines.append("")
    (OUT / "README.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_static_docs():
    files = []
    for title, rel_path, content in STATIC_DOCS:
        target = OUT / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content.rstrip() + "\n", encoding="utf-8")
        files.append((title, target))
    return files


def main():
    OUT.mkdir(exist_ok=True)
    files = []
    for key, (folder, title, sources) in TOPIC_CONFIG.items():
        path = write_doc(key, folder, title, sources)
        files.append((title, path))
    files.extend(write_static_docs())
    write_index(files)


if __name__ == "__main__":
    main()
