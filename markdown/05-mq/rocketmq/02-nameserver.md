# NameServer

> 专题：RocketMQ
> 来源：RocketMQ.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 是什么

- `NameServer` 是 `RocketMQ` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `NameServer` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `NameServer`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `NameServer` 展开，属于 `RocketMQ` 的复习范围。
- 建议优先掌握：架构设计, 定时任务, 路由元信息, 路由注册, 路由删除, 路由发现。
- 二级节点提示了主要拆分角度：Broker每隔30秒项NameServer集群的每一台机器发送心跳包，包含自身创建的topic路由等信息, 消息客户端每隔30秒项NameServer更新对应的Topic路由信息, NameServer收到Broker发送的心跳包时会记录时间戳, Nameserver每隔10秒会扫描一次brokerLiveTable，如果120秒内没有收到心跳包，则认为Broker失效，更新topic的路由信息，将失效的Broker信息移除, NameServer每隔10秒扫描一次Broker，移除处于未激活状态的Broker, NameServer每隔10分钟打印一次KV配置, topicQueueTable, brokerAddrTable, clusterAddrTable, brokerLiveTable。
- 三级节点通常对应具体细节、API、机制或易错点：Broker上的FilterServer列表，用于类模式消息过滤, NameServer连续120秒没有收到Broker的心跳, Broker正常关闭情况下，会执行unregisterBroker指令。

### 复习追问

- `架构设计` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `定时任务` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `路由元信息` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `路由注册` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `路由删除` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## NameServer

### 架构设计

#### Broker每隔30秒项NameServer集群的每一台机器发送心跳包，包含自身创建的topic路由等信息

#### 消息客户端每隔30秒项NameServer更新对应的Topic路由信息

#### NameServer收到Broker发送的心跳包时会记录时间戳

#### Nameserver每隔10秒会扫描一次brokerLiveTable，如果120秒内没有收到心跳包，则认为Broker失效，更新topic的路由信息，将失效的Broker信息移除

### 定时任务

#### NameServer每隔10秒扫描一次Broker，移除处于未激活状态的Broker

#### NameServer每隔10分钟打印一次KV配置

### 路由元信息

#### topicQueueTable

#### brokerAddrTable

#### clusterAddrTable

#### brokerLiveTable

#### filterServerTable

- Broker上的FilterServer列表，用于类模式消息过滤

### 路由注册

#### Broker启动时向集群中所有的NameServer发送心跳语句，每隔30秒再发送一次

#### NameServer收到Broker心跳包时会先更新brokerLiveTable缓存中BrokerLiveInfo的lastUpdateTimestamp，然后每隔10秒扫描一次brokerLiveTable，如果连续120秒没有收到心跳包，NamerServer将移除Broker的路由信息，同时关闭Socket连接

### 路由删除

#### 触发条件

- NameServer连续120秒没有收到Broker的心跳

- Broker正常关闭情况下，会执行unregisterBroker指令

### 路由发现

#### RokcetMQ路由发现是非实时的，当topic路由出现变化后，NameServer不会主动推送给客户端，而是有客户端定时拉取主图的最新路由。

#### 根据主题拉取路由信息的命令编码为GET_ROUTEINFO_BY_TOPIC
