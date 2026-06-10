# Eureka

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 是什么

- `Eureka` 是 `Spring Cloud` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `Eureka` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `Eureka`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `Eureka` 展开，属于 `Spring Cloud` 的复习范围。
- 建议优先掌握：作用, 相似, 划分, 基本架构, 基础概念。
- 二级节点提示了主要拆分角度：服务注册和发现, Zookeeper, Consul, Eureka Server, Eureka Client, Register Service, Provider Service, Consumer Service, 依赖Spring-cloud-starter-netflix-eureka-server, 相关配置。
- 三级节点通常对应具体细节、API、机制或易错点：服务注册中心, 客户端, 服务提供者, 服务消费者, eureka.instance.prefer-ip-address=true, eureka.client.registerWithEureka=false, eureka.client.fetchRegistry=false, 服务注册, 服务续约, Eureka Client默认每隔30秒发送一次心跳来进行服务续约。

### 复习追问

- `作用` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `相似` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `划分` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `基本架构` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `基础概念` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## Eureka

### 作用

#### 服务注册和发现

### 相似

#### Zookeeper

#### Consul

### 划分

#### Eureka Server

- 服务注册中心

#### Eureka Client

- 客户端

### 基本架构

#### Register Service

- 服务注册中心

#### Provider Service

- 服务提供者

#### Consumer Service

- 服务消费者

### Eureka Server

#### 依赖Spring-cloud-starter-netflix-eureka-server

#### 相关配置

- eureka.instance.prefer-ip-address=true
  - 提交IP信息

- eureka.client.registerWithEureka=false
  - 防止注册自己

- eureka.client.fetchRegistry=false
  - 防止注册自己

#### @EnableEurekaServer

### Eureka Client

#### 依赖spring-cloud-starter-netfilx-eureka-client

#### @EnableEurekaClient

### 基础概念

#### Register

- 服务注册

#### Renew

- 服务续约

- Eureka Client默认每隔30秒发送一次心跳来进行服务续约

- Eureka Server在90秒内未收到Eirela Client心跳，则将Eureka Client实例从注册列表中删除

#### Fetch Registries

- 获取服务注册列表信息

- Eureka Client默认每隔30秒更新一次

#### Cancel

- 服务下线

- DiscoveryManager.getInstance().shutdownComponent()

#### Eviction

- 服务剔除

- Eureka Server在90秒内未收到Eirela Client心跳，则将Eureka Client实例从注册列表中删除

### 高可用

#### 架构

- Eureka Client又分为Application Service 和Application Client，即服务提供者和服务消费者

- 每个区域有一个Eureka集群，并且每个区域至少有一个Eureka Server可以处理区域故障，以防服务瘫痪

#### Register服务注册

- client注册
  - DiscoveryClient类
    - EurekaClient接口
      - LookupService接口
  - 服务注册方法register()
    - 通过HTTP请求注册
  - InstanceInfoReplicator.run方法调用register方法
  - InstanceInfoReplictor.initScheduledTasks开启注册，并启动定时任务向EurekaServer服务续约

- Server
  - EurekaBootStrap
  - PeerAwareInstanceRegistryImpl
    - 服务注册，并将注册信息同步到其他Eureka Server
    - 注册列表信息保存在一个Map中
  - PeerEurekaNodes

- Renew服务续约
  - client:DiscoveryClient.renew
  - server:InstanceResource.renewLease
  - 相关配置
    - eureka.instance.leaseRenewalIntervalInSeconds=30
    - eureka.instance.leaseExpirationDurationInSeconds=90

#### Eureka Client获取服务实例慢的原因

- Eureka Client的注册延迟
  - Eureka Client启动之后，默认延迟40秒会发起注册

- Eureka Server的响应缓存
  - Eureka Server每30秒维护一次响应缓存，即刚注册的实例，并不会立即出现在服务注册列表中
  - eureka.server.responseCacheUpdateIntervalMs

- Eureka Client的缓存
  - Eureka Client保留注册表信息的缓存，默认30秒更新一次

- LoadBalancer的缓存
  - Ribbon的负载平衡器从本地的Eureka Client获取服务注册列表。Ribbon本身还维护了缓存，默认30秒刷新一次
  - ribbon.ServerListRefreshInterval

#### Eureka的自我保护机制

- 当Eureka Server接收到的服务续约基于配置的百分比，则开启自我保护模式
  - 默认15分钟低于85%

- 注册列表不会删除

- eureka.server.enable-self-preservation:true
  - 该功能默认开启

#### 搭建Eureka Server集群

- eurela.client.serviceUrl.defaultZone
