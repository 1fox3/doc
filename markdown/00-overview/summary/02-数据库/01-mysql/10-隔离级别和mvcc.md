# 隔离级别和MVCC

> 专题：重点汇总
> 来源：重点汇总.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## 隔离级别和MVCC

### 事务一致性问题

#### 脏写

- 一个事务修改了另一个未提交事务修改过的数据

#### 脏读

- 一个事务读到了另一个未提交事务修改过的数据

#### 不可重复读

- 一个事务修改了另一个未提交事务读取的数据

#### 幻读

- 如果一个事务根据某些搜索条件查询出一些记录，在该事务未提交时，另一个事务写入了一些符合那些搜索条件的记录

### 隔离级别

#### READ UNCOMMITTED

#### READ COMMITTED

- 脏读

#### REPEATABLE READ

- 不可重复读

#### SERIALIZABLE

- 幻读

### MVCC

#### 记录中的roll_pointer与undo日志中的roll_pointer连在一起，称为记录的版本链

#### ReadView(一致性视图)

- 构成
  - m_ids
    - 在生成ReadView时，当前系统中活跃的读写事务id列表
  - min_trx_id
    - 在生成ReadView时，当前系统中活跃的读写事务中最小的事务id，也就是m_ids中的最小值
  - max_trx_id
    - 在生成ReadView时，系统应该分配给下一个事务的事务id值
  - creator_trx_id
    - 生成该ReadView的事务的事务id

- 记录某个版本的可见性判断
  - 版本中的trx_id等于creator_trx_id，可见
  - 版本中的trx_id小于min_trx_id，可见
  - 版本中的trx_id大于等于max_trx_id,不可见
  - 版本中的trx_id在min_trx_id和max_trx_id之间
    - 在m_ids中，不可见
    - 不在m_ids中，可见

- 创建时机
  - READ COMMITTED
    - 每次读取数据前都会生成一个ReadView
  - REPEATABLE READ
    - 在第一次读取数据时生成一个ReadView
    - 当以START TRANSACTION WITH CONSISTENT SNAPSHOT 语句开启事务时，会在该语句执行后，立即生成一个ReadView

#### 二级索引

- ReadView中的min_trx_id是否大于该页面的PAGE_MAX_TRX_ID属性值，如果大于，则整个页面可见，否则，回表之后再判断可见性

### purge操作

#### 清除不需要的undo日志和打了删除标记的记录
