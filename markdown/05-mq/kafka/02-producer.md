# 生产者

## 发送流程

1. 应用构造 `ProducerRecord`。
2. 经过 `ProducerInterceptor`，可做审计、埋点、字段补充。
3. 使用 key/value serializer 序列化。
4. 根据分区器选择目标分区。
5. 写入 `RecordAccumulator`。
6. Sender 线程按 Broker 聚合请求并发送。
7. Broker 返回响应后触发 callback。

## 发送模式

- fire-and-forget：只调用 `send`，不关心结果，吞吐高但可靠性最低。
- sync：调用 `send(record).get()`，链路简单但吞吐低。
- async：通过 callback 感知结果，生产环境更常见。

## 分区选择

- 显式指定 partition 时直接写入该分区。
- key 不为空时通常按 key hash，保证相同 key 进入同一分区。
- key 为空时使用粘性分区策略，优先把一批消息写入同一分区，批次满或分区不可用后切换。

## 关键参数

- `bootstrap.servers`：初始 Broker 地址，不需要配置所有 Broker，但至少配置多个以避免单点。
- `acks`：`0` 不等待响应，`1` 等 Leader 写入，`all` 等 ISR 中满足条件的副本写入。
- `retries`：可重试异常的重试次数，应配合幂等避免乱序和重复影响。
- `batch.size`：单个分区 ProducerBatch 大小，过小影响吞吐，过大增加延迟和内存压力。
- `linger.ms`：等待更多消息进入批次的时间，适当增大可提升压缩率和吞吐。
- `buffer.memory`：生产者总缓冲区大小，耗尽后 `send` 可能阻塞。
- `max.block.ms`：等待元数据或缓冲区可用的最长时间。
- `compression.type`：常用 `lz4`、`snappy`、`zstd`，压缩降低网络和磁盘压力但增加 CPU 消耗。
- `max.in.flight.requests.per.connection`：单连接未确认请求数；开启幂等后 Kafka 可以在保证有序的前提下处理重试。

## 工程实践

- 高可靠链路使用 `acks=all`、合理副本数、`min.insync.replicas>=2` 和幂等生产者。
- 需要单 key 顺序时，保证同一业务 key 固定进入同一分区，不要在处理链路中并发打乱同一 key。
- callback 中不要执行慢逻辑，避免阻塞 Sender 线程。
- 生产端异常要区分可重试异常、不可重试异常和业务校验失败。
