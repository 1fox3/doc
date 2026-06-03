# 实时数仓

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
