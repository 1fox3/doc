# Bean加载(BeanFactory)

> 专题：Spring
> 来源：Spring.xmind

## 补充与实践

- 补充：Spring 6 要求 Java 17+ 并迁移到 Jakarta 命名空间，理解 Bean 生命周期仍是排查问题的基础。
- 实践：复杂初始化逻辑优先使用明确的生命周期回调，避免在构造器里访问尚未注入完成的依赖。
- 误区：三级缓存只能解决部分单例 setter 循环依赖，构造器循环依赖和原型循环依赖无法靠它解决。

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
