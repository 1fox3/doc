# Flink

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
