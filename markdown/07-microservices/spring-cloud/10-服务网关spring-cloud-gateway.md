# 服务网关(Spring Cloud Gateway)

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：新版本更推荐 Spring Cloud LoadBalancer、Gateway、OpenFeign、Resilience4j，Hystrix/Ribbon 已不是新项目首选。
- 实践：超时、重试、熔断、限流必须成套设计，错误组合会放大流量并拖垮下游。
- 排障：微服务调用问题按入口网关、注册发现、负载均衡、网络、服务线程池、下游依赖逐层定位。

## 详细说明

### 是什么

- `服务网关(Spring Cloud Gateway)` 是 `Spring Cloud` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `服务网关(Spring Cloud Gateway)` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `服务网关(Spring Cloud Gateway)`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `服务网关(Spring Cloud Gateway)` 展开，属于 `Spring Cloud` 的复习范围。
- 建议优先掌握：Spring Cloud官网退出的第二代网关框架, 作为整个分布式系统流量入口的作用, 核心组件, 核心原理, 断言工厂, 过滤器。
- 二级节点提示了主要拆分角度：Netflix Zuul是基于Servlet的，采用HttpClient进行请求转发，使用阻塞模式, Spring Cloud Gateway使用非阻塞模式，性能优于Netflix Zuul, 协议转换，路由转发, 流量聚合，对流量进行监控，日志输出, 作为整个系统的前端工程，对流量进行控制，有限流作用, 作为系统的前端边界，外部流量只能通过网关才能访问系统, 可以在网关层做权限判断, 可以在网关层做缓存, 路由-Router, 过滤器-Filter。
- 三级节点通常对应具体细节、API、机制或易错点：用来判定请求到底交给哪个Gateway Web Handler处理, DateTime, Cookie, Header, Host, Method, Path, QueryParam, RemoteAddr, 针对单个路由的网关过滤器。

### 复习追问

- `Spring Cloud官网退出的第二代网关框架` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `作为整个分布式系统流量入口的作用` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `核心组件` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `核心原理` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `断言工厂` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## 服务网关(Spring Cloud Gateway)

### Spring Cloud官网退出的第二代网关框架

#### Netflix Zuul是基于Servlet的，采用HttpClient进行请求转发，使用阻塞模式

#### Spring Cloud Gateway使用非阻塞模式，性能优于Netflix Zuul

### 作为整个分布式系统流量入口的作用

#### 协议转换，路由转发

#### 流量聚合，对流量进行监控，日志输出

#### 作为整个系统的前端工程，对流量进行控制，有限流作用

#### 作为系统的前端边界，外部流量只能通过网关才能访问系统

#### 可以在网关层做权限判断

#### 可以在网关层做缓存

### 核心组件

#### 路由-Router

#### 过滤器-Filter

#### 断言-Predicate

- 用来判定请求到底交给哪个Gateway Web Handler处理

### 核心原理

#### 请求首先交个Gateway Handler Mapping处理，如果请求与路由匹配（会用到断言），则将其发送到响应的Gateway Web Handler处理

#### Gateway Web Handler处理请求时会经过一些列的过滤链。

### 断言工厂

#### 断言（Predicate）来自原Java8的接口。该接口接收一个入参，放回一个布尔值，包含多种默认方法将断言组合成其他复杂的逻辑（如：与，或，非）

#### RoutePredicateFactory

- DateTime
  - AfterRoutePredicateFactory
    - 请求时间在配置的时间之后
  - BeforeRoutePredicateFactory
    - 请求时间在配置的时间之前
  - BetweenRoutePredicateFactory
    - 请求事件在配置的时间之间

- Cookie
  - CookieRoutePredicateFactory
    - 请求携带的Cookie满足配置的值

- Header
  - HeaderRoutePredicateFactory
    - 请求携带的Header满足配置的值

- Host
  - HostRoutePredicateFactory
    - 请求的Host满足配置的值

- Method
  - MethodRoutePredicateFactory
    - 请求Method满足配置的值

- Path
  - PathRoutePredicateFactory
    - 请求路径满足配置的值

