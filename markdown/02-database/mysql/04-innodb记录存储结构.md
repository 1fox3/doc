# InnoDB记录存储结构

## 行格式

- InnoDB 常见行格式包括 `REDUNDANT`、`COMPACT`、`DYNAMIC`、`COMPRESSED`，MySQL 8.0 默认通常为 `DYNAMIC`。
- 一条记录由额外信息、隐藏列、NULL 标记、变长字段长度列表和用户列数据组成。
- 无显式主键时，InnoDB 会选择第一个非空唯一索引作为聚簇键；仍不存在时生成 6 字节隐藏 `row_id`。

## 隐藏列

- `DB_TRX_ID` 记录最近一次修改该行的事务 ID，用于 MVCC 可见性判断。
- `DB_ROLL_PTR` 指向 undo log 中的旧版本，用于构造历史版本和事务回滚。
- `DB_ROW_ID` 在表没有合适主键时生成，作为聚簇索引键。

## 溢出页

- `VARCHAR`、`TEXT`、`BLOB` 等大字段可能不完全存储在聚簇索引页内。
- `DYNAMIC` 行格式通常在页内保存指针，将长字段主体放到溢出页，减少索引页膨胀。
- 大字段会增加随机 I/O 和 Buffer Pool 压力，热点查询应避免无条件读取大字段。

## 实践要点

- 主键建议短、稳定、递增或近似递增，避免聚簇索引频繁页分裂和二级索引膨胀。
- 大字段拆表或延迟读取可以降低回表成本和缓存污染。
- 表结构评审时关注 NULL 列数量、变长字段、字符集和主键选择对行大小的影响。

## 行大小影响

- 行越宽，单页可容纳记录越少，B+Tree 高度和页读取次数更容易增加。
- 二级索引叶子节点会保存主键值，长主键会放大每个二级索引的体积。
- `utf8mb4` 下 `VARCHAR(n)` 的最大字节数可能是 `n * 4`，定义很长的变长列会影响临时表、排序和索引长度设计。
- 允许 NULL 的列需要额外 NULL 标记位，数量很多时也会增加记录管理开销。

## 设计示例

```sql
-- 不推荐：随机长字符串主键会放大聚簇索引和全部二级索引。
CREATE TABLE order_bad (
  id varchar(64) PRIMARY KEY,
  user_id bigint NOT NULL,
  created_at datetime NOT NULL,
  KEY idx_user_created(user_id, created_at)
) ENGINE=InnoDB;

-- 更常见：使用短主键，业务唯一号另建唯一索引。
CREATE TABLE order_good (
  id bigint PRIMARY KEY,
  order_no varchar(64) NOT NULL,
  user_id bigint NOT NULL,
  created_at datetime NOT NULL,
  UNIQUE KEY uk_order_no(order_no),
  KEY idx_user_created(user_id, created_at)
) ENGINE=InnoDB;
```

## 常见误区

- “没有主键也没关系”：InnoDB 会生成隐藏 row_id，但业务无法利用它做稳定定位，也不利于复制和数据维护。
- “字段越多越方便”：宽表会降低缓存密度，高频查询只需要少量字段时成本明显上升。
- “大字段可以随便放”：`TEXT/BLOB` 会影响回表、网络传输、临时表和备份恢复耗时。
