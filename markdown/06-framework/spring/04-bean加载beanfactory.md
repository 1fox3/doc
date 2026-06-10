# Bean加载(BeanFactory)

> 专题：Spring
> 来源：Spring.xmind

## 补充与实践

- 补充：Spring 6 要求 Java 17+ 并迁移到 Jakarta 命名空间，理解 Bean 生命周期仍是排查问题的基础。
- 实践：复杂初始化逻辑优先使用明确的生命周期回调，避免在构造器里访问尚未注入完成的依赖。
- 误区：三级缓存只能解决部分单例 setter 循环依赖，构造器循环依赖和原型循环依赖无法靠它解决。

## 详细说明

### 是什么

- `Bean加载(BeanFactory)` 是 `Spring` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `Bean加载(BeanFactory)` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `Bean加载(BeanFactory)`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `Bean加载(BeanFactory)` 展开，属于 `Spring` 的复习范围。
- 建议优先掌握：加载主过程, FactoryBean, 循环依赖。
- 二级节点提示了主要拆分角度：1、转换对应的beanName, 2、尝试从缓存中加载单例, 3、bean实例化, 4、原型模式依赖检查, 5、检测parentBeanFactory, 6、BeanDefinition类型转换, 7、寻找依赖, 8、针对不同的模式创建bean, 9、类型转换, getObject。
- 三级节点通常对应具体细节、API、机制或易错点：transformedBeanName, getSingleton, getObjectForBeanInstance, isPrototypeCurrentlyInCreating, getParentBeanFactory, getMergedLocalBeanDefinition, dependsOn, isSingleton, isPrototype, getScope。

### 复习追问

- `加载主过程` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `FactoryBean` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `循环依赖` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## Bean加载(BeanFactory)

### 加载主过程

#### 1、转换对应的beanName

- transformedBeanName

#### 2、尝试从缓存中加载单例

- getSingleton
  - 流程
    - 1、检查缓存中是否存在实例
    - 2、检查提前曝光中是否存在实例
    - 3、获取单例工厂
    - 4、获取单例并放到提前曝光缓存中
    - 5、删除单例工厂中对应的bean名
  - 相关定义
    - singletonObjects
    - singletonFactories
    - earlySingletonObjects
    - registeredSingletons

#### 3、bean实例化

- getObjectForBeanInstance
  - 流程
    - 1、对FactoryBean正确性验证
    - 2、若获取的是工厂则直接返回此实例
    - 3、从缓存中获取实例
    - 4、创建实例
      - doGetObjectFromFactoryBean
        - 1、factory.getObject
        - 2、postProcessObjectFromFactoryBean(BeanPostPorcessor)

#### 4、原型模式依赖检查

- isPrototypeCurrentlyInCreating

#### 5、检测parentBeanFactory

- getParentBeanFactory

#### 6、BeanDefinition类型转换

- getMergedLocalBeanDefinition

#### 7、寻找依赖

- dependsOn

#### 8、针对不同的模式创建bean

- isSingleton
  - getSingleton
    - 1、检查缓存是否已加载过
    - 2、记录beanName正在加载的状态
    - 3、加载单例前置处理
    - 4、获取单例实例
    - 5、加载单例后置处理
    - 6、修改缓存并删除各种辅助状态
    - 7、返回处理结果

- isPrototype

- getScope

#### 9、类型转换

- getTypeConvert().convertIfNecessary

### FactoryBean

#### getObject

#### isSingleton

#### getObjectType

### 循环依赖

#### 构造器循环依赖

- 无法解决

#### setter循环依赖

- 提前曝光单例工厂方法处理

#### prototype范围依赖

- 无法解决