- QueryParam
  - QueryParamRoutePredicateFactory
    - 请求参数满足配置的值

- RemoteAddr
  - RemoteAddrRoutePredicateFactory
    - 请求地址满足配置的值

### 过滤器

#### 从作用范围划分

- 针对单个路由的网关过滤器
  - GatewayFilter

- 针对所有路由的全局网关过滤器
  - GlobalFilter

#### 过滤器工厂

- AddRequestHeader GatewayFilter Factory
  - 添加请求头网关过滤器工厂

- AddRequestParameter GatewayFilter Factory
  - 添加请求参数网关过滤器工厂

- AddResponseHeader GatewayFilter Factory
  - 添加响应头网关过滤器工厂

- Hystrix GatewayFilter Factory
  - Hystrix熔断的网关过滤器工厂

- PrefixPath GatewayFilter Factory
  - PrefixPath的网关过滤器工厂

- PreserveHostHeader GatewayFilter Factory
  - 保留原请求头的过滤器工厂

- RequestRateLimiter GatewayFilter Factory
  - 请求限流的网关过滤器工厂

- RedirectTo GatewayFilter Factory
  - 重定向的网关过滤器工厂

- RemoveRequestHeader GatewayFilter Factory
  - 删除请求头的网关过滤器工厂

- RemoveResponseHeader GatewayFilter Factory
  - 删除响应头的网关过滤器工厂

- RewritePath GatewayFilter Factory
  - 重写路径的网关过滤器工厂

- SaveSession GatewayFilter Factory
  - 保存会话的网关过滤器工厂

- SecureHeaders GatewayFilter Factory
  - 安全头的网关过滤器工厂

- SetPath GatewayFilter Factory
  - 设置路径的网关过滤器工厂

- SetResponseHeader GatewayFilter Factory
  - 设置响应头的网关过滤器工厂

- SetStatus GatewayFilter Factory
  - 设置状态的网关过滤器工厂

- StripPrefix GatewayFilter Factory
  - StripPrefix的网关过滤器工厂

- Retry GatewayFilter Factory
  - 重试的网关过滤器工厂

#### 自定义过滤器

- 实现GatewayFilter和Ordered接口

- 通过RouteLocator将过滤器注册到路由中

#### 自定义过滤器工程

- 继承如下虚类
  - AbstractGatewayFilterFactory
    - 接收一个参数
  - AbstractNameValueGatewayFilterFactory
    - 接收两个参数

- @Bean的方式注入到IoC容器中

#### 全局过滤器

- 不需要在配置文件中配置，作用在所有路由上，最终通过GatewayFilterAdapter包装成GatewayFilterChain可识别的过滤器

- 内置GlobalFilter
  - LoadBalancer
    - 负载均衡客户端过滤器
      - LoadBalancerClientFilter
  - HttpClient
    - Http客户端相关过滤器
      - NettyRouteFilter
      - NettyWriteResponseFilter
  - Websocket
    - Websocket相关过滤器
      - WebsocketRoutingFilter
  - FowardPath
    - 路径转发过滤器
      - FowardPathFilter
  - RouteToRequestUrl
    - 转发路由Url过滤器
      - RouteToRequestUrlFilter
  - WebClient
    - WebClient相关过滤器
      - WebClientHttpRoutingFilter
      - WebClientWriteResponseFilter

- 自定义
  - 实现GlobalFilter和Ordered接口
  - @Bean的方式注入IOC容器

### 限流

#### 常见方式

- Hystrix适用线程池隔离，当超过线程池负载时，走熔断逻辑

- Tomcat通过限制线程数来控制并发

- 通过时间窗口的平均速度来控制流量

#### 限流算法

- 计数器算法

- 漏桶算法

- 令牌桶算法

#### 只提供了RequestRateLimiterGatewayFilterFactory

- 使用Redis和lua脚本实现令牌桶算法进行限流

- 依赖spring-boot-starter-data-redis-reactive

- 相关配置
  - burstCapacity
    - 令牌桶总容量
  - replenishRate
    - 令牌桶每秒的平均填充速率
  - key-resolver
    - 用于限流的键的解析器的Bean对象名字，#{@beanName}
