# RocketMQ消息存储

> 专题：重点汇总
> 来源：重点汇总.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## RocketMQ消息存储

### 存储设计

#### 重点文件

- CommitLog
  - 消息存储，所有消息主题的消息都存储在CommitLog文件中
  - 追求极致的磁盘顺序写
  - 消息一旦写入，不支持修改
  - 通过偏移量来命名文件，可进行二分查找

- ConsumerQueue
  - 消息消费队列，消息到达CommitLog文件后，将异步转发到ConsumerQueue文件中，供消息消费者消费
  - 每条消息固定长度
    - commitlog偏移量-8字节
    - 大小-4字节
    - tag哈希码-8字节

- Index
  - 消息索引，主要存储消息key和offset的对应关系
  - 支持基于消息某一个属性进行查找
  - 基于文件的hash索引
  - 文件结构
    - Index文件头
      - beginTimestamp
      - endTimestamo
      - beginPhyoffset
      - endPhyoffset
      - hashSlotCount
      - indexCount
    - 500万个哈希槽
    - 2000万个Index条目
      - hashCode
      - pyhoffset
      - timedif
      - pre index no

#### 内存映射

- 在Java中使用FileChannel的map方法创建内存映射文件

- 如果RocketMQ Broker进程异常退出，存储的页缓存中的数据并不会丢失，操作异同会董事将页缓存中的数据持久化到磁盘中，实现数据安全可靠。

#### 刷盘策略

- 同步刷盘
  - 在RocketMQ的实现中称作组提交

- 异步刷盘
  - broker将消息存储到pagecache后就立即返回成功
  - 开启一个异步线程定时(默认500ms)执行FileChannel的force方法，将内存中的数据定时一写入磁盘。

#### transientStorePoolEnable

- 过程
  - 消息写入对外内存并立即返回
  - 异步将对外内存中的数据提交到pagecache，再异步刷盘到磁盘中

- 好处
  - 批量写入pagechahce
  - 实现内存级别的读写分离

- 缺点
  - 出现故障时，写入堆外内存的数据会丢失

#### 文件恢复机制

- 文件恢复过程
  - 查找ConsumeQueue文件中最后一条完整的消息记录的物理偏移量
  - 跟CommitLog中的最大偏移量比较，以CommitLog中的偏移量为准里删除ConsumeQueue中的内容或重新推数

- 如何确定要恢复的文件
  - 正常停止刷盘
    - 从倒数第三个文件开始，直到找到最后一条消息记录
  - 异常停止刷盘
    - 借助检查点文件，从最后一个文件开始，如果该文件的第一条消息的存储时间消息文件的刷盘时间，就从这个文件开始恢复，否则继续寻找上一个文件

### 消息发送存储过程

#### 如果当前节点broker停止工作或当前不支持写入则拒绝写入

#### 如果消息的延迟级别大于0，则使用延时主题和队列

#### 获取当前可以写入的CommitLog

#### 写入CommitLog之前，先申请putMessageLock

#### 设置消息的存储时间，并判断CommitLog是否需要创建或可写入

#### 消息追加到MappedFile中

#### 创建全局唯一的消息ID

- IP

- 端口号

- 消息偏移量

#### 获取该消息在消息队列的偏移量

#### 计算消息的总长度

#### 判断CommitLog是否有足够空间写入消息

#### 消息内容存储到ByteBuffer，然后创建AppendMessageResult

#### 更新消息队列的逻辑偏移量

#### 处理完消息追加逻辑后释放putMessageLock

#### 根据刷盘方式，经数据持久化到磁盘中，然后执行HA主从同步

### 存储文件组织和内存映射

#### MappedFileQueue

- 是MappedFile的管理容器，MappedFileQueue对存储目录进行封装

#### MappedFile

#### TransientStorePool

- 短暂存储池。RocketMQ单独创建了一个DirectByteBuffer内存缓存池，用来临时存储数据，数据先写入该内存映射中，然后有Commit线程定时将数据从该内存复制到与目标物理文件对应的内存映射中。

- RocketMQ引入该机制时为了提供一种内存锁定，将当前堆外内存一直锁定在内存中，避免被进程将内存交换到磁盘

### 存储文件

#### 目录

- commitlog
  - 消息存储目录

- config
  - consumerFilter.json
    - 主题消息过滤信息
  - consumerOffset.json
    - 集群消费模式下的消息消费进度
  - delayOffset.json
    - 延时消息队列拉取进度
  - subscriptionGroup.json
    - 消息消费组的配置信息
  - topics.json
    - topic配置属性

- consumequeue
  - 消息消费队列存储目录

- index
  - 消息索引文件存储目录

- abort
  - 如果存在abort文件，说明broker非正常关闭，该文件在Broker启动时创建，正常退出时删除

- checkpoint
  - 监测点文件，存储CommitLog、ConsumeLog，INdex的最后一次刷盘时间戳

#### 重点文件 (24)

- CommitLog
  - 默认大小为1GB，对应配置为mapedFileSizeCommitLog

- ConsumeQueue
  - 一级目录为消息主题，二级目录为消息队列
  - 使用二分查找方式实现根据消息存储时间查找消息
  - 记录内容
    - CommitLog偏移量
    - 文件大小
    - tag哈希码

