# Directory目录与Router路由服务

> 专题：Dubbo
> 来源：Dubbo.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## Directory目录与Router路由服务

### Directory目录

#### 介绍

- Directory代表了多个invoker，其内部维护者一个list，并且这个list的内容时动态变化的

#### 实现

- RegistryDirectory
  - invoker列表根据注册服务中心的推送变化而变化

- StaticDirectory
  - 消费者使用了多个注册中心时，把所有注册中心的invoker列表汇总到一个invoker列表中

#### RegistryDirectory

- 创建
  - 在消费端启动时创建

- invoker列表更新
  - 调用RegistryDiectcory的subscribe方法，并添加一个监听器，担当服务发现提供者地址发生变化后调用监听器的notify方法

- RouterChain
