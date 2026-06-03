# Spring Cloud OAuth2保护微服务系统

> 专题：Spring Cloud
> 来源：SpringCloud.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## Spring Cloud OAuth2保护微服务系统

### OAuth2

#### 一个标准的授权协议

#### OAuth2允许不同的客户端通过认证和授权的形式来访问被其保护起来的资源

#### 角色划分

- 服务提供方Authorization Server

- 资源持有者Resource Server

- 客户端Client

#### 认证流程

- 资源持有者（用户）打开客户端，客户端询问用户授权

- 用户同意授权

- 客户端向授权服务器申请授权

- 授权服务器对客户端进行认证，也包括用户信息的认证，认证成功后授权给予令牌

- 客户端获取令牌后，携带令牌向资源服务器请求资源

- 资源服务器确认令牌正确无误，向客户端释放资源

### Spring OAuth2

#### OAuth2 Provider

- 职责
  - OAuth2 Provider通过管理和验证OAuth2令牌来控制客户端是否有权限访问被其保护的资源
  - OAuth2 Provider还必须为用户提供认证API接口
    - 根据认证API接口，用户提供账号和密码等信息，来确认客户端是否可以被OAuth2 Provider授权
  - 负责公开被OAuth2保护起来的资源
  - 需要配置代表用户的OAuth2客户端信息，被用户允许的客户端就可以访问被OAuth2保护的资源

- 角色
  - Authorization Service
    - 配置
      - 实现AuthorizationServerConfigurer，并加上@EnableAuthorizationServer
      - 注入如下3个配置
        - ClientDetailsServiceConfigurer
          - 配置客户端信息，可放在内存也可放在数据库中
          - clientId
            - 客户端Id,需在Authorization Server中是唯一的
          - secret
            - 客户端的密码
          - scope
            - 客户端的域
          - authorizedGrantTypes
            - 认证类型
          - authorities
            - 权限信息
        - AuthorizationServerEndpointsConfigurer
          - 配置授权Token的节点和Token服务，默认开启除密码类型的所有验证类型
          - authenticationManager
            - 配置该项，开启密码认证
          - userDetailsService
            - 配置获取用户认证信息的接口
          - authorizationCodeServices
            - 配置管理implict验证的状态
          - tokenGranter
            - 配置Token Granter
          - token管理策略
            - InMemoryStore
            - JdbcTokenStore
            - JwtTokenStore
        - AuthorizationServerSecurityConfigurer
          - 配置Token节点的安全策略
          - @EnableAuthorizationServer
  - Resource Service
    - 开启@EnableResourceServer
    - 使用ResourceServerConfigurer配置
      - tokenServices
        - ResourceServerTokenServices
        - RemoteTokenServices
      - resourceId
        - 配置资源Id

- 节点
  - 授权节点/oauth/authorize
  - 获取Token节点/oauth/token

#### OAuth2 Client

- Protected Resource Configuration(受保护资源配置)
  - Id
    - 资源的Id
  - clientId
    - OAuth2 Client的Id
  - clientSecret
    - 客户端密码
  - accessTokenUri
    - 获取Token的API节点
  - scope
    - 客户端的域
  - clientAuthenticationScheme
    - 客户端验证类型，Http Basic（默认），Form
  - userAuthorizationUri
    - 如果用户需要授权访问资源，则用户被重定向到的认证Url

- Client Configuration(客户端配置)
  - @EnableOAuth2Client
  - 创建一个Bean（Id为oauth2ClientContextFilter），用来存储当前请求和上下文的请求
  - 在Request域内创建AccessTokenRequest类型的Bean
