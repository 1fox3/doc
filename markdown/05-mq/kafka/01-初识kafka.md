# 初识Kafka

> 专题：Kafka
> 来源：Kafka.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## 初识Kafka

### 基本概念

#### Producer

- 生产者

#### Consumer

- 消费者

#### Broker

- 服务代理节点

#### Topic

- 主题

#### Partition

- 分区

#### Replica

- 副本(主+从)

#### AR

- 所有副本

#### ISR

- 一定程度同步的副本

#### OSR

- 同步滞后过多的副本

#### HW

- 高水位，消费者只能看到前一个消息

#### LSO

- 第一条消息的offset

#### LEO

- 下一条写入消息的offset

### 服务端参数配置

#### zookeeper.connect

#### listeners

#### broker.id

#### log.dir

#### log.dirs

- 优先级比log.dir高

#### message.max.bytes

- broker能接受消息的最大值
