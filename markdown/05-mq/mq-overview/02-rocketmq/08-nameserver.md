# NameServer

> 专题：消息队列总览
> 来源：面试内容汇总/MQ.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

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
