# 路由网关Spring Cloud Zuul

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：新版本更推荐 Spring Cloud LoadBalancer、Gateway、OpenFeign、Resilience4j，Hystrix/Ribbon 已不是新项目首选。
- 实践：超时、重试、熔断、限流必须成套设计，错误组合会放大流量并拖垮下游。
- 排障：微服务调用问题按入口网关、注册发现、负载均衡、网络、服务线程池、下游依赖逐层定位。

## 脑图内容

## 路由网关Spring Cloud Zuul

### 作用

#### Zuul、Ribbon、Eureka相结合，可以实现只能路由和负载均衡的功能，Zuul能够将请求流量按某种策略分发到集群状态的多个服务实例

#### 网关将所有服务的API接口统一聚合，并统一对外暴露。外界系统调用API接口是，都是由网关对外暴露的API接口，外界系统不需要知道微服务系统中各服务相互调用的复杂性，微服务系统也保护了器内部微服务单元的API接口，防止器被外界直接调用，导致服务的敏感信息对外暴露

#### 网关服务可以做用户身份认证和权限认证，防止非法请求操作API接口，对服务器起到保护作用

#### 网关可以实现监控功能，实时日志输出，对请求进行记录

#### 网关可以用来实现流量监控，在高流量的情况下，对服务进行降级

#### API接口从内部服务分离出来，方便做测试

### 两大核心组件

#### 路由-Router

#### 过滤器-Filter

### 工作原理

#### Zuul是通过Servlet实现的，Zuul通过自定义的ZuulServlet（类似于Spring MVC的DispatchServlet）来对请求进行控制。

#### Zuul的核心时一系列过滤器，可以在Http请求的发起和响应返回期间执行一系列的过滤器。

- pre过滤器
  - 它是在请求路由到具体的服务之前执行的，这种类型的过滤器可以做安全验证，例如身份验证、参数验证等

- routing过滤器
  - 它用于将请求路由到具体的微服务实例。默认情况下使用Http Client进行网络请求

- post过滤器
  - 它是在请求已被路由到微服务后执行的。一般情况下，用作收集统计信息、指标、以及将响应传输到客户端

- error过滤器
  - 它是在其他过滤器发生错误时执行的

#### Zuul采取了动态读取、编译和运行这些过滤器。过滤器之间不能相互通信，而是通过RequestContext对象来共享数据，每个请求都会创建一个RequestContext对象

#### Zuul过滤器关键特性

- Type
  - Zuul的过滤器类型

- Execution Order
  - 执行顺序，Order的值越小，越先执行

- Criteria
  - 标准，过滤器执行所需的条件

- Action
  - 行动，如果符合执行条件，则执行Action

### 搭建zuul服务

#### 依赖spring-cloud-starter-netfilx-zuul

#### @EnableZuulProxy

#### zuul.prefix:/v1

- url的统一前缀，http://localhost/v1/hiapi

#### ZuulFallbackPrivider接口-熔断功能

- getRoute
  - 指定熔断功能用于哪些路由服务

- fallbackResponse
  - 快速失败时的逻辑

#### 自定义过滤器

- 实现ZuulFilter接口
  - filterType()
  - filterOrder()
  - shouldFilter()
  - Object run()
