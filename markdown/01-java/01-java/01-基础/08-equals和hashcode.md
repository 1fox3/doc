# equals和hashCode

## 核心规则

- `equals` 判断业务语义是否相等，`hashCode` 用于哈希容器快速定位桶位置。
- 重写 `equals` 必须同时重写 `hashCode`，否则对象放入 `HashMap`、`HashSet` 后会出现查找失败、去重失效等问题。

## equals 五大契约

| 约束 | 含义 |
|------|------|
| 自反性 | `x.equals(x)` 必须为 `true` |
| 对称性 | `x.equals(y)` 为 `true` 时，`y.equals(x)` 也必须为 `true` |
| 传递性 | `x.equals(y)` 且 `y.equals(z)` 为 `true`，则 `x.equals(z)` 必须为 `true` |
| 一致性 | 参与比较的字段未变化时，多次调用结果应一致 |
| 非空性 | `x.equals(null)` 必须返回 `false` |

## hashCode 规则

- `equals` 为 `true` 的两个对象，`hashCode` 必须相同。
- `hashCode` 相同的两个对象，`equals` 不一定为 `true`（哈希冲突允许存在）。
- `hashCode` 应尽量分布均匀，避免哈希桶退化为链表。

## 注意点

- 用于相等判断的字段应稳定，不建议使用频繁变化的字段。
- 实体类使用数据库自增 ID 时，注意持久化前 ID 为空的相等性问题。
- Java 16+ 的 `record` 自动生成基于组件字段的 `equals/hashCode/toString`，适合不可变值对象。
- Lombok 的 `@EqualsAndHashCode` 要谨慎配置 `callSuper` 和包含字段，继承层级复杂时尤其容易出错。
