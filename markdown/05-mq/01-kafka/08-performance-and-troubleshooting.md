# 性能调优与故障排查

## 生产端调优

- 增大 `batch.size` 和 `linger.ms` 提升批量效果。
- 开启 `compression.type` 降低网络和磁盘压力。
- 避免 callback 慢逻辑阻塞 Sender 线程。
- 监控 `bufferpool-wait-time`、请求延迟和重试次数。

## Broker 调优

- 使用多磁盘目录分摊分区日志。
- 控制单 Broker 分区数量，避免恢复和 Leader 选举过慢。
- 关注页缓存命中、磁盘 I/O、网络带宽和请求队列。
- 对跨机房复制或大规模副本迁移设置限流，避免影响正常读写。

## 消费端调优

- 分区数决定同一 group 的最大并行度。
- `max.poll.records` 控制单次拉取量，避免一次处理过多导致超时。
- `max.poll.interval.ms` 要大于最长业务处理时间，或拆分慢任务。
- 使用手动提交 offset，把提交位置绑定到已完成业务。

## 消息堆积排查

排查顺序建议：

1. 看生产速率是否突增。
2. 看 consumer lag 是所有分区增长还是少数分区热点。
3. 看消费者实例数是否小于分区数。
4. 看业务处理耗时、下游依赖和线程池队列。
5. 看是否频繁 Rebalance。
6. 看 Broker 磁盘、网络、GC 和请求延迟。

## 关键监控

- Consumer lag。
- Under replicated partitions。
- Offline partitions。
- ISR shrink/expand 频率。
- Produce/fetch request latency。
- Broker 磁盘使用率和剩余空间。
- Controller 切换次数。
- 请求错误率、重试率和限流情况。
