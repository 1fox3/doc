# SqlSession接口

> 专题：MyBatis
> 来源：面试内容汇总/MyBatis.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## SqlSession接口

### DefaultSqlSession

#### 不是线程安全的

#### 有多个共享变量，比如Configuration和Executor等，在多线程情况下可能导致数据不一致，因此不是线程安全的

### SqlSessionManager

#### 线程安全

#### 由MyBatis支持

### SqlSessionTemplate

#### 线程安全 (5)

#### 由Spring提供
