# Flink CDC

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
