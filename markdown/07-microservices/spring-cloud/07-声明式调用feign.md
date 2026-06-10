# 声明式调用Feign

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：新版本更推荐 Spring Cloud LoadBalancer、Gateway、OpenFeign、Resilience4j，Hystrix/Ribbon 已不是新项目首选。
- 实践：超时、重试、熔断、限流必须成套设计，错误组合会放大流量并拖垮下游。
- 排障：微服务调用问题按入口网关、注册发现、负载均衡、网络、服务线程池、下游依赖逐层定位。

## 详细说明

### 是什么

- `声明式调用Feign` 是 `Spring Cloud` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `声明式调用Feign` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `声明式调用Feign`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `声明式调用Feign` 展开，属于 `Spring Cloud` 的复习范围。
- 建议优先掌握：采用了声明式API接口的风格，将Java Http客户端绑定到它的内部, 使用, FeignClientsConfiguration, Feign是一个伪Java Http客户端，Feign不做任何请求处理。Feign通过注解生成Request模板，从而简化了Http API的开发。, FeignClientRegistrar, SynchronousMethodHandler, Http Client。
- 二级节点提示了主要拆分角度：依赖spring-cloud-starter-openfeign, @EnableFeignClients, @FeignClient, 使用@Bean注册Retryer的bean, 用于创建声明式API接口，该接口应该是RESTful风格, name和value, url, decode404, configuration, fallback。
- 三级节点通常对应具体细节、API、机制或易错点：依赖Ribbon和Hystrix, 接口上加上此注解用来声明一个FeignClient, value-远程服务的服务名, configuration-指定配置类, 被调用的服务ServiceId, 直接硬编码接口地址, 404是被解码还是抛异常, 指明FignClient的配置类，默认配置类为FeignClientsConfiguration类，在缺省的情况下，这个类注入了默认的Decoder，Encoder和Contract等配置的Bean, 配置熔断器的处理类, Decoder。

### 复习追问

- `采用了声明式API接口的风格，将Java Http客户端绑定到它的内部` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `使用` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `FeignClientsConfiguration` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `Feign是一个伪Java Http客户端，Feign不做任何请求处理。Feign通过注解生成Request模板，从而简化了Http API的开发。` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `FeignClientRegistrar` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## 声明式调用Feign

### 采用了声明式API接口的风格，将Java Http客户端绑定到它的内部

### 使用

#### 依赖spring-cloud-starter-openfeign

- 依赖Ribbon和Hystrix

#### @EnableFeignClients

#### @FeignClient

- 接口上加上此注解用来声明一个FeignClient

- value-远程服务的服务名

- configuration-指定配置类

#### 使用@Bean注册Retryer的bean

### @FeignClient

#### 用于创建声明式API接口，该接口应该是RESTful风格

#### name和value

- 被调用的服务ServiceId

#### url

- 直接硬编码接口地址

#### decode404

- 404是被解码还是抛异常

#### configuration

- 指明FignClient的配置类，默认配置类为FeignClientsConfiguration类，在缺省的情况下，这个类注入了默认的Decoder，Encoder和Contract等配置的Bean

#### fallback

- 配置熔断器的处理类

### FeignClientsConfiguration

#### 默认注入配置如下

- Decoder
  - ResponseEntityDecoder

- Encoder
  - SpringEncoder

- Logger
  - Slf4jLogger

- Contract
  - SpringMvcContract

- Feign.Builder
  - HystrixFeign.Builder

#### @ConditionalOnMissingBean

#### 可重写FeignClientsConfiguration类中的Bean，覆盖掉默认的Bean，从而达到自定义配置的目的

### Feign是一个伪Java Http客户端，Feign不做任何请求处理。Feign通过注解生成Request模板，从而简化了Http API的开发。

#### 开发人员可以使用注解的方式定制Request API模板。在发送Http Rquest之前，Feign通过处理注解的方式替换掉Request模板中的参数，生成真正的Request，并交给Java Http客户端去处理。

### FeignClientRegistrar

#### 扫描被@FeignClient注解的接口

#### 使用JDK代理，拦截方法调用

### SynchronousMethodHandler

#### 分局参数生成RequstTempalte对象，并转成Requst对象，通过Http Client获取Response

### Http Client

#### HttpUrlConnection（默认）

#### 使用HttpClient

- feign.httpclient.enabled=true

- 引入HttpClient依赖
  - groupId:io.github.openfeign
  - artifactId:feign-httpclient

#### 使用Okhttp

- feign.okhttp.enabled=true

- 引入okhttp依赖
  - groupId:io.github.openfeign
  - artifactId:feign-okhttp

### 负载均衡

#### LoadBalancerFeignClient
