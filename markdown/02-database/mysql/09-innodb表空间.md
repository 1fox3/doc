# InnoDB表空间

> 专题：MySQL
> 来源：Mysql.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## InnoDB表空间

### 区

#### 定义

- 对于16KB的页来说，连续的64个页就是一个区，一个区默认1MB

### 组

#### 定义 (2)

- 256个区为一组

### 表空间

#### 第一个组的最开始的3个页面时固定的

- FSP_HDR
  - 这个类型用来登记整个表空间的一些整体属性以及本组所有的区的属性

- IBUF_BITMAP
  - 用来存储关于Change Buffer的一些信息

- INODE
  - 这个类型的页面存储了许多称为INODE Entry的数据结构

#### 其余各组最开始的2个页面时固定的

- XDES
  - 用来登记本组256个区的属性(FSP_HDR与XDES作用类似，不过FSP_HDR还额外存储了一些关于表空间的属性)

- IBUF_BITMAP
  - 用来存储关于Change Buffer的一些信息

### 段

#### B+树种叶子节点为一段，非叶子节点为一段

#### 结构(INODE Entry)

- Segment ID

- NOT_FULL_N_USED
  - Not Full 链表中已经使用了多少个页面

- 3个List Base Node
  - FREE链表
  - NOT_FULL链表
  - FULL链表

- Magic Number

- Fragment Array Entry
  - 零散页面

### 碎片区

#### 不属于具体的段，属于表空间

### XDES Entry

#### 结构

- Segment ID

- ListNode
  - 可以将若干个XDES Entry结构串成一个链表

- State

- Page State Bitmap

#### 链表分类

- FREE链表

- FREE_FRAG链表

- FULL_FRAG链表

### 系统表空间

#### SYS(Insert Buffer Header)

- 存储Change Buffer的头部信息

#### INDEX(Insert Buffer Root)

- 存储Change Buffer的根页面

#### TRX_SYS(Transaction System)

- 事务系统的相关信息

#### SYS(First Rollback Segment)

- 第一个回滚段的信息

#### SYS(Data Dicitionary Header)

- 数据字典头部信息
