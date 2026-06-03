# 配置中心Spring Cloud Config

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：新版本更推荐 Spring Cloud LoadBalancer、Gateway、OpenFeign、Resilience4j，Hystrix/Ribbon 已不是新项目首选。
- 实践：超时、重试、熔断、限流必须成套设计，错误组合会放大流量并拖垮下游。
- 排障：微服务调用问题按入口网关、注册发现、负载均衡、网络、服务线程池、下游依赖逐层定位。

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
