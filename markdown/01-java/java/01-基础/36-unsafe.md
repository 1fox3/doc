# Unsafe

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## Unsafe

### sun.misc.Unsafe

### 单例实现

### 获取unsafe实例

#### 通过反射

#### -Xbootclasspath/a:${path},将调用unsafe的jar包路径追加到默认的bootstrap路径中

### 相关功能

#### 内存操作

- allocateMemory

- reallocateMemory

- setMemory

- copyMemory

- freeMemory

#### 内存屏障

- loadFence

- storeFence

- fullFence

#### 对象操作

- getObject

- putObject

- getIntVolatile

- putIntVolatile

- putOrderedObject

- putOrderedInt

- putOrderedLong

- allocateInstance
  - 创建对象是，不会调用类的构造方法

#### 数组操作

- arrayBaseOffset

- arrayIndexScale

#### CAS操作

- compareAndSwapObject

- compareAndSwapInt

- compareAndSwapLong

#### 线程调度

- park
  - 阻塞线程

- unpark

#### Class操作

- staticFieldOffset

- staticFieldBase

- shuouldBeInitialized

- defineClass
  - ClassLoader

- defineAnonymousClass
  - Lambda表达式

#### 系统信息

- addressSize
  - 系统指针大小

- pageSize
  - 内存页大小
