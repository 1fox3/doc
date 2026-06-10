# Curator

> 专题：ZooKeeper
> 来源：ZooKeeper.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 是什么

- `Curator` 是 `ZooKeeper` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `Curator` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `Curator`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `Curator` 展开，属于 `ZooKeeper` 的复习范围。
- 建议优先掌握：Curator客户端, 流畅式API, 监听器, 状态转换, 两种边界情况, 菜谱。
- 二级节点提示了主要拆分角度：CuratorFramework, CuratorListener, UnhandledErrorListener, Connected, Suspended, Reconnected, Lost, READ_ONLY, 有序节点创建过程中发生错误, 删除节点时发生错误。
- 三级节点通常对应具体细节、API、机制或易错点：并不是Curator所独有的功能，而是通过ZooKeeper启用该选项, CreateBuilder提供了一个withProtection方法来通知Curator客户端，在创建的有序节点前添加一个唯一标识符，如果create失败了，客户端会开始重试操作，重试操作的一个步骤就是验证是否存在一个节点包含这个唯一标识符, DeleteBuilder接口中定义guaranteed方法，可以对delete操作提供保障，一直重试，直到成功或Curator客户端实例不可用, 进行主节点选举操作, LeaderLatchListener, LeaderSelectorListener, PathChildrenCacheListener。

### 复习追问

- `Curator客户端` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `流畅式API` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `监听器` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `状态转换` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `两种边界情况` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

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
