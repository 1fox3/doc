# @Resource、@Autowired、@Inject

> 专题：Spring
> 来源：面试内容汇总/Spring.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## @Resource、@Autowired、@Inject

### @Resource

#### 属性

- name-名称

- type-类型

#### 逻辑

- 如果指定了name、type，则动Spring容器中找到一个名称和类型相对应的一个bean，找不到则报错

- 如果只指定了name，则从Spring容器中找到一个名称和name一样的bean，找不到则报错

- 如果只指定了type，则从Spring容器中找到一个类型和type类型一样的bean，找不到或找到多个则报错

- 如果没有指定参数，则默认找到名字装配，未找到则按类型装配，找不到则报错

### @Autowired

#### 默认按类型装配，找不到或找到多个则报错

#### 如果按名称装配，则搭配@Qualifier("name")使用

#### 默认必须装配，可指定required=false

### @Inject

#### 和@Autowired类似，可以完全提到

#### 无required参数，要求Bean必须存在

#### 按名称装配，需使用@Named("name")使用
