# 技术知识库

本目录由原始 XMind 脑图整理为 Markdown，并按技术主题补充了核心认知、面试重点、实践检查点、版本趋势和章节实践建议。

## 阅读路径

- 先阅读 `00-overview/summary/README.md` 建立全局地图。
- Java 后端方向建议依次阅读 Java/JVM、数据库、缓存、消息队列、Spring、微服务、分布式协调与网络通信。
- 专题 `README.md` 提供全局框架和版本趋势，章节文档提供补充实践建议和脑图原始内容整理。

## 目录

### 总览

- [重点汇总](00-overview/summary/README.md)

### Java 与 JVM

- [JVM](01-java/jvm/README.md)
- [Java 12-17 新特性](01-java/java-version-features/java-12-17.md)
- [Java 18-21 新特性](01-java/java-version-features/java-18-21.md)
- [Java 8 新特性](01-java/java-version-features/java-8.md)
- [Java 9-11 新特性](01-java/java-version-features/java-9-11.md)
- [Java 版本新特性总览](01-java/java-version-features/README.md)
- [Java 语言基础](01-java/java/README.md)
- [LTS 版本选型与升级](01-java/java-version-features/lts-upgrade.md)

### 数据库

- [MongoDB](02-database/mongodb.md)
- [MySQL](02-database/mysql/README.md)

### 缓存

- [Redis](03-cache/redis/README.md)

### 搜索引擎

- [Elasticsearch](04-search/elasticsearch/README.md)

### 消息队列

- [Kafka](05-mq/kafka/README.md)
- [RocketMQ](05-mq/rocketmq/README.md)
- [消息队列总览](05-mq/mq-overview/README.md)

### 开发框架

- [MyBatis](06-framework/mybatis/README.md)
- [Spring](06-framework/spring/README.md)
- [Spring Boot](06-framework/spring-boot/README.md)
- [Spring Boot 1.x 到 2.x](06-framework/spring-boot-version-features/spring-boot-1-to-2.md)
- [Spring Boot 2.0 到 2.3](06-framework/spring-boot-version-features/spring-boot-2-0-to-2-3.md)
- [Spring Boot 2.4 到 2.7](06-framework/spring-boot-version-features/spring-boot-2-4-to-2-7.md)
- [Spring Boot 3.x](06-framework/spring-boot-version-features/spring-boot-3.md)
- [Spring Boot 升级路线](06-framework/spring-boot-version-features/upgrade-guide.md)
- [Spring Boot 版本新特性总览](06-framework/spring-boot-version-features/README.md)
- [Spring MVC](06-framework/spring-mvc/README.md)

### 微服务

- [Nacos](07-microservices/nacos/README.md)
- [Spring Cloud](07-microservices/spring-cloud/README.md)
- [Spring Cloud Alibaba](07-microservices/spring-cloud-alibaba.md)

### 分布式协调与 RPC

- [Dubbo](08-distributed/dubbo/README.md)
- [ZooKeeper](08-distributed/zookeeper/README.md)

### 网络通信

- [Netty](09-network/netty/README.md)

### PHP

- [PHP7 内核剖析](10-php/php7-kernel/README.md)

### 大数据

- [Apache Doris](11-bigdata/olap/doris.md)
- [Apache Hudi](11-bigdata/lakehouse/hudi.md)
- [Apache Iceberg](11-bigdata/lakehouse/iceberg.md)
- [ClickHouse](11-bigdata/clickhouse/README.md)
- [ClickHouse 查询优化](11-bigdata/clickhouse/query-optimization.md)
- [Flink](11-bigdata/flink/README.md)
- [Flink CDC](11-bigdata/data-pipeline/flink-cdc.md)
- [Flink Checkpoint](11-bigdata/flink/checkpoint.md)
- [Flink Exactly Once](11-bigdata/flink/exactly-once.md)
- [Flink State Backend](11-bigdata/flink/state-backend.md)
- [Flink Window 与 Watermark](11-bigdata/flink/window-watermark.md)
- [HBase](11-bigdata/hbase/README.md)
- [HBase Compaction 与 Region](11-bigdata/hbase/compaction-region.md)
- [HBase RowKey 设计](11-bigdata/hbase/rowkey-design.md)
- [HDFS](11-bigdata/hadoop/hdfs.md)
- [Hadoop 总览](11-bigdata/hadoop/README.md)
- [Hive](11-bigdata/hive/README.md)
- [Hive Metastore](11-bigdata/hive/metastore.md)
- [Hive SQL 优化](11-bigdata/hive/sql-optimization.md)
- [Hive 分区与分桶](11-bigdata/hive/partition-bucket.md)
- [MapReduce](11-bigdata/hadoop/mapreduce.md)
- [MergeTree](11-bigdata/clickhouse/mergetree.md)
- [ODS/DWD/DWS/ADS](11-bigdata/data-warehouse/ods-dwd-dws-ads.md)
- [Spark](11-bigdata/spark/README.md)
- [Spark RDD/DataFrame/Dataset](11-bigdata/spark/rdd-dataframe-dataset.md)
- [Spark Shuffle](11-bigdata/spark/shuffle.md)
- [Spark 内存与 OOM](11-bigdata/spark/memory-oom.md)
- [Trino/Presto](11-bigdata/olap/trino.md)
- [YARN](11-bigdata/hadoop/yarn.md)
- [任务调度系统](11-bigdata/platform/scheduler.md)
- [元数据与血缘](11-bigdata/governance/metadata-lineage.md)
- [大数据基础概念](11-bigdata/fundamentals/basic-concepts.md)
- [大数据学习路线](11-bigdata/learning-path.md)
- [大数据求职路线](11-bigdata/README.md)
- [大数据线上排障手册](11-bigdata/operations/troubleshooting.md)
- [大数据项目面试模板](11-bigdata/project-experience.md)
- [实时数仓](11-bigdata/data-warehouse/realtime-warehouse.md)
- [小文件治理](11-bigdata/optimization/small-files.md)
- [批处理与流处理](11-bigdata/fundamentals/batch-vs-stream.md)
- [指标体系与口径治理](11-bigdata/data-warehouse/metrics.md)
- [数仓建模](11-bigdata/data-warehouse/README.md)
- [数据倾斜治理](11-bigdata/optimization/data-skew.md)
- [数据同步工具](11-bigdata/data-pipeline/sync-tools.md)
- [数据安全与权限](11-bigdata/governance/security.md)
- [数据格式与压缩](11-bigdata/fundamentals/file-format-compression.md)
- [数据质量](11-bigdata/governance/data-quality.md)
- [数据采集与日志链路](11-bigdata/data-pipeline/log-collection.md)
- [数据链路与湖仓](11-bigdata/data-pipeline/README.md)
- [湖仓选型对比](11-bigdata/lakehouse/table-format-comparison.md)
- [维度建模与拉链表](11-bigdata/data-warehouse/dimensional-modeling.md)
- [资源与成本治理](11-bigdata/platform/resource-cost.md)
