# RocketMQ监控

> 专题：RocketMQ
> 来源：RocketMQ.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## RocketMQ监控

### 设计理念

#### 生产者与消费者在与RocketMQ集群进行交互时会收集相关统计信息并存储在内存中，一般都是采用滑动窗口的机制避免统计数据在内存中不断积压，造成内存移除

#### 监控采集客户端会将RocketMQ集群中存储的指标抽取到一个存储介质中，通常会使用时序数据库，开入InfluxDB。监控界面从存储介质中查询数据后进行可视化展示

#### 相关指标

- TOPIC_PUT_NUMS
  - 以主题为维度统计消息写入数量

- TOPIC_PUT_SIZE
  - 以主题为维度统计消息写入字节数

- GROUP_GET_NUMS
  - 以消费组为维度统计消息获取条数

- GROUP_GET_SIZE
  - 以消费组为维度统计获取字节数

- SNDBCK_PUT_NUMS
  - 以消费组为维度统计重试消息发送数量

- BROKER_PUT_NUMS
  - 以集群为维度统计消息写入条数

- BROKER_GET_NUMS
  - 以集群为维度统计消息获取条数

- GROUP_GET_LATENCY
  - 以消费组为维度统计消息拉取延迟时间

### 相关日志

#### ${user.home}/logs/rocketmqlogs/stat.log

### 监控应用

#### Prometheus

- SoundCloud开源

#### MQCloud

- 搜狐开源
