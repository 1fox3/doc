# ApplicationContext

> 专题：Spring
> 来源：Spring.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

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
