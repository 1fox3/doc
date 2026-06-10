# Ribbon

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：新版本更推荐 Spring Cloud LoadBalancer、Gateway、OpenFeign、Resilience4j，Hystrix/Ribbon 已不是新项目首选。
- 实践：超时、重试、熔断、限流必须成套设计，错误组合会放大流量并拖垮下游。
- 排障：微服务调用问题按入口网关、注册发现、负载均衡、网络、服务线程池、下游依赖逐层定位。

## 详细说明

### 是什么

- `Ribbon` 是 `Spring Cloud` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `Ribbon` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `Ribbon`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `Ribbon` 展开，属于 `Spring Cloud` 的复习范围。
- 建议优先掌握：RestTemplate, 结合RestTemplate使用, Ribbon核心类, RibbonLoadBalanceClient-C, ILoadBalancer-I。
- 二级节点提示了主要拆分角度：Spring Resources中一个访问第三方RESTful API接口的网络请求框架。, 负载均衡方式, 使用方式, 目前用于生产环境的模块, 引入Eureka Client依赖spring-cloud-starter-eureka, 引入Ribbon依赖spring-cloud-starter-ribbon, @EnableEurekaClient, 向IOC容器注入RestTempalte的Bean，并加上@LoadBalanced注解, 实现原理, LoadBalanceClient。
- 三级节点通常对应具体细节、API、机制或易错点：一种是独立进程单元，通过负载均衡策略，将请求转发到不同的执行单元上，例如Nginx, 另一种是将负载均衡逻辑以代码的形式封装到服务消费者的客户端上，服务消费者维护了一份服务提供者的信息列表，有了信息列表，通过负载均衡策略将请求分摊给多个服务提供者，从而达到负载均衡的目的，Ribbon就是基于此方式, 和RestTemplate相结合, 和Feign相结合, ribbon-loadbalancer, ribbon-eureka, ribbon-core, LoadBalancerAutoConfiguration维护了一个被@LoadBalance修饰的RestTemplate列表，并给列表中的RestTemplate对象添加了一个拦截器。在拦截器的方法中，将远程调度方法交给了Ribbon的负载均衡器LoadBalanceClient去处理，从而达到了负载均衡的目的, choose方法, 可禁止调用Eureka Client获取注册列表。

### 复习追问

- `RestTemplate` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `结合RestTemplate使用` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `Ribbon核心类` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `RibbonLoadBalanceClient-C` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `ILoadBalancer-I` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## Ribbon

### RestTemplate

#### Spring Resources中一个访问第三方RESTful API接口的网络请求框架。

### Ribbon

#### 负载均衡方式

- 一种是独立进程单元，通过负载均衡策略，将请求转发到不同的执行单元上，例如Nginx

- 另一种是将负载均衡逻辑以代码的形式封装到服务消费者的客户端上，服务消费者维护了一份服务提供者的信息列表，有了信息列表，通过负载均衡策略将请求分摊给多个服务提供者，从而达到负载均衡的目的，Ribbon就是基于此方式

#### 使用方式

- 和RestTemplate相结合

- 和Feign相结合

#### 目前用于生产环境的模块

- ribbon-loadbalancer
  - 可以独立使用或与其他模块一起使用的负载均衡器API

- ribbon-eureka
  - Ribbon结合Eureka客户端的API，为负载均衡器提供动态服务注册列表信息

- ribbon-core
  - Ribbon的核心API

### 结合RestTemplate使用

#### 引入Eureka Client依赖spring-cloud-starter-eureka

#### 引入Ribbon依赖spring-cloud-starter-ribbon

#### @EnableEurekaClient

#### 向IOC容器注入RestTempalte的Bean，并加上@LoadBalanced注解

#### 实现原理

- LoadBalancerAutoConfiguration维护了一个被@LoadBalance修饰的RestTemplate列表，并给列表中的RestTemplate对象添加了一个拦截器。在拦截器的方法中，将远程调度方法交给了Ribbon的负载均衡器LoadBalanceClient去处理，从而达到了负载均衡的目的

### Ribbon核心类

#### LoadBalanceClient

- choose方法
  - 轮询的方式返回服务实例

#### ribbon.eureka.enable=false

- 可禁止调用Eureka Client获取注册列表

#### stores.ribbon.listOfServers

- 配置服务实例的Url

### RibbonLoadBalanceClient-C

#### LoadBalanceClient-I

- ServiceInstanceChooser-I

- choose方法
  - 根据serviceId获取实例

#### execute()

- 2个重载方法

#### reconstructURI

- 重构Url

### ILoadBalancer-I

#### addServers

- 添加一个server集合

#### chooseServer

- 根据key获取server

#### markServerDown

- 标记某个服务下线

#### getReachableServers

- 获取可用server集合

#### getAllservers

- 获取所有server集合

### IClientConfig

#### 用于配置负载均衡的客户端

### IRule

#### 负载均衡策略

#### BestAvailableRule

- 选择最小请求数

#### ClientConfigEnabledRoundRobinRule

- 轮询

#### RandomRule

- 随机

#### RoundRobinRule

- 轮询选择server

#### RetryRule

- 根据轮询的方式重试

#### WeightResponseTimeRule

- 根据响应时间去分配一个weight，weight越低，被选择的可能性就越低

#### ZoneAvoidanceRule

- 根据server的zone区域和可用性来轮询选择

### IPing

#### 用于判断server是否有响应，从而判定server是否可用

#### 默认每10秒中ping一次

#### PingUrl

- 真实去ping某个url，判断其是否可用

#### PingConstant

- 固定返回某个服务是否可用，默认返回true，即可用

#### NoOpPing

- 不去ping,直接返回true，即可用

#### DummyPing

- 直接返回true，并实现initWithNiwsConfig方法

#### NIWSDiscoverPing

- 根据DiscovertEnabledServer的InstanceInfo的InstanceStatus去判断，如果为InstanceStatus，UP，则可用，否则不可用
