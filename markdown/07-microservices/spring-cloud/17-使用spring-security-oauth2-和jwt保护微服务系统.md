# 使用Spring Security OAuth2 和JWT保护微服务系统

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## 使用Spring Security OAuth2 和JWT保护微服务系统

### JWT

#### 简介

- JSON Web Token 是一种开放的标准，JWT定义了一种紧凑且自包含的标准，该标准旨在将各个主题的信息包装为JSON对象

- 常使用HMAC算法或RSA(公钥/私钥的非对称性加密)算法对JWT进行签名，安全性很好

- 特点
  - 紧凑性
    - 由于是加密后的字符串，JWT数据体积非常小，可通过POST请求或HTTP请求头发送
  - 自包含
    - JWT包含了主题的所有信息，所以避免了每个请求都要向Uaa服务验证身份，降低了服务器的负载

#### 结构（以“.”分割）

- Header(头)
  - tpy(令牌类型，默认JWT)
  - alg(算法类型)
    - HMAC
    - SHA256
    - RSA

- Payload(有效载荷)
  - 信息

- Signature(签名)
  - 将Base64编码后的Header、Payload和密钥进行签名

#### 应用场景

- 认证

- 信息交换

#### 依赖

- spring-security-jwt
