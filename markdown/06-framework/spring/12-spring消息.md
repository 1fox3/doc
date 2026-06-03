# Spring消息

> 专题：Spring
> 来源：Spring.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## Spring消息

### JmsTemplate

### MessageListener

#### SimpleMessageListenerContainer

- 处理固定数量的JMS会话，不支持事务

#### DefaultMessageListenerContainer

- 建立在SimplMessageListenerContainer容器智商，添加了对事务的支持
  - concurrentConsumers消息监听器数量
  - sheduleNewInvoker
    - invokeListener
      - doReceiveAndExecute
        - doExecuteListener

#### ServerSessionMessage.ListenerContainer

- 可支持石湖湾，允许动态管理JMS会话
