# 消息存储

## 存储文件

- `CommitLog`：保存完整消息内容，所有 Topic 的消息混合顺序写入。
- `ConsumeQueue`：消费队列索引，按 Topic 和 QueueId 组织，记录 CommitLog offset、消息大小和 tag hash。
- `IndexFile`：按 key 查询消息的索引文件。

## 写入链路

1. Broker 接收发送请求。
2. 校验消息和 Topic 权限。
3. 追加写入 CommitLog。
4. Reput 线程异步分发 ConsumeQueue 和 IndexFile。
5. 根据刷盘和复制策略返回结果。

## MappedFile

RocketMQ 使用内存映射文件提升文件读写效率。MappedFileQueue 管理多个固定大小文件，CommitLog 默认单文件较大，ConsumeQueue 单位更小且按队列拆分。

## 刷盘策略

- 异步刷盘：写入页缓存后返回，吞吐高，但宕机可能丢失未刷盘数据。
- 同步刷盘：等待刷盘成功后返回，可靠性更高但延迟更高。

## transientStorePool

在异步刷盘场景中，可以先写入堆外内存池，再提交到 FileChannel，降低 page cache 抖动，但链路更复杂，需要结合版本和部署策略评估。

## 文件清理与恢复

Broker 启动时会根据 CommitLog、ConsumeQueue 和 checkpoint 恢复状态。过期文件删除通常按时间和磁盘水位触发。磁盘水位过高会触发写入保护，严重时影响生产可用性。

## 排障关注

- CommitLog 写入延迟。
- ConsumeQueue 分发积压。
- 磁盘使用率和刷盘耗时。
- Page cache 命中和 OS I/O wait。
- Broker 是否因磁盘水位进入保护状态。
