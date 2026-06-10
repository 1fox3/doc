# PHP基础架构

> 专题：PHP7 内核剖析
> 来源：PHP7内核剖析.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 是什么

- `PHP基础架构` 是 `PHP7 内核剖析` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `PHP基础架构` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `PHP基础架构`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `PHP基础架构` 展开，属于 `PHP7 内核剖析` 的复习范围。
- 建议优先掌握：PHP7的变化, PHP源码目录, 声明周期。
- 二级节点提示了主要拆分角度：抽象语法树, Native TLS, 执行函数参数和返回值类型, zval结构变化, 异常处理, HashTable变化, 执行器, 新的参数解析方式, SAPI, main。
- 三级节点通常对应具体细节、API、机制或易错点：代码解析生成抽象语法树，然后经抽象语法树编译为ZendVM指令。, 使得PHP的编译器与执行器很好的隔离开, 线程局部存储，用于保存线程的资源池, 通过_thread标识一个全局变量，这个全局变量线程独享, struct _zval_struct, PHP5.x会直接抛error错误的情况，PHP7改为了抛出异常, execute_data、opline采用寄存器变量存储, PHP应用接口层, PHP的主要代码, ZendVM，即PHP解析器的主要实现。

### 复习追问

- `PHP7的变化` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `PHP源码目录` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `声明周期` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## PHP基础架构

### PHP7的变化

#### 抽象语法树

- 代码解析生成抽象语法树，然后经抽象语法树编译为ZendVM指令。

- 使得PHP的编译器与执行器很好的隔离开

#### Native TLS

- 线程局部存储，用于保存线程的资源池

- 通过_thread标识一个全局变量，这个全局变量线程独享

#### 执行函数参数和返回值类型

#### zval结构变化

- struct _zval_struct
  - zvalue_value value
    - union _zvalue_value
      - long lval
      - duble dval
      - struct {char * val, int len} str
      - HashTable *ht
      - zend_object_value obj
      - zend_ast *ast
  - zend_unit refcount_gc
    - PHP7之前存在zval中
    - PHP7存在zvalue中
  - zend_uchar type
  - zend_uchar is_ref_gc
    - 是否为引用

#### 异常处理

- PHP5.x会直接抛error错误的情况，PHP7改为了抛出异常

#### HashTable变化

#### 执行器

- execute_data、opline采用寄存器变量存储

#### 新的参数解析方式

### PHP源码目录

#### SAPI

- PHP应用接口层

#### main

- PHP的主要代码

#### Zend

- ZendVM，即PHP解析器的主要实现

#### ext

- PHP扩展目录

#### TSRM

- 线程安全相关实现

### 声明周期

#### 模块初始化阶段

- php_module_startup()
  - 激活SAPI
  - 启动PHP输出
  - 初始化垃圾回收器
  - 启动Zend引擎
    - 启动内存池
    - 设置一些util函数句柄
    - 设置Zend虚拟机编译、执行器的函数句柄，以及垃圾回收函数的函数句柄
    - 分配函数、类、常量符号表
    - 注册Zend核心扩展
    - 注册Zend定义的标准常量
    - 注册$GLOBALS超全局变量的获得handler
    - 分配php.ini配置的存储符号表EG
  - 注册PHP定义的常量
    - PHP_VERSION
    - PHP_ZTS
    - PHP_SAPI
  - 解析php.ini
    - php.ini配置保存在configuration_hash哈希表中
  - 映射PHP、Zend核心的php.ini配置
    - 根据解析出的php.ini，获取对应的配置值，将最终的配置插入EG
  - 注册相关变量的handler
    - $_GET
    - $_POST
    - $_COOKIE
    - $_SERVER
    - $_ENV
    - $_REQUST
    - $_FILES
  - 注册静态编译的扩展
  - 注册动态加载的扩展
  - 回调各扩展定义的module startup钩子函数
    - PHP_MINIT_FUNCTION
  - 注册php.ini中禁用的函数
    - disable_functions
    - disable_classes

#### 请求初始化阶段

- php_request_startup()
  - 激活输出
  - 激活Zend引擎
    - 重置垃圾回收器
    - 初始化编译器
    - 初始化执行器
    - 初始化词法扫描器
  - 激活SAPI
  - 回调各扩展定义的request startup函数

#### 执行脚本阶段

- php_execute_script()
  - 编译
    - PHP源代码到抽象语法树再到opline指令的转化过程
  - 执行
    - zend引擎执行opline指令

#### 请求关闭阶段

- php_request_shutdown()
  - flush输出内容
  - 发送HTTP应答header头
  - 清理全局变量
  - 关闭编译器
  - 关闭执行器
  - 回调request shutdown钩子函数

#### 模块关闭阶段

- php_module_shutdown()
  - 清理持久化符号表
  - 清理模块注册
  - 调用个扩展的shutdown函数
  - 清理扩展globals
  - 注销扩展提供的内部函数
  - 清理ini
  - 销毁EG
  - 关闭输出
  - 释放PG
