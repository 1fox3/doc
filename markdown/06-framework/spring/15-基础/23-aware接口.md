# Aware接口

> 专题：Spring
> 来源：面试内容汇总/Spring.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## Aware接口

### 介绍

#### 用于提供对于Spring容器内部资源的访问，Aware能让Bean感知Spring容器的存在，即让Bean可以使用Spring容器所提供的资源

### 接口范围

#### ApplicationContextAware

- 获取ApplicationContext对象

#### BeanNameAware

- 获取当前Bean的名称

#### BeanFactoryAware

- 获取BeanFactory对象

#### BeanClassLoaderAware

- 获取加载当前Bean的ClassLoader对象

#### EnvironmentAware

- 获取Environment对象

#### ResourceLoaderAware

- 获取ResourceLoader对象

#### ServletConfigAware

- 获取ServletConfig对象

#### ServletContextAware

- 获取ServletContet对象
