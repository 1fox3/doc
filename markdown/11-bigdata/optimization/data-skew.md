# 数据倾斜治理

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
