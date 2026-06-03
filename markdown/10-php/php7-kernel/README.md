# PHP7 内核剖析

> 来源：PHP7内核剖析.xmind

## 核心认知

- PHP7 内核重点包括 Zend 引擎、zval、HashTable、内存管理、OPcache、函数调用和对象模型。
- 理解引用计数、写时复制和垃圾回收有助于解释 PHP 性能与内存行为。

## 面试重点

- SAPI、生命周期、zval 结构、HashTable、内存分配、编译执行流程。
- 引用计数、循环引用回收、OPcache、函数和对象实现。

## 实践检查点

- 能解释大数组复制、引用传递和写时复制的性能影响。
- 能从 FPM、OPcache、慢日志和内存峰值定位 PHP 服务问题。

## 版本与趋势

- PHP 8.x 已成为主流演进方向，JIT、Union Types、Attributes、Fibers、Readonly 等特性需要补充了解。
- PHP7 内核知识仍可用于理解 zval、HashTable、引用计数、写时复制和 FPM 性能问题。

## 章节目录

- [PHP基础架构](01-php基础架构.md)
- [SAPI](02-sapi.md)
- [数据类型](03-数据类型.md)
- [内存管理](04-内存管理.md)
- [编译与执行](05-编译与执行.md)
- [函数](06-函数.md)
- [面向对象](07-面向对象.md)
- [命名空间](08-命名空间.md)
- [instantiate](09-instantiate.md)
