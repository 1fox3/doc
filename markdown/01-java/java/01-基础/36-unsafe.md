# Unsafe

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 核心概念

- `Unsafe` 是 JDK 内部提供的底层能力类，可以直接操作内存、对象字段、CAS、线程挂起恢复等。
- 它绕过了 Java 的部分安全检查，因此名字叫 Unsafe。

### 常见能力

- 堆外内存分配和释放。
- CAS 原子操作。
- 按字段偏移量读写对象字段。
- 线程 park/unpark。
- 绕过构造器创建对象。

### 实践建议

- 业务代码不应直接使用 Unsafe。
- 并发工具、Netty、序列化框架等底层组件可能间接使用它。
- 现代 Java 更推荐使用 VarHandle、ByteBuffer、Foreign Function & Memory API 等替代方向。

### 复习检查

- 能用自己的话解释 `Unsafe`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `Unsafe` 展开，属于 `Java 语言基础` 的复习范围。
- 建议优先掌握：sun.misc.Unsafe, 单例实现, 获取unsafe实例, 相关功能。
- 二级节点提示了主要拆分角度：通过反射, -Xbootclasspath/a:${path},将调用unsafe的jar包路径追加到默认的bootstrap路径中, 内存操作, 内存屏障, 对象操作, 数组操作, CAS操作, 线程调度, Class操作。
- 三级节点通常对应具体细节、API、机制或易错点：allocateMemory, reallocateMemory, setMemory, copyMemory, freeMemory, loadFence, storeFence, fullFence, getObject, putObject。

### 复习追问

- `sun.misc.Unsafe` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `单例实现` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `获取unsafe实例` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `相关功能` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

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
