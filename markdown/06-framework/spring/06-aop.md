# AOP

> 专题：Spring
> 来源：Spring.xmind

## 补充与实践

- 补充：Spring AOP 基于代理，事务、缓存、异步等注解都依赖代理边界。
- 实践：事务方法避免自调用，异常回滚规则要明确，跨服务事务优先采用最终一致性方案。
- 误区：`@Transactional` 默认只对运行时异常回滚，且 private/final 方法通常不会被代理增强。

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
