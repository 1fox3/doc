# ApplicationContext

> 专题：Spring
> 来源：Spring.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 是什么

- `ApplicationContext` 是 `Spring` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `ApplicationContext` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `ApplicationContext`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `ApplicationContext` 展开，属于 `Spring` 的复习范围。
- 建议优先掌握：1、设置配置路径(setConfigLocations), 2、refresh()。
- 二级节点提示了主要拆分角度：1、准备刷新的上下文环境(prepareRefresh), 2、初始化BeanFactory(obtainFreshBeanFactory), 3、对BeanFactory进行功能填充(prepareBeanFactory), 4、子类扩展(postProcessBeanFactory), 5、激活BeanFactory处理器(invokeBeanFactoryPostProcessors), 6、注册拦截Bean创建的处理器(registerBeanPostProcessors), 7、初始化Message源(initMessageSource), 8、初始化消息广播器(initApplicationEventMulticaster), 9、子类扩展初始化其他Bean(onRefresh), 10、所有注册的bean中查找Listener bean 支持到消息广播器中(registerListeners)。
- 三级节点通常对应具体细节、API、机制或易错点：1、子类覆盖(initPropertySources), 2、属性验证（validateRequiredProperties), refreshBeanFactory, 1、支持SpEl语言-“#{log.level}”(setBeanExpressionResolver), 2、支持属性编辑器(addPropertyEditorRegistrar), 3、增加一些内置类(addBeanPostProcessor), 4、设置可忽略接口(ignoreDependencyInterface), 5、注册固定依赖属性(registerResolvableDependency), 6、增加对AspectJ支持(setTempClassLoader), 7、相关环境变量及属性以单例模式注册(registerSingleton)。

### 复习追问

- `1、设置配置路径(setConfigLocations)` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `2、refresh()` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## ApplicationContext

### 1、设置配置路径(setConfigLocations)

### 2、refresh()

#### 1、准备刷新的上下文环境(prepareRefresh)

- 1、子类覆盖(initPropertySources)

- 2、属性验证（validateRequiredProperties)

#### 2、初始化BeanFactory(obtainFreshBeanFactory)

- refreshBeanFactory
  - 1、创建DefaultListableBeanFactory
  - 2、指定序列化id
  - 3、定制BeanFactory(customizeBeanFactory)
    - 1、设置是否允许同名称覆盖
    - 2、设置是否允许循环依赖
    - 3、设置Qualifier和Autowired注解解析器
  - 4、加载BeanDefinitions(loadBeanDefinitions)
    - configResources
    - configLocations
  - 5、使用全局变量记录BeanFactory

#### 3、对BeanFactory进行功能填充(prepareBeanFactory)

- 1、支持SpEl语言-“#{log.level}”(setBeanExpressionResolver)

- 2、支持属性编辑器(addPropertyEditorRegistrar)
  - 自定义属性编辑器
    - 1、继承父类PropertyEditorSupport
    - 2、注册CustomEditorConfigurer.customEditors
  - Spring自带的属性编辑器
    - 1、实现PropertyEditorRegistrar接口
    - 2、注册CustomEditorConfigurer.propertyEditorRegistrars
  - 注册时机

- 3、增加一些内置类(addBeanPostProcessor)
  - ApplicationContextAwareProcessor

- 4、设置可忽略接口(ignoreDependencyInterface)
  - 主要设置依赖注入的时候忽略Aware相关bean

- 5、注册固定依赖属性(registerResolvableDependency)

- 6、增加对AspectJ支持(setTempClassLoader)

- 7、相关环境变量及属性以单例模式注册(registerSingleton)

#### 4、子类扩展(postProcessBeanFactory)

#### 5、激活BeanFactory处理器(invokeBeanFactoryPostProcessors)

- postProcessBeanFactory
  - mergeProperties
  - convertProperties
  - processProperties

#### 6、注册拦截Bean创建的处理器(registerBeanPostProcessors)

- BeanFactoryPostProcessor

- BeanPostProcessor

#### 7、初始化Message源(initMessageSource)

- MessageSource接口
  - HierarchicalMessageSource接口
    - ResourceBundleMessageSource
    - ReloadResourceBundleMessageSource(可定时刷新)

#### 8、初始化消息广播器(initApplicationEventMulticaster)

#### 9、子类扩展初始化其他Bean(onRefresh)

#### 10、所有注册的bean中查找Listener bean 支持到消息广播器中(registerListeners)

#### 11、初始化剩下的单例(finishBeanFactoryInitialization)

- ConversionService
  - 主要支持Converter接口功能

- freezeConfiguration冻结配置

- 初始化非延迟加载(将所有单例bean提前实例化)

#### 12、完成刷新并发送广播通知(finishRefresh)

- initLifecycleProcessor

- onRefresh.startBeans

- publishEvent

#### 13、destroyBean

#### 14、cancelRefresh
