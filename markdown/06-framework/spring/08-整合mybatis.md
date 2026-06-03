# 整合MyBatis

> 专题：Spring
> 来源：Spring.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

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
