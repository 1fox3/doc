# AOP

> 专题：Spring
> 来源：面试内容汇总/Spring.xmind

## 补充与实践

- 补充：Spring AOP 基于代理，事务、缓存、异步等注解都依赖代理边界。
- 实践：事务方法避免自调用，异常回滚规则要明确，跨服务事务优先采用最终一致性方案。
- 误区：`@Transactional` 默认只对运行时异常回滚，且 private/final 方法通常不会被代理增强。

## 脑图内容

## AOP

### Spring Aop和AspectJ Aop

#### Spring AOP属于运行时增强，基于代理，相对简单

#### AspectJ AOP属于编译时增强，基于字节码操作，功能更加强大

### AspectJ定义的通知类型

#### Before

#### After

#### AfterReturning

#### AfterThrowing

#### Around
