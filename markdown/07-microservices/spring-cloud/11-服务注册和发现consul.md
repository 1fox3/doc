# 服务注册和发现Consul

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：新版本更推荐 Spring Cloud LoadBalancer、Gateway、OpenFeign、Resilience4j，Hystrix/Ribbon 已不是新项目首选。
- 实践：超时、重试、熔断、限流必须成套设计，错误组合会放大流量并拖垮下游。
- 排障：微服务调用问题按入口网关、注册发现、负载均衡、网络、服务线程池、下游依赖逐层定位。

## 脑图内容

## 服务注册和发现Consul

### 简介

#### 使用Go语言编写

#### 提供了分布式系统的服务注册和发现、配置等功能，每个功能都可单独使用，也可一起使用构建全方位的服务网格

#### 使用分布式一会协议RAFT算法实现，有多数据中心的高可用方案

### 基本术语

#### 代理（Agent）

#### 客户端（Client）

#### 服务端（Server）

#### 数据中心

#### 共识

#### Gossip

#### LAN Gossip

- 局域网Gossip

#### WAN Gossip

- 仅包含服务端的WAN Gossip池。

#### 远程调用RPC

### 功能

#### 服务发现

#### 运行时健康检查

#### KV存储

#### 安全服务通信

#### 多数据中心

### Consul的原理

#### 每个提供服务的节点都运行了Consul的代理（Agnet）

#### 代理节点可以和一个或多个Consul服务端通信。Consul服务端是存储和复制数据的节点，采用RAFT算法保证了数据一致性，并选出领导者

#### 需要发现服务，可查询任意数据中心的Consul服务端或Consul客户端，Consul客户端会将查询转发给Consul服务端

### 基本架构

#### 同一数据中心的所有节点都加入了Gossip协议，意味着Gossip协议包含该数据中心的所有节点

- 这样做的好处
  - 不需要在客户端上配置服务端地址，服务发现都是自动完成的
  - 检测节点故障的工作不放在服务端上，而是分布式的，是的故障检测比心跳机制更高的扩展性
  - 数据中心可被用作消息传递层，比如发生领导者选举等重要时间时起到通知作用

#### 领导者负责所有查询和事务，非领导者需将请求转发给领导者

### 与Eureka的区别

#### Eureka是Netflix公司开源的服务注册中心组件

#### 通常Eureka客户端使用嵌入式SDK来注册和发现服务

#### 相比Eureka，Consul提供了更多高级功能， 包括更丰富的运行时健康检查，键值存储和多数据中兴的相互感知

#### Eureka使用注册列表复制的方式提供弱一致的服务视图，Consul使用Raft算法提供强一直的保证。

### 命令

#### consul agent dev

- 运行一个consul agent

#### consul join IP

- 将agent加入consul集群

#### consul members

- 列出consul cluster集群中的members

### 服务提供者consul-provider

#### 依赖spring-cloud-starter-consul-discovery

#### @EnableDiscoveryClient

### Spring Cloud Consul Config做配置中心

#### 依赖spring-cloud-starter-consul-config

#### spring.cloud.consul.config配置项

- enabled
  - 设置config是否启用，默认true

- format
  - 设置配置的值得格式，yaml，properties

- prefix
  - 配置的基本目录

- defaultContext
  - 默认的配置，被所有的应用读取

- profileSepartor
  - 配置分割符，默认“,”

- data-key
  - 为应用配置的key名字，值为整个应用配置的字符串

### 动态刷新配置

#### 在需要动态刷新的类上加@RefreshScope

#### 使用Spring Cloud Config Bus

### 注意

#### consul支持的KV存储的value值不能超过512KB

#### 在dev模式启动下，所有数据存储在内存中，重启时所有数据丢失

#### 非dev模式启动，支持数据持久化，数据不会丢失
