# Curator

> 专题：ZooKeeper
> 来源：ZooKeeper.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## Curator

### Curator客户端

#### CuratorFramework

### 流畅式API

### 监听器

#### CuratorListener

#### UnhandledErrorListener

### 状态转换

#### Connected

#### Suspended

#### Reconnected

#### Lost

#### READ_ONLY

- 并不是Curator所独有的功能，而是通过ZooKeeper启用该选项

### 两种边界情况

#### 有序节点创建过程中发生错误

- CreateBuilder提供了一个withProtection方法来通知Curator客户端，在创建的有序节点前添加一个唯一标识符，如果create失败了，客户端会开始重试操作，重试操作的一个步骤就是验证是否存在一个节点包含这个唯一标识符

#### 删除节点时发生错误

- DeleteBuilder接口中定义guaranteed方法，可以对delete操作提供保障，一直重试，直到成功或Curator客户端实例不可用

### 菜谱

#### LeaderLatch（群首闩）

- 进行主节点选举操作

- LeaderLatchListener
  - isLeader
  - notLeader

#### LeaderSelector（群首选举器）

- LeaderSelectorListener
  - takeLeadership

#### PathChildrenCached（子节点缓存器）

- PathChildrenCacheListener
