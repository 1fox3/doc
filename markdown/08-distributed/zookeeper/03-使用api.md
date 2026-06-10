# 使用API

> 专题：ZooKeeper
> 来源：ZooKeeper.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 是什么

- `使用API` 是 `ZooKeeper` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `使用API` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `使用API`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `使用API` 展开，属于 `ZooKeeper` 的复习范围。
- 建议优先掌握：创建会话, 命令, 获取管理权。
- 二级节点提示了主要拆分角度：ZooKeeper(String connectString, int sessionTimeout, Watcher watcher), stat, dump, 创建节点, 查看节点, 异步创建节点, 异步查看节点。
- 三级节点通常对应具体细节、API、机制或易错点：connectionString, sessionTimeout, watcher, 查看会话信息, 查看还有多长时间过期, create方法, getData方法。

### 复习追问

- `创建会话` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `命令` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `获取管理权` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## 使用API

### 创建会话

#### ZooKeeper(String connectString, int sessionTimeout, Watcher watcher)

- connectionString
  - 主机名和ZooKeeper的端口，服务器列表

- sessionTimeout
  - ZooKeeper等待客户端通信的最长时间，即超时时间

- watcher
  - 用于处理会话事件的一个对象

### 命令

#### stat

- 查看会话信息

#### dump

- 查看还有多长时间过期

### 获取管理权

#### 创建节点

- create方法
  - 参数
    - path
    - data
    - OPEN_ACL_UNSAFE
    - CreateMode.EPHEMERAL
  - 异常
    - KeeperException
      - ConnectionLossException
    - InterruptedException

#### 查看节点

- getData方法
  - 参数
    - path
    - watch
    - stat

#### 异步创建节点

- create方法
  - 参数
    - path
    - data
    - acl
    - createMode
    - AsyncCallback（回调）
      - processResult（回调方法）
        - rc
          - OK或KeeperExpection异常对应的编码值
        - path
        - ctx
        - name
          - znode节点名称
      - 只有一个单独的线程处理所有的回调调用，如果回调函数阻塞，则后续回调函数都阻塞
    - ctx

#### 异步查看节点

- getData方法
  - 参数
    - path
    - watch
    - stat
    - DataCallback
      - processResult
        - rc
        - path
        - ctx
        - data
        - stat
