# ApplicationContext和BeanFactory的区别

> 专题：Spring
> 来源：面试内容汇总/Spring.xmind

## 补充与实践

- 补充：Spring 6 要求 Java 17+ 并迁移到 Jakarta 命名空间，理解 Bean 生命周期仍是排查问题的基础。
- 实践：复杂初始化逻辑优先使用明确的生命周期回调，避免在构造器里访问尚未注入完成的依赖。
- 误区：三级缓存只能解决部分单例 setter 循环依赖，构造器循环依赖和原型循环依赖无法靠它解决。

## 脑图内容

## ApplicationContext和BeanFactory的区别

### ApplicationContext是BeanFactory的子接口。BeanFactory时一种更加基础的容器实现，它提供了最基础的IOC功能，而ApplicationContext则提供了更多企业级的高级功能

### BeanFactory

#### 懒加载

#### 使用语法显示提供资源对象

#### 不支持国际化

#### 不支持基于依赖的注解

### ApplicationContext

#### 即时加载

#### 自己创建和管理资源对象

#### 支持国际化

#### 支持基于依赖的注解
