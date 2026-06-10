# 整合MyBatis

> 专题：Spring
> 来源：Spring.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 是什么

- `整合MyBatis` 是 `Spring` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `整合MyBatis` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `整合MyBatis`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `整合MyBatis` 展开，属于 `Spring` 的复习范围。
- 建议优先掌握：MyBatis配置文件, SqlSessionFactory创建, MapperFactoryBean创建, MapperScannerConfigurer。
- 二级节点提示了主要拆分角度：configuration：根元素, properties：定义配置外在化, settings：全局性配置, typeAliases：为一些类定义别名, typeHandlers：定义类型处理，JAVA类型与数据库中的类型之间的转换关系, objectFactory：用于指定结果对象的实例是如何创建的, plugins：MyBatis的插件，插件可以修改MyBatis的运行规则, environments：配置MyBatis的环境, environment：配置MyBatis的环境, transactionManager：事务管理器。
- 三级节点通常对应具体细节、API、机制或易错点：InitializingBean接口(afterPropertiesSet), FactoryBean接口(getObject), processPropertyPlaceHolders(修改bean属性), scanner.registerFilters(生成过滤器来控制扫描结果), ClassPathMapperScanner.scan。

### 复习追问

- `MyBatis配置文件` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `SqlSessionFactory创建` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `MapperFactoryBean创建` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `MapperScannerConfigurer` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## 整合MyBatis

### MyBatis配置文件

#### configuration：根元素

#### properties：定义配置外在化

#### settings：全局性配置

#### typeAliases：为一些类定义别名

#### typeHandlers：定义类型处理，JAVA类型与数据库中的类型之间的转换关系

#### objectFactory：用于指定结果对象的实例是如何创建的

#### plugins：MyBatis的插件，插件可以修改MyBatis的运行规则

#### environments：配置MyBatis的环境

#### environment：配置MyBatis的环境

#### transactionManager：事务管理器

#### dataSource：数据源

#### mappers：指定映射文件或映射类

### SqlSessionFactory创建

#### SqlSessionFactoryBean类

- InitializingBean接口(afterPropertiesSet)

- FactoryBean接口(getObject)

### MapperFactoryBean创建

#### MapperFactoryBean类

- InitializingBean接口(afterPropertiesSet)
  - checkDaoConfig
    - 1、父类验证sqlSessionFactory是否存在
    - 2、映射接口验证
    - 3、映射文件存在验证
  - initDao(模板方法，留给子类扩展使用)

- FactoryBean接口(getObject)
  - getSqlSession().getMapper()

### MapperScannerConfigurer

#### InitializingBean接口(afterPropertiesSet)

#### BeanFactoryPostProcessor接口(postProcessBeanFactory)

#### BeanDefinitionRegistryPostProcessor接口(postProcessBeanDefinitionRegistry)

- processPropertyPlaceHolders(修改bean属性)
  - 1、找到所有以注册的PropertyResourceConfigurer类型的bean
  - 2、模拟Spring中的环境来调用处理器

- scanner.registerFilters(生成过滤器来控制扫描结果)
  - annotationClass(AnnotationTypeFilter)
  - markerInterface(AssignableTypeFilter)
  - 不扫描package-info.java文件

- ClassPathMapperScanner.scan
  - findCandidateComponents(扫描包路径下的文件并生成相应的bean)
    - isCandidateComponent(判断文件是否符合要求)
