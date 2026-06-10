# 基础

> 专题：Spring
> 来源：面试内容汇总/Spring.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 是什么

- `基础` 是 `Spring` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `基础` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `基础`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 子章节

- [ApplicationContext和BeanFactory的区别](01-applicationcontext和beanfactory的区别.md)
- [获取ApplicationContext](02-获取applicationcontext.md)
- [依赖注入方式](03-依赖注入方式.md)
- [可以注入null吗？](04-可以注入null吗.md)
- [作用域（@Scope）](05-作用域scope.md)
- [如何防止相同Bean注入异常](06-如何防止相同bean注入异常.md)
- [Bean初始化进行操作,按执行顺序](07-bean初始化进行操作按执行顺序.md)
- [Bean销毁时进行操作](08-bean销毁时进行操作.md)
- [@Service,@Repository,@Controller](09-servicerepositorycontroller.md)
- [@Bean和@Component区别](10-bean和component区别.md)
- [@Bean和@Component生成同名的Bean](11-bean和component生成同名的bean.md)
- [@Autowired](12-autowired.md)
- [@Resource、@Autowired、@Inject](13-resourceautowiredinject.md)
- [@Required](14-required.md)
- [注入Java集合类型](15-注入java集合类型.md)
- [Spring自动装配](16-spring自动装配.md)
- [循环依赖](17-循环依赖.md)
- [AOP](18-aop.md)
- [通知注解](19-通知注解.md)
- [事务](20-事务.md)
- [方法异步执行](21-方法异步执行.md)
- [定时任务](22-定时任务.md)
- [Aware接口](23-aware接口.md)
- [@Import](24-import.md)
- [@Enable*](25-enable.md)
- [事件监听](26-事件监听.md)
- [可以不要XML位置文件吗](27-可以不要xml位置文件吗.md)
- [支持的缓存框架](28-支持的缓存框架.md)
- [Spring 5.0新功能](29-spring-50新功能.md)
- [Spring Native](30-spring-native.md)
