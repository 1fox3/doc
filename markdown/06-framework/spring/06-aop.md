# AOP

> 专题：Spring
> 来源：Spring.xmind

## 补充与实践

- 补充：Spring AOP 基于代理，事务、缓存、异步等注解都依赖代理边界。
- 实践：事务方法避免自调用，异常回滚规则要明确，跨服务事务优先采用最终一致性方案。
- 误区：`@Transactional` 默认只对运行时异常回滚，且 private/final 方法通常不会被代理增强。

## 详细说明

### 是什么

- `AOP` 是 `Spring` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `AOP` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `AOP`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `AOP` 展开，属于 `Spring` 的复习范围。
- 建议优先掌握：动态代理, 静态代理。
- 二级节点提示了主要拆分角度：aspectj-autoproxy, AopNamespaceHandler.init(), AnnotationAwareAspectJAutoProxyCreator, Instrumentation, Spring开启静态代理。
- 三级节点通常对应具体细节、API、机制或易错点：AspectJAutoProxyBeanDefinitionParser.parse(), 实现BeanPostProcessor接口, Bean实例化后调用postProcessAfterInitialization, ClassFileTransformer接口, Agent.premain, <context:load-time-weaver/>, aop.xml。

### 复习追问

- `动态代理` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `静态代理` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## AOP

### 动态代理

#### aspectj-autoproxy

#### AopNamespaceHandler.init()

- AspectJAutoProxyBeanDefinitionParser.parse()
  - AopNameSpaceUtils.reqisterAspectJAnnotationAutoProxyCreatorIfNecessary
    - 1、注册或者升级AnnoatationAwareAspectJAutoProxyCreator
      - 自动注册AnnotationAwareAspectJAutoProxyCreator类
      - 如果已经存在自动代理创建起，且与现在的不一致，则根据优先级来判断到底使用哪个
    - useClassProxingIfNecessary
      - proxy-target-class
        - JDK动态代理
          - 实现了至少一个接口，代理所有实现的接口
          - 原理：运行期间创建一个接口的实现类来完成对目标对象的代理
        - CGLIB
          - 可代理实现类的所有方法
          - 1、无法通知Final方法，因为它们不能被覆写
          - 2、需将CGLIB二级制发型包放在classpath下面
          - 原理：运行期间生成代理对象的扩展子类，底层依靠ASM操作字节码实现，性能比JDK强
      - expose-proxy
        - 主要处理目标对象内部的自动调用无法实施切面中的增强
        - AopContext.currentProxy()获取当前代理类
    - registerComponentIfNecessary
      - 注册组件并通知

#### AnnotationAwareAspectJAutoProxyCreator

- 实现BeanPostProcessor接口

- Bean实例化后调用postProcessAfterInitialization
  - wrapIfNecessary
    - 1、已经处理过的直接返回
    - 2、无需处理的直接返回
    - 3、基础设施类和bean不需要自动代理直接返回
    - 4、获取增强方法或增强器
      - getAdvicesAndAdvisorsForBean
        - findEligibleAdvisors
          - findCandidateAdvisors
            - buildAspectJAdvisors(遍历所有beanName)
              - getAdvisors
                - getAdvisor
                  - getPointCut
                    - findAspectJAnnotationOnMethod
                      - Pointcut.class
                      - Before.class
                      - Around.class
                      - After.class
                      - AfterReturning.class
                      - AtterThrowing.class
                  - InstatntiationModelAwarePointCutAdvisorImpl
                    - 简单的信息封装
                    - 增强器初始化(instantiateAdvice)
                      - getAdvice
                        - AspectJMethodBeforeAdvice
                        - AspectJAroundAdvice
                        - AspectJAfterAdvice
                        - AspectJAfterReturningAdvice
                        - AspectJAfterThrowingAdvice
                - 配置了延时初始化，需要在首位加入同步初始化增强器，已保证增强使用前实例化(SyntheticInstantiationAdvisor)
                - getDeclaredFields
          - findAdvisorsThatCanApply
            - AopUtils.findAdvisorsThatCanApply
              - AopUtils.canApply
    - 5、根据获取的增强进行代理
      - createProxy
        - 1、实例化ProxyFactory并获取代理
          - 1、获取当前类属性
          - 2、添加代理接口
          - 3、封装Advisor并加入到ProxyFactory中
            - buildAdvisors
              - Advisor
              - Advice
              - AdvisorAdapter
          - 4、设置要代理的类
          - 5、子类定制入口customizeProxyFactory
          - 6、获取代理
            - proxyFactory.getProxy
              - createAopProxy
                - JdkDynamicAopProxy
                - CglibProxyFactory

### 静态代理

#### Instrumentation

- ClassFileTransformer接口

- Agent.premain

#### Spring开启静态代理

- <context:load-time-weaver/>
  - LoadTimeWeaverBeanDefinitionParser
    - isAspectJWeavingEnabled
    - weavingEnableDef.setBeanClassName
      - 注册bean(DefaultContextLoadTimeWeaver)到BeanDefinition中
        - InstrumentationLoadTimeWeaver
      - LoadTimeWeaverAwareProcessor注册到BeanFactory
        - postProcessBeforeInitialization
    - isBeanConfigurerAspectEnabled

- aop.xml
