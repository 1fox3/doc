# 配置中心Spring Cloud Config

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：新版本更推荐 Spring Cloud LoadBalancer、Gateway、OpenFeign、Resilience4j，Hystrix/Ribbon 已不是新项目首选。
- 实践：超时、重试、熔断、限流必须成套设计，错误组合会放大流量并拖垮下游。
- 排障：微服务调用问题按入口网关、注册发现、负载均衡、网络、服务线程池、下游依赖逐层定位。

## 详细说明

### 是什么

- `配置中心Spring Cloud Config` 是 `Spring Cloud` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `配置中心Spring Cloud Config` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `配置中心Spring Cloud Config`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `配置中心Spring Cloud Config` 展开，属于 `Spring Cloud` 的复习范围。
- 建议优先掌握：读取配置, 高可用, 使用Spring Cloud Bus刷新配置, 配置存储在Mysql中。
- 二级节点提示了主要拆分角度：Config Server从本地读取配置文件, Config Server从远程仓库读取配置文件, 构建Eureka Server, Config Server注册到Eureka Server, Config Client使用Eureka Server, Spring Cloud Bus使用轻量的消息代理将分布式的节点连接起来，可以用于广播配置文件的更改或者服务的监控管理。, 实现：config-client, config-server。
- 三级节点通常对应具体细节、API、机制或易错点：原理, 构建Config Server, 构建Config Client, 好处, 配置, 依赖spring-cloud-starter-netflix-eureka-server, eureka.client.register-with-eureka:false, eureka.client.fetch-registry:false, @EnableEurekaSerer, 依赖spring-cloud-starter-bus-amqp。

### 复习追问

- `读取配置` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `高可用` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `使用Spring Cloud Bus刷新配置` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `配置存储在Mysql中` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## 配置中心Spring Cloud Config

### 读取配置

#### Config Server从本地读取配置文件

- 原理
  - 所有的配置文件统一写在Config Server工程目录下
  - Config Server暴露Http API接口
  - Config Client通过调用Config Server的Http API接口来读取配置文件

- 构建Config Server
  - 依赖spring-cloud-config-server
  - @EnableConfigServer
  - spring.config.server.profile.search-locations
    - 指定配置目录

- 构建Config Client
  - 依赖spring-cloud-config-server
  - spring.cloud.config.uri
  - spring.cloud.config.fail-fast

#### Config Server从远程仓库读取配置文件

- 好处
  - 做到配置统一管理，并且可以通过Spring Cloud Bus在不人工启动程序的情况下对Config Client的配置进行刷新

- 配置
  - spring.cloud.config.git
    - uri
    - searchPaths
    - username
    - password
  - spring.cloud.config.label
    - 分支名

### 高可用

#### 构建Eureka Server

- 依赖spring-cloud-starter-netflix-eureka-server

- eureka.client.register-with-eureka:false

- eureka.client.fetch-registry:false

- @EnableEurekaSerer

#### Config Server注册到Eureka Server

#### Config Client使用Eureka Server

### 使用Spring Cloud Bus刷新配置

#### Spring Cloud Bus使用轻量的消息代理将分布式的节点连接起来，可以用于广播配置文件的更改或者服务的监控管理。

#### 实现：config-client

- 依赖spring-cloud-starter-bus-amqp

- 配置消息队列，可选kafka，rabbitmq等

- @RefreshScope

- 调用http://localhost:8762/actuator/bus-refresh?destination=eureka-client:**

### 配置存储在Mysql中

#### config-server

- spring.cloud.config.server.jdbc=true

- spring.cloud.config.server.jdbc.sql=select k,v from table where APPLICATION=? AND PROFILE=? AND LABEL=?
