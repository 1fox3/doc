# Hadoop 总览

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
