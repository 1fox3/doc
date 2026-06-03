# Undo日志

> 专题：重点汇总
> 来源：重点汇总.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## Undo日志

### 事务id

#### 分配时机

- 对于只读事务来说，只有它在第一次对某个用户创建的临时表执行增删改操作时，才会分配一个事务id

- 对于写事务来说，只有它在第一次对某个表执行增删改操作时，才会分配一个事务id

#### 生成方式

- 服务器会在内存中维护一个全局变量，每当需要为某个事务分配id时，就会把该变量的值当做事务id分配给事务

- 每当这个变量的值为256的倍数时，就会将该变量的值刷新到系统表空间的页号为5的页面中一个名为Max Trx ID的属性中

- 当系统重启时，会将这Max Trx ID属性加载到内存中，将该值加上256之后赋值给前面提到的全局变量

#### trx_id隐藏列

### roll_pointer

#### 指向记录对应的undo日志的指针

### undo日志格式

#### INSERT

- TRX_UNDO_INSERT_REC
  - end of record
  - undo_type
  - undo_no
    - 在一个事务中undo no是从0开始递增的
  - table_id
  - <len, value>
  - start of record

- 仅记录聚簇索引对应的日志，非聚簇索引在回滚时，执行对应的删除操作即可

#### DELETE

- 删除过程
  - 将记录的delete_record标识设置为1
  - 事务提交后，会有专门的线程把该记录从链表中移除并加入到垃圾链表中，然后再调整一些页面的其他信息

- TRX_UNDO_DEL_MARK_REC
  - end of record
  - undo type
  - undo no
  - table id
  - info bits
    - 记录头信息的前4个bit的信息
  - trx_id
  - roll_pointer
  - <len, value>
  - len of index_col_info
    - 索引列各列信息部分的大小
  - <pos, len, value>
    - 被索引列的各列信息
  - start of record

#### UPDATE

- 不更新主键
  - 就地更新
  - 先删除旧记录再插入新记录
  - TRX_UNDO_UPD_EXIST_REC
    - end of record
    - undo type
    - undo no
    - table id
    - info bits
      - 记录头信息的前4个bit的信息
    - trx_id
    - roll_pointer
    - <len, value>
    - n_updated
      - 共有多少列被更新了
    - <pos,old_len,old_value>
      - 被更新的列更新前信息
    - len of index_col_info
      - 索引列各列信息部分的大小
    - <pos, len, value>
      - 被索引列的各列信息
    - start of record

- 更新主键
  - 删除
    - 增加删除undo日志
  - 添加新记录
    - 增加insert的undo日志

### undo日志页

#### FIL_PAGE_UNDO_LOG

- Undo Page Header
  - TRX_UNDO_PAGE_TYPE
  - TRX_UNDO_PAGE_START
  - TRX_UNDO_PAGE_FREE
  - TRX_UNDO_PAGE_NODE
    - 链表结构点，用于指向前一个和后一个节点

#### 一个事务undo日志分为2个链表

- insert undo链表

- update undo链表

#### 普通表和临时表的undo日志分开记录

#### undo页仅在需要的时候才会申请内存

#### 不同事务的undo日志分开记录

### 重用undo页面

#### 基本原则

- 该链表中仅包含一个undo页面

- 该页面已使用的空间小于整体页面的3/4

#### insert undo链表

- 事务提交后，可直接进行覆盖使用

#### update undo链表

- 不能立即删除掉，不能覆盖之前的日志，仅能在后面追加

### 回滚段

#### 存放了各个undo页面链表的first undo page的页号，这些页号被称为undo slot

#### FIL_NULL

- 标识该undo slot不执行任何页面

#### 从回滚段中申请页面链表

- 从回滚段中的一个页面开始遍历，查看FIL_NULL标识
  - 如果是FIL_NULL，那么就在表空间创建一个段，让后从这个段中的申请一个页面作为undo页面链表的first undo page，最后把该undo slot的值设置为刚刚申请的这个页面地址，这也就意味着这个undo slot被分配给了这个事务
  - 如果不是FIL_NULL，说明该undo slot已经指向了一个undo链表，需跳到下一个undo slot

#### 分类

- 0号
  - 系统表空间

- 33~127号
  - 既可以时系统表空间，也可以在自己配置的undo表空间

- 1~32号
  - 临时表空间

### roll_pointer (7)

#### is_insert

- 表示执行的undo日志是否为TRX_UNDO_INSERT大类的undo日志

#### rseg_id

- 表示该指针指向的undo日志的回滚段编号

#### page_number

- 表示该指针指向的undo日志所在的页面页号

#### offset

- 表示该指针指向的undo日志在页面中的偏移量

### 为事务分配Undo页面链表的过程

#### 事务在执行过程中对普通表的记录进行首次改动前，首先在系统表空间的第5号页面申请一个回滚段

#### 分配到回滚段后，优先从2个cached的链表中申请已缓存的undo slot

#### 如果没有换粗你的undo slot可用，则到Rollback Segment Header页面中找到一个可用的undo slot分配给当前事务

#### 找到可用的undo slot后，若果undo slot是从cached链表中获取的，那么它对应的Undo Log Segment就已经分配了；否则需要重新分配一个Undo Log Segment，然后从该Undo Log Segment中申请一个页面作为Undo页面链表的first undo page，并把该页号填入获取的undo slot中

#### 事务把undo日志写入到上面申请的undo页面链表中

### 回滚段配置

#### innodb_rollback_segments

- 普通表空间回滚段数
  - 小于等于33，依次配置为准
  - 大于33，则以此配置减去32为准

#### innodb_undo_directory

- 指定undo表空间所在的目录，默认是数据目录

#### innodb_undo_tablespaces

- 定义undo表空间的数量，默认为0表示不创建任何undo表空间

### undo日志在崩溃恢复是的作用

#### 遍历128个回滚段中的undo slot，从中找出不为FIL_NULL的undo slot

#### undo slot第一个页面中的Undo Log Segment Header中的TRX_UNDO_STATE属性为TRX_UNDO_ACTIVE

#### 然后从Undo Log Segment Header中的TRX_UNDO_LAST_LOG属性，找到最后一个Undo Log Header的位置

#### 从该Undo Log Header中找到对应的事务id和其他一些信息

#### 然后通过undo日志中记录的信息将该事务对页面所做的更改全部回滚掉
