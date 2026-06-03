# 熔断器Hystrix

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：新版本更推荐 Spring Cloud LoadBalancer、Gateway、OpenFeign、Resilience4j，Hystrix/Ribbon 已不是新项目首选。
- 实践：超时、重试、熔断、限流必须成套设计，错误组合会放大流量并拖垮下游。
- 排障：微服务调用问题按入口网关、注册发现、负载均衡、网络、服务线程池、下游依赖逐层定位。

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
