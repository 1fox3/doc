# 技术知识库

本目录由原始 XMind 脑图整理为 Markdown，并按技术主题补充了核心认知、面试重点、实践检查点、版本趋势和章节实践建议。

## 阅读路径

- Java 后端方向建议依次阅读 Java/JVM、数据库、缓存、消息队列、Spring、微服务、分布式协调与网络通信。
- 专题 `README.md` 提供全局框架和版本趋势，章节文档提供补充实践建议和脑图原始内容整理。

## 目录

### Java 与 JVM

- [Java 语言基础](01-java/01-java/README.md)
- [JVM](01-java/02-jvm/README.md)
- [Java 版本新特性总览](01-java/01-java/06-java-version-features/README.md)
- [Java 8 新特性](01-java/01-java/06-java-version-features/java-8.md)
- [Java 9-11 新特性](01-java/01-java/06-java-version-features/java-9-11.md)
- [Java 12-17 新特性](01-java/01-java/06-java-version-features/java-12-17.md)
- [Java 18-21 新特性](01-java/01-java/06-java-version-features/java-18-21.md)
- [LTS 版本选型与升级](01-java/01-java/06-java-version-features/lts-upgrade.md)

### 开发框架

- [Framework 技术体系](02-framework/README.md)
- [Spring](02-framework/01-spring/README.md)
- [Spring MVC](02-framework/02-spring-mvc/README.md)
- [Spring Boot](02-framework/03-spring-boot/README.md)
- [Spring Boot 版本升级](02-framework/04-spring-boot-version-features/README.md)
- [Spring Boot 2.x 关键变化](02-framework/04-spring-boot-version-features/01-spring-boot-2.md)
- [Spring Boot 3.x 关键变化](02-framework/04-spring-boot-version-features/02-spring-boot-3.md)
- [Spring Boot 升级检查项](02-framework/04-spring-boot-version-features/03-upgrade-checklist.md)
- [MyBatis](02-framework/05-mybatis/README.md)

### 数据库

- [MySQL](03-database/01-mysql/README.md)
- [MongoDB](03-database/02-mongodb/README.md)

### 缓存

- [Redis](04-cache/01-redis/README.md)

### 消息队列

- [Kafka](05-mq/01-kafka/README.md)
- [RocketMQ](05-mq/02-rocketmq/README.md)
- [RabbitMQ](05-mq/03-rabbitmq/README.md)

### 搜索引擎

- [Elasticsearch](06-search/01-elasticsearch/README.md)

### 微服务

- [Spring Cloud](07-microservices/01-spring-cloud/README.md)
- [Spring Cloud Alibaba](07-microservices/01-spring-cloud/06-spring-cloud-alibaba.md)
- [Nacos](07-microservices/02-nacos/README.md)

### 分布式协调与 RPC

- [Dubbo](08-distributed/01-dubbo/README.md)
- [ZooKeeper](08-distributed/02-zookeeper/README.md)

### 网络通信

- [Netty](09-network/01-netty/README.md)

### 大数据

- [大数据技术体系](10-bigdata/README.md)
- [大数据架构与基础概念](10-bigdata/00-foundation/architecture-and-concepts.md)
- [数据格式与压缩](10-bigdata/00-foundation/file-format-and-compression.md)
- [分布式存储：HDFS、对象存储与 HBase](10-bigdata/01-storage/distributed-storage.md)
- [Hive Metastore 与表组织](10-bigdata/01-storage/hive-metastore-and-table-layout.md)
- [批计算：MapReduce 与 Spark](10-bigdata/02-compute/batch-compute-spark-mapreduce.md)
- [流计算：Flink 状态、窗口与一致性](10-bigdata/02-compute/stream-compute-flink.md)
- [资源管理：YARN 与多租户调度](10-bigdata/02-compute/resource-management-yarn.md)
- [数据采集、同步与 CDC](10-bigdata/03-ingestion/data-ingestion-and-cdc.md)
- [数仓分层、维度建模与指标体系](10-bigdata/04-warehouse-lakehouse/data-warehouse-modeling.md)
- [湖仓表格式：Iceberg、Hudi 与 Delta Lake](10-bigdata/04-warehouse-lakehouse/lakehouse-table-formats.md)
- [OLAP 查询与数据服务：ClickHouse、Doris、Trino、HBase](10-bigdata/05-olap-serving/olap-engines-and-serving.md)
- [数据治理与平台能力](10-bigdata/06-governance-platform/governance-and-platform.md)
- [性能优化与线上排障](10-bigdata/07-optimization-operations/performance-and-troubleshooting.md)
