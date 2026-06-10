# equals和hashCode

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 核心结论

- `equals` 用于判断两个对象在业务语义上是否相等，`hashCode` 用于支持哈希容器快速定位桶位置。
- 只要重写 `equals`，通常就必须同时重写 `hashCode`，否则对象放入 `HashMap`、`HashSet` 等容器后会出现查找失败、重复元素等问题。

### 基本契约

- 自反性：`x.equals(x)` 必须为 true。
- 对称性：`x.equals(y)` 为 true 时，`y.equals(x)` 也必须为 true。
- 传递性：`x.equals(y)` 和 `y.equals(z)` 都为 true 时，`x.equals(z)` 必须为 true。
- 一致性：对象参与比较的字段未变化时，多次调用结果应一致。
- 非空性：任何非 null 对象 `x.equals(null)` 都应返回 false。

### hashCode 规则

- 如果两个对象 `equals` 为 true，它们的 `hashCode` 必须相同。
- 如果两个对象 `hashCode` 相同，它们不一定 `equals` 为 true，因为哈希冲突是允许的。
- `hashCode` 应尽量让不同对象分布均匀，避免哈希桶退化。

### 工程实践

- 用于相等判断的字段应尽量稳定，不建议使用会频繁变化的字段作为 `equals/hashCode` 依据。
- 实体类如果使用数据库自增 ID，要注意对象持久化前 ID 为空时的相等性问题。
- Java 16+ 的 `record` 会自动生成基于组件字段的 `equals/hashCode/toString`，适合不可变值对象。
- Lombok 的 `@EqualsAndHashCode` 要谨慎配置 `callSuper` 和包含字段，继承层级复杂时尤其容易出错。

### 面试回答

- 我会先说明 `equals` 是业务相等，`hashCode` 是哈希容器定位；再强调两者契约：相等对象必须有相同哈希值；最后结合 `HashMap` 说明如果只重写 `equals` 不重写 `hashCode`，相同业务对象可能落到不同桶，导致查不到或去重失败。

### 复习检查

- 能用自己的话解释 `equals和hashCode`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图内容

## equals和hashCode
