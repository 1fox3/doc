# PHP基础架构

> 专题：PHP7 内核剖析
> 来源：PHP7内核剖析.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

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
