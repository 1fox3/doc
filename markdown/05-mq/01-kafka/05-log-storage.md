# 日志存储与清理

## 日志结构

每个分区对应一个日志目录，目录内由多个 LogSegment 组成。每个 Segment 通常包含：

- `.log`：消息数据文件。
- `.index`：offset 到物理位置的稀疏索引。
- `.timeindex`：时间戳到 offset 的稀疏索引。
- 事务相关索引：用于事务消息控制。

## 写入与读取

- 写入采用追加写，磁盘顺序写吞吐高。
- 操作系统页缓存承担主要缓存能力，Kafka 不重复实现复杂缓存层。
- 读取文件发送给网络时可利用零拷贝，减少用户态和内核态复制。
- 索引是稀疏索引，先定位接近位置，再顺序扫描。

## 日志切分

Segment 会按大小或时间切分，常见参数包括：

- `log.segment.bytes`
- `log.roll.ms`
- `log.roll.hours`

切分粒度影响删除效率、索引大小和恢复成本。

## 清理策略

- `log.cleanup.policy=delete`：按时间或大小删除旧 Segment，适合日志和事件流。
- `log.cleanup.policy=compact`：按 key 保留最新值，适合状态变更和 CDC changelog。
- `delete,compact` 可组合使用。

## 保留参数

- `log.retention.ms` / `log.retention.hours`：按时间保留。
- `log.retention.bytes`：按分区日志大小保留。
- `retention.ms`、`retention.bytes` 可在 Topic 级覆盖。

## 大消息问题

Kafka 默认更适合中小消息。大消息会降低批处理效率、占用网络和页缓存、拉高 GC 与请求延迟。生产环境优先把大对象放对象存储，只在 Kafka 中传引用；确实要调大时需同时检查 producer、broker、consumer 的最大消息大小配置。
