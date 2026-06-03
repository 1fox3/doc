# 批处理与流处理

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
