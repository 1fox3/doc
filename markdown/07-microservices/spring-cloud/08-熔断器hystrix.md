# 熔断器Hystrix

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：新版本更推荐 Spring Cloud LoadBalancer、Gateway、OpenFeign、Resilience4j，Hystrix/Ribbon 已不是新项目首选。
- 实践：超时、重试、熔断、限流必须成套设计，错误组合会放大流量并拖垮下游。
- 排障：微服务调用问题按入口网关、注册发现、负载均衡、网络、服务线程池、下游依赖逐层定位。

## 详细说明

### 是什么

- `熔断器Hystrix` 是 `Spring Cloud` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `熔断器Hystrix` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `熔断器Hystrix`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `熔断器Hystrix` 展开，属于 `Spring Cloud` 的复习范围。
- 建议优先掌握：设计原则, 工作机制, RestTemplate和Ribbon使用熔断器, Feign使用熔断器, 使用Hystrix Dashboard监控熔断器状态, 使用Turbine聚合监控。
- 二级节点提示了主要拆分角度：防止单个服务的故障耗尽整个服务的Servlet容器的进程资源, 快速失败机制，如果某个服务出现故障，则调用该服务的请求快速失败，而不是等待线程, 提供回退(fallback)方案，在请求发生故障时，提供设定好的回退方案, 使用熔断机制，防止故障扩散到其他服务, 提供断路器的监控组件Hystrix Hashboard,可以实时监控熔断器的状态, 某个API接口的失败次数在一定时间内小于设定的阈值，熔断器处理关闭状态，该API接口正常提供服务, 失败次数大于阈值，Hystrix判定该API接口出现故障，打开熔断器，这时请求API皆苦指定快速失败的逻辑, 熔断器打开一段时间后处于半打开状态，一定数量的请求正常请求，剩下的快速失败，若接口正常返回则熔断器关闭，否则继续打开，这样熔断器就具有了自我修复能力, 依赖spring-cloud-starter-netflix-hystrix, @EnableHystrix。
- 三级节点通常对应具体细节、API、机制或易错点：fallbackMethod=快速失败的返回, 指定快速失败的处理类Bean, 依赖spring-cloud-starter-netflix-hystrix-dashboard, @EnableHystrixDashboard, http://localhost:8764/hysrix.stream, http://localhost:8764/hysrix, 填入：http://localhost:8769/turbine.stream, 监控间隔时间, title。

### 复习追问

- `设计原则` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `工作机制` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `RestTemplate和Ribbon使用熔断器` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `Feign使用熔断器` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `使用Hystrix Dashboard监控熔断器状态` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## 熔断器Hystrix

### 设计原则

#### 防止单个服务的故障耗尽整个服务的Servlet容器的进程资源

#### 快速失败机制，如果某个服务出现故障，则调用该服务的请求快速失败，而不是等待线程

#### 提供回退(fallback)方案，在请求发生故障时，提供设定好的回退方案

#### 使用熔断机制，防止故障扩散到其他服务

#### 提供断路器的监控组件Hystrix Hashboard,可以实时监控熔断器的状态

### 工作机制

#### 某个API接口的失败次数在一定时间内小于设定的阈值，熔断器处理关闭状态，该API接口正常提供服务

#### 失败次数大于阈值，Hystrix判定该API接口出现故障，打开熔断器，这时请求API皆苦指定快速失败的逻辑

#### 熔断器打开一段时间后处于半打开状态，一定数量的请求正常请求，剩下的快速失败，若接口正常返回则熔断器关闭，否则继续打开，这样熔断器就具有了自我修复能力

### RestTemplate和Ribbon使用熔断器

#### 依赖spring-cloud-starter-netflix-hystrix

#### @EnableHystrix

#### 在需要的接口上使用@HystrixCommand注解

- fallbackMethod=快速失败的返回

### Feign使用熔断器

#### feign.hystrix.enabled=true

#### @FeignClient(fallback=)

- 指定快速失败的处理类Bean

### 使用Hystrix Dashboard监控熔断器状态

#### RestTemplate使用Hystrix Dashboard

- 依赖spring-cloud-starter-netflix-hystrix-dashboard

- @EnableHystrixDashboard

- http://localhost:8764/hysrix.stream
  - 显示熔断器的数据指标

- http://localhost:8764/hysrix
  - 填入：http://localhost:8764/hysrix.stream
  - 监控间隔时间
  - title

#### Feign中使用Hystrix Dashboard

- 依赖spring-cloud-starter-netflix-hystrix-dashboard

- @EnableHystrixDashboard

### 使用Turbine聚合监控

#### 依赖spring-cloud-starter-netflix-turbine

#### 依赖spring-cloud-starter-actuator

#### http://localhost:8764/hysrix

- 填入：http://localhost:8769/turbine.stream

- 监控间隔时间

- title
