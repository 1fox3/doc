# 性能调优与故障排查

## 生产端调优

- 复用 Connection，按线程或组件管理 Channel。
- 使用 Publisher Confirm 的异步批量确认，不要每条消息同步等待。
- 控制消息大小，大消息优先存对象存储并在 MQ 中传引用。
- 路由失败必须监控 return callback。

## 消费端调优

- 合理设置 prefetch，避免慢消费者缓存过多未 ack 消息。
- 消费处理慢时扩容消费者，但不要超过下游承载能力。
- 使用手动 ack，并把 ack 放在业务处理成功之后。
- 对不可恢复错误进入死信，不要无限 requeue。

## Broker 调优

- 监控内存水位、磁盘水位和 flow control。
- 使用 quorum queue 时关注 Raft 副本状态和同步延迟。
- 避免单队列超大堆积，必要时按业务 key 拆分多个队列。
- 对持久化消息关注磁盘 I/O 和 fsync 延迟。

## 堆积排查

1. 查看 ready、unacked 和 total 消息数。
2. 如果 unacked 高，说明消费者拿到消息但处理或 ack 慢。
3. 如果 ready 高，说明消费者数量不足、prefetch 不合理或下游慢。
4. 检查是否有毒丸消息反复 requeue。
5. 检查磁盘、内存水位是否触发 flow control。

## 关键监控

- Queue ready/unacked 数量。
- Publish/ack/deliver rate。
- Consumer 数量和 channel 数量。
- Connection churn。
- 内存水位、磁盘水位、文件描述符。
- Dead letter 数量。
- Confirm 延迟和 return 数量。
