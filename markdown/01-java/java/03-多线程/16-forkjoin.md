# ForkJoin

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## ForkJoin

### 介绍

#### JDK7开始提供

#### 任务拆分，任务结果再合并，与MapReduce类似

### 底层机制

#### 工作窃取（work-stealing）算法

#### 被窃取任务的线程从队列尾部获取任务，窃取任务的线程从双端队列的头部获取任务

### 核心类

#### ForkJoinPool

- execute
  - 异步执行任务，无返回结果

- invoke，invokeAll
  - 异步执行任务，等待完成才返回结果

- submit
  - 异步执行任务，并返回一个Future对象

#### ForkJoinTask

- 实际执行的任务类

- RecursiveAction
  - 无返回结果

- RecursiveTask
  - 有返回结果

### 注意点

#### 任务拆解的很深，系统内的线程数量堆积，导致系统性能严重下降

#### 若函数的调用栈很深，会导致栈内存溢出

### parallelStream

#### 基于ForkJoin实现

#### 默认启动与CPU核数相同的线程

- java.unit.concurrent.ForkJoinPool.common.parallelism配置线程数量

#### 坑

- 事务不共享

- 不能访问主线程本地变量

- 非线程安全