- Index
  - Rocket将消息索引建与消息偏移量的映射写入Index

- checkpoint文件
  - 文件固定长度为4KB，仅使用前24字节
  - physicMsgTimestamp
    - CommitLog文件刷盘时间点
  - logicsMsgTimestamp
    - ConsumeQueue文件刷盘时间
  - indexMsgTimestamp
    - Index文件刷盘时间

### 实时更新ConsumeQueue与Index文件

#### ReputMessageService来准时转发CommitLog文件的更新事件，该进程在Broker启动时创建，且指定一个reputFromOffset，指定从哪个偏移量开始转发消息

#### 相关实现类

- CommitLogDispatcherBuildConsumeQueue

- CommitLogDispatcherBuildIndex

### ConsumeQueue与Index文件恢复

#### 过程

- 判断上一次是否正常退出，等价于判断是否存在abort文件

- 加载延迟队列

- 加载commitlog目录下所有文件并排好序

- 加载所有消息消费队列

- 加载并存储checkpoint文件

- 加载Index文件，如果上次异常退出，且Index文件刷盘时间小于该文件最大的消息时间戳，则将该文件销毁

- 根据broker是否为正常停止，执行不同的恢复策略
  - 正常恢复
    - Broker正常停止再重启时，从倒数第3个文件开始恢复，如果不足3个文件，则从第一个文件开始恢复
    - 变量解释
      - mappedFileOffset
        - 当前文件已校验通过的物理偏移量
      - processOffset
        - CommitLog文件已确认的物理偏移量
    - 遍历CommitLog，每次取出一条消息
      - 查找结果为true，且消息长度大于0
        - 表示消息正确，mappedFileOffset指向前移动本条消息长度
      - 查找结果为true，且消息长度为0
        - 表示已到文件末尾，如果还有下一个文件，则充值processOffset，mappedFileOffset并重复上述步骤，否则跳出循环
      - 查找结果为false
        - 文件未填满所有信息，则跳出循环，结束遍历文件
    - 更新MappedFileQueue的flushWhere和committedPosition指针
    - 删除offset之后所有文件
  - 异常恢复
    - 大致过程
      - 从最后一个文件向倒序推进，找到第一个消息存储正常的文件
    - 如何判断消息文件正确
      - 判断文件的魔数是否为MESSAGE_MAGIC_CODE
      - 如果文件中的第一条消息的存储时间为0，则返回false，说明文件中未存储任何消息
      - 对比文件第一条消息的时间戳以检测点。如果小于检测点说明该文件消息部分可靠的，从该文件开始恢复
      - 找到对应的MappedFile，遍历MappedFile中的消息，验证消息的合法性，并重新转发到ConsumeQueue和Index文件
      - 如果未找到有效的MappedFile，则是指CommitLog的flushWhere，committedWhere指针为0，并销毁CommitQueue文件

- 恢复ConsumerQueue文件后，将CommitLog实例中保存每个消息消费队列当前的存储逻辑偏移量，这就是消息中不仅存储主题，消息队列ID，还存储了消息队列偏移量的关键所在

### 文件刷盘机制

#### 同步刷盘

- CommitLog.handleDiskFlush

- GroupCommitService
  - 处理完一批刷盘请求后，如果还有任务，则立即执行，否则每个10ms空转一次

- 消息生产者在消息服务端将消息内容追加到内存映射文件(内存)后，需要将内存的内容立刻写入磁盘

#### 异步刷盘

- 将消息直接追加到ByteBudder(堆外内存)，wrotePosition随着消息的不断追加向后移动

- CommitRealTimeService线程每隔200ms将ByteBuffer的数据提交到FileChannel中

- FileChannel在通道中追加提交的内容，其wrotePostion指针向后移动，然后返回

- commit操作成功返回，将commitedPosition向后移动本次提交的内容长度，此时wrotePostion依然可以向前推进

- FlushRealTimeService线程默认每500ms将FileChannel中新追加的内存，通过FileChannel.force方法将数据写入磁盘

### 过期文件删除机制

#### 基本策略

- 如果非当前写文件在一定时间间隔内没有再次更新，则认为时过期文件，可以被删除，默认过期时间为72小时-fileReservedTime

#### 先关任务

- cleanFilesPeriodically
  - 检测是否需要清除过期文件
  - 10s一次-cleanResourceInterval

#### 相关配置

- fileReservedTime
  - 文件保留时间

- deletePhysicFilesInterval
  - 删除物理文件的间隔时间

- destoryMapedFileIntervalFactory
  - 第一次拒绝删除之后能保留文件的最大时间

#### 删除文件条件

- 指定删除文件的时间点，默认凌晨4点

- 检查磁盘空间是否充足

- 预留手工触发机制

#### 删除过程

- 从倒数第二个文件开始遍历，计算文件的最大村花时间，即文件的最后一次更新加文件存活时间(默认72h)

- 如果当前时间大于文件的最大存活时间或需要强制删除文件时，删除MappedFile占有的相关资源，如果执行成功，则将该文件加入待删除文件列表，最后统一执行File.delete方法将文件从物理磁盘中删除

### 同步双写

#### HaService

#### 异步执行asyncPutMessage
