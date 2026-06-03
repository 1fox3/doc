# Redo日志

> 专题：MySQL
> 来源：Mysql.xmind

## 补充与实践

- 补充：InnoDB 通过 undo log 和 ReadView 实现 MVCC，通过 redo log 保证崩溃恢复，通过 binlog 支持复制和归档。
- 实践：长事务会拖住 undo 清理并影响版本链，线上应限制事务时长和交互式事务。
- 误区：可重复读不等于完全不会幻读，InnoDB 通过 next-key lock 在当前读场景解决幻读。

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
