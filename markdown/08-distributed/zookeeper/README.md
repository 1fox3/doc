# ZooKeeper

> 来源：ZooKeeper.xmind, 面试内容汇总/ZooKeeper.xmind

## 核心认知

- ZooKeeper 提供一致性元数据协调，适合配置、命名、选主、分布式锁等小数据强一致场景。
- 不要把 ZooKeeper 当作大数据存储或高频业务读写数据库。

## 面试重点

- ZNode、Watcher、Session、ACL、ZXID、Leader 选举、ZAB、过半机制。
- 临时节点、顺序节点、分布式锁、羊群效应和 Curator 封装。

## 实践检查点

- 能解释会话过期与连接断开的区别，以及对临时节点的影响。
- 能设计可重入、公平、可超时的分布式锁，并处理锁释放异常。

## 版本与趋势

- ZooKeeper 仍常用于协调与元数据，但新系统应谨慎评估是否可由 etcd、Nacos、KRaft 或云服务替代。
- 使用 ZooKeeper 时要控制节点数量、watcher 数量、会话超时和磁盘延迟。

## 章节目录

### ZooKeeper.xmind

- [简介](01-简介.md)
- [了解](02-了解.md)
- [使用API](03-使用api.md)
- [处理状态变化](04-处理状态变化.md)
- [故障处理](05-故障处理.md)
- [注意事项](06-注意事项.md)
- [C语言客户端](07-c语言客户端.md)
- [Curator](08-curator.md)
- [内部原理](09-内部原理.md)
- [运行ZooKeeper](10-运行zookeeper.md)
### 面试内容汇总/ZooKeeper.xmind

- [端口](11-端口.md)
- [节点](12-节点.md)
- [会话](13-会话.md)
- [Watcher](14-watcher.md)
- [事务ID](15-事务id.md)
- [ACL](16-acl.md)
- [Leader选举](17-leader选举.md)
- [ZAB](18-zab.md)
- [Java客户端](19-java客户端.md)
- [四字母命令](20-四字母命令.md)
- [instantiate](21-instantiate.md)
