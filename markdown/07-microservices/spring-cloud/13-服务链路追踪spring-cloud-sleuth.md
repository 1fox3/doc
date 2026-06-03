# 服务链路追踪Spring Cloud Sleuth

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## 服务链路追踪Spring Cloud Sleuth

### 基本术语

#### Span

- 基本工作单元，发送一个远程调度任务就会产生一个Span

#### Trace

- 由一系列Span组成，呈树状结构

#### Annotation

- 用于记录一个时间，一些核心注解用于定义一个请求的开始和结束
  - cs-Client Sent
    - 客户端发送一个请求
  - sr-Server Received
    - 服务端获得请求并准备开始处理它，如果将其sr减去cs时间戳，可得到网络传输时间
  - ss-Server Sent
    - 服务端发送响应
  - cr-Client Received
    - 客户端接收响应

### Zipkin

#### Twitter的一个开源项目，基于Google的Dapper实现

#### 致力于收集分布式系统的链路数据，提供了数据持久化策略，也提供了面向开发者的API接口，用于查询数据，也提供了UI组件帮助用户查看链路信息

#### 支持的数据存储In-Memory，Mysql，Cassandra和ES

#### curl -sSL https://zipkin.io/quickstart.sh | bash -s java -jar zipkin.jar

#### localhost:9411

### 使用

#### Zipkin依赖spring-cloud-starter-zipkin

#### sleuth依赖spring-cloud-starter-sleuth

#### spring.sleuth.sampler.probability=1.0

- 以100%的改立将链路的数据上传给Zipkin Server，默认值为10%

#### spring.sleuth.web.client.enable=true

- 开启sleuth功能

### 在链路数据中添加自定义数据

#### @Autowired Tracer tracer;

#### tracer.currentSpan().tag("name","forezp");

### 使用RabbitMQ传输链路数据

#### zipkin.collector.rattbimq

- address（RABBIT_ADDRESS）

- password（RABBIT_PASSWORD）

- username（RABBIT_USER）

- virual-host（RABBIT_VIRTUAL_HOST）

- user-ssl=true（RABBIT_USE_SSL）

- concurrency（RABBIT_CONCURRENCY）
  - 并发消费者数量，默认为1

- connection-timeout（RABBIT_CONNECTION_TIMEOUT）

- queue（RABBIT_QUEUE）
  - 从中获取span信息的队列，默认为zipkin

### 在数据库中存储链路数据

#### zipkin.torage

- type
  - 默认为mem，Mysql，ElasticSearch、Cassandra3

- mysql.host

- mysql.port

- mysql.username

- mysql.password

- mysql.db

- mysql.max-active
  - 最大连接数，默认10

### 使用ES存储链路数据

#### zipkin.torage.elasticsearch

- hosts

- pipeline

- max-requests
  - 默认64

- timeout
  - 默认10s

- index
  - 默认zipkin

- data-separator
  - 默认“-”

- index-shrads
  - 默认5

- index-replicas

- username

- password
