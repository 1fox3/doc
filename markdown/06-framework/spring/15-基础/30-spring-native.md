# Spring Native

> 专题：Spring
> 来源：面试内容汇总/Spring.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## Spring Native

### 无需JVM，提供了一种运行和部署Spring应用的方式，通过GraalJVM将Spring应用程序编译成原生镜像

### 与JVM的区别

#### Spring Native构建时会进行应用程序静态分析

#### Spring Native构建时会移除未被使用的组件

#### Spring Native反射、资源、动态代理需要配置化

#### Spring Native构建时的classpath是固定不变的

#### Spring Native没有类延迟加载，可执行文件包含所有内容都在启动时加载到内存

#### Spring Native构建时会运行一些代码

#### Spring Native对于Java应用程序还存在一些局限性

### 应用场景

#### Spring Cloud无服务器化

#### 以更廉价持久的方式运行Spring微服务

#### 非常适合K8S平台，如VMware Tanzu

#### 为Spring应用创建更加的容器镜像

### 优点

#### 无需JVM环境，Spring Native应用程序可以作为一个可执行文件独立部署

#### 应用即时启动，一般情况下应用启动时间小于100ms

#### 即时的峰值性能

#### 更少的内存消耗

### 缺点(与JVM应用相比)

#### 构建更笨重，构建时间更长

#### 更少的运行时优化

#### 很多java功能受限

#### 很多特性还不成熟
