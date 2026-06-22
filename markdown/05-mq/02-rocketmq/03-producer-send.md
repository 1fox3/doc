# 消息发送

## 发送方式

- 同步发送：等待 Broker 响应，适合重要业务消息。
- 异步发送：通过 callback 获取结果，适合高吞吐链路。
- 单向发送：不等待响应，适合日志、监控等允许丢失的场景。

## 发送流程

1. Producer 校验 Topic、消息体大小和属性。
2. 获取或刷新 Topic 路由。
3. 根据负载均衡策略选择 MessageQueue。
4. 发送请求到目标 Broker。
5. Broker 写入消息并返回 SendResult。
6. 失败时按异常类型和重试配置决定是否重试。

## 队列选择

- 默认轮询队列，配合故障规避跳过近期失败 Broker。
- 顺序消息使用 `MessageQueueSelector` 或 sharding key，把同一业务键写入同一队列。
- 批量消息要求同一批消息属于同一 Topic，且消息总大小不能过大。

## 发送重试

同步发送失败可按配置重试其他 Broker。重试可能导致重复消息，所以业务必须设计幂等。单向发送无法感知失败，不适合核心交易链路。

## 常见参数

- `sendMsgTimeout`：发送超时时间。
- `retryTimesWhenSendFailed`：同步发送失败重试次数。
- `retryTimesWhenSendAsyncFailed`：异步发送失败重试次数。
- `retryAnotherBrokerWhenNotStoreOK`：存储结果非 OK 时是否尝试其他 Broker。
- `compressMsgBodyOverHowmuch`：超过阈值后压缩消息体。

## 实践建议

- 核心消息使用同步发送，并记录 messageId、业务 key 和发送结果。
- 业务侧使用唯一键防重复，例如订单号、流水号、事件 ID。
- callback 中不要执行慢调用，避免阻塞客户端内部线程。
