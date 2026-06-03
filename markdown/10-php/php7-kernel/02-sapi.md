# SAPI

> 专题：PHP7 内核剖析
> 来源：PHP7内核剖析.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## SAPI

### Cli

#### 相关参数

- -r
  - 直接执行php代码

- -v
  - php版本

- -m
  - 输出已安装的扩展

- -c
  - 执行php.ini配置

#### 提供了一个内置WEB服务器，仅可用于本地开发是，不可用于线上

- 也是一个独立的SAPI

### Fpm

#### FastCGI

#### 多进程模型

- 一个master进程和多个worker进程组成

- 一个worker进程只能同时处理一个请求

- master通过共享内存获取worker进程信息

- 可监听多个端口，每个端口对应一个worker pool，每个worker pool对应多个worker进程

#### php-fpm.conf

#### worker处理流程

- 等待请求

- 解析请求

- 请求初始化

- 执行php脚本

- 关闭请求

#### master进程管理

- 管理方式（pm）
  - 静态模式（static）
    - worker进程数固定不变，按最大初始化进程数
  - 动态模式（dynamic）-默认
  - 按需模式（ondemand）
    - 有请求时才创建worker进程

- 信号
  - SIGINT、SIGTERM、SIGQUIT
    - 退出fpm
  - SIGUSR1
    - 重新加载日志文件
  - SIGUSER2
    - 重启fpm
  - SIGCHLD
    - 子进程退出时发送给父进程

- 默认每秒都会检查worker进程状态，以便创建或关闭worker进程

- 如需关闭worker进程，会关闭最老的那个

### Embed

#### 主要用于提供给第三方应用使用，编译后为普通的库文件

#### enabme-embed=[shared|static]指定库类型，默认shared

#### 编译后代码位置

- PHP_HOME/lib

- PHP_HOME/include/php/sapi

#### 实现

- 相关api
  - php_embed_init()
  - php_embed_shutdown()
