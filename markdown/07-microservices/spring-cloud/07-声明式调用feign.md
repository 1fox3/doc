# 声明式调用Feign

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：新版本更推荐 Spring Cloud LoadBalancer、Gateway、OpenFeign、Resilience4j，Hystrix/Ribbon 已不是新项目首选。
- 实践：超时、重试、熔断、限流必须成套设计，错误组合会放大流量并拖垮下游。
- 排障：微服务调用问题按入口网关、注册发现、负载均衡、网络、服务线程池、下游依赖逐层定位。

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
