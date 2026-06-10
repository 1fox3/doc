# Redo日志

> 专题：MySQL
> 来源：面试内容汇总/Mysql.xmind

## 补充与实践

- 补充：InnoDB 通过 undo log 和 ReadView 实现 MVCC，通过 redo log 保证崩溃恢复，通过 binlog 支持复制和归档。
- 实践：长事务会拖住 undo 清理并影响版本链，线上应限制事务时长和交互式事务。
- 误区：可重复读不等于完全不会幻读，InnoDB 通过 next-key lock 在当前读场景解决幻读。

## 详细说明

### 是什么

- `Redo日志` 是 `MySQL` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `Redo日志` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `Redo日志`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `Redo日志` 展开，属于 `MySQL` 的复习范围。
- 建议优先掌握：只将事务执行过程中产生的redo日志刷新到磁盘的好处, 日志格式, 无主键情况下，row_id隐藏列赋值, Mini-Transaction, redo log block, redo log buffer, redo日志刷盘时机, redo日志文件组。
- 二级节点提示了主要拆分角度：redo日志占用空间非常小, redo日志时顺序写入磁盘的, type, space ID, page number, data, 服务器会在内存中维护一个全局变量，每当向某个包含row_id隐藏列的表中插入一条记录时，就会把这个全局变量的值当做新纪录的row_id的值，并且把这个全局变量自增1, 每当这个全局变量的值为256的倍数时，就会将该变量的值刷新到系统表空间页号为7的页面中一个名为Max Row ID的属性中, 当系统启动时，会将这个Max Row ID属性加载到内存中，并将该值加上256之后赋值给前面提到的全局变量, 定义。
- 三级节点通常对应具体细节、API、机制或易错点：这条redo日志的类型, 表空间ID, 页号, redo日志的具体内容, 对底层页面进行一次原子访问的过程, LOG_BLOCK_HDR_NO, LOG_BLOCK_HDR_DATA_LEN, LOG_BLOCK_FIRST_REC_GROUP, LOG_BLOCK_CHECKPOINT_NO。

### 复习追问

- `只将事务执行过程中产生的redo日志刷新到磁盘的好处` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `日志格式` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `无主键情况下，row_id隐藏列赋值` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `Mini-Transaction` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `redo log block` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## Redo日志

### 只将事务执行过程中产生的redo日志刷新到磁盘的好处

#### redo日志占用空间非常小

#### redo日志时顺序写入磁盘的

### 日志格式

#### type

- 这条redo日志的类型
  - MLOG_1BYTE
  - MLOG_2BYTE
  - MLOG_4BYTE
  - MLOG_8BYTE
  - MLOG_WRITE_STRING
  - MLOG_REC_INSERT
  - MLOG_COMP_REC_INSERT
  - MLOG_COMP_PAGE_CREATE
  - MLOG_COMP_REC_DELETE
  - MLOG_COMP_LIST_START_DELETE
  - MLOG_COMP_LIST_END_DELETE
  - MLG_ZIP_PAGE_COMPRESS
  - MLOG_MULTI__REC_END

#### space ID

- 表空间ID

#### page number

- 页号

#### data

- redo日志的具体内容

### 无主键情况下，row_id隐藏列赋值

#### 服务器会在内存中维护一个全局变量，每当向某个包含row_id隐藏列的表中插入一条记录时，就会把这个全局变量的值当做新纪录的row_id的值，并且把这个全局变量自增1

#### 每当这个全局变量的值为256的倍数时，就会将该变量的值刷新到系统表空间页号为7的页面中一个名为Max Row ID的属性中

#### 当系统启动时，会将这个Max Row ID属性加载到内存中，并将该值加上256之后赋值给前面提到的全局变量

### Mini-Transaction

#### 定义

- 对底层页面进行一次原子访问的过程

#### 一个事务可以包含若干条语句，每一条语句又包含若干个MTR，每个MTR又可以包含若干条redo日志

### redo log block

#### log block header

- LOG_BLOCK_HDR_NO

- LOG_BLOCK_HDR_DATA_LEN

- LOG_BLOCK_FIRST_REC_GROUP

- LOG_BLOCK_CHECKPOINT_NO

#### log block body

#### log block trailer

### redo log buffer

#### innodb_log_buffer_size默认16MB

#### 由若干个连续的redo log block组成

#### buf_free指明后续redo日志需要写入的位置

### redo日志刷盘时机

#### log buffer空间不足时

#### 事务提交时

#### 将某个脏页刷新到磁盘时

#### 后台有个进程每秒一次的频率将log buffer中的redo日志刷新到磁盘

#### 正常关闭服务器时

#### 做checkpoint时

### redo日志文件组

#### innodb_log_group_home_dir

#### innodb_log_file_size

#### innodb_log_file_in_group

### lsn(log sequence number)

#### 记录当前已经写入的日志量

#### flush_to_disk_lsn

- 表示刷新到磁盘中的redo日志量的全局变量

#### checkpoint_lsn

- 当前系统中可以被覆盖的redo日志总量

### 崩溃恢复

#### 确定恢复起点

- 比较checkpoint1和checkpoint2这2个block中的checkpoint_no值的大小

#### 确定恢复终点

- 普通block的log block header部分中有一个LOG_BLOCK_HDR_DATA_LEN的属性来记录当前block中使用了多少字节，只要这个值不等于512就好

#### 恢复过程

- 使用hash表，对redo日志按照页面进行聚合

- 跳过已经刷新到磁盘中的页面
