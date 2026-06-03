# Flink Window 与 Watermark

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
