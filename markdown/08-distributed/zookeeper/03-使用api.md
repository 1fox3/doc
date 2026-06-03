# 使用API

> 专题：ZooKeeper
> 来源：ZooKeeper.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

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
