# HashMap 深入

> 关联：[集合总览](README.md) | [红黑树](04-红黑树.md)

## 核心参数

```java
static final int DEFAULT_INITIAL_CAPACITY = 1 << 4; // 16
static final int MAXIMUM_CAPACITY = 1 << 30;
static final float DEFAULT_LOAD_FACTOR = 0.75f;
static final int TREEIFY_THRESHOLD = 8;   // 链表转红黑树阈值
static final int UNTREEIFY_THRESHOLD = 6; // 红黑树退化为链表阈值
static final int MIN_TREEIFY_CAPACITY = 64; // 允许树化的最小 table 容量
```

## 哈希函数

```java
static final int hash(Object key) {
    int h;
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
```

这一步叫做"扰动函数"，目的是让 `hashCode` 的高 16 位参与低位运算。

**为什么要做高低位异或？**

- 桶下标通过 `(n-1) & hash` 计算，当 `n`（table 容量）较小时，只有 `hash` 的低位参与运算，高位被完全忽略。
- 如果 `hashCode` 的高低位分布不均匀，直接截取低位会加剧碰撞。
- 将高 16 位异或到低 16 位，使高位信息也能影响桶的分配，以较低代价改善分布。

```
原始 hashCode:  1111 1011 1010 1100  0001 1010 0010 1001
右移 16 位:     0000 0000 0000 0000  1111 1011 1010 1100
XOR 结果:       1111 1011 1010 1100  1110 0001 1000 0101
                                    ← 这 16 位参与定位桶 →
```

## tableSizeFor

构造时传入的容量会被向上取整到 2 的幂：

```java
static final int tableSizeFor(int cap) {
    int n = cap - 1;
    n |= n >>> 1;
    n |= n >>> 2;
    n |= n >>> 4;
    n |= n >>> 8;
    n |= n >>> 16;
    return (n < 0) ? 1 : (n >= MAXIMUM_CAPACITY) ? MAXIMUM_CAPACITY : n + 1;
}
```

例如 `cap=10` → `n=9=0b1001` → 经过几次位填充后 `n=0b1111=15` → 返回 `16`。

`cap-1` 是为了避免本身已经是 2 的幂时多扩一倍（如 `cap=16` 若不减 1，最终会得到 32）。

## 初始化（懒加载）

`table` 数组不在构造时创建，在第一次 `put` 时由 `resize()` 初始化：

```java
final Node<K,V>[] resize() {
    // 第一次调用时 oldTab == null，oldCap == 0
    int newCap = (oldCap == 0) ?
        ((oldThr > 0) ? oldThr : DEFAULT_INITIAL_CAPACITY) :
        // 扩容：容量翻倍
        (oldCap << 1);
    // ...
    Node<K,V>[] newTab = (Node<K,V>[]) new Node[newCap];
    table = newTab;
    // 把旧节点迁移到新 table...
    return newTab;
}
```

## Node 结构

```java
static class Node<K,V> implements Map.Entry<K,V> {
    final int hash;   // key 的 hash，缓存避免重复计算
    final K key;
    V value;
    Node<K,V> next;   // 链表后继
}
```

JDK 8 引入的 `TreeNode` 继承自 `LinkedHashMap.Entry`（后者继承自 `Node`），额外持有红黑树的父、左、右子、前驱节点以及颜色标志：

```java
static final class TreeNode<K,V> extends LinkedHashMap.Entry<K,V> {
    TreeNode<K,V> parent;
    TreeNode<K,V> left;
    TreeNode<K,V> right;
    TreeNode<K,V> prev; // 用于反树化时还原链表顺序
    boolean red;
}
```

`TreeNode` 同时维护了双向链表（`prev/next`）和红黑树结构，因此树化和反树化无需重新分配节点。

## put 流程

```java
final V putVal(int hash, K key, V value, boolean onlyIfAbsent, boolean evict) {
    Node<K,V>[] tab; Node<K,V> p; int n, i;

    // 1. table 未初始化，先扩容初始化
    if ((tab = table) == null || (n = tab.length) == 0)
        n = (tab = resize()).length;

    // 2. 目标桶为空，直接插入
    if ((p = tab[i = (n - 1) & hash]) == null)
        tab[i] = newNode(hash, key, value, null);
    else {
        Node<K,V> e; K k;

        // 3. 桶首节点命中
        if (p.hash == hash &&
            ((k = p.key) == key || (key != null && key.equals(k))))
            e = p;

        // 4. 桶首节点是树节点，走红黑树插入
        else if (p instanceof TreeNode)
            e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);

        // 5. 链表遍历
        else {
            for (int binCount = 0; ; ++binCount) {
                if ((e = p.next) == null) {
                    p.next = newNode(hash, key, value, null); // 尾插
                    if (binCount >= TREEIFY_THRESHOLD - 1)    // 达到阈值尝试树化
                        treeifyBin(tab, hash);
                    break;
                }
                if (e.hash == hash &&
                    ((k = e.key) == key || (key != null && key.equals(k))))
                    break;  // 找到 key 相同节点
                p = e;
            }
        }

        // 6. 找到已有节点：更新 value
        if (e != null) {
            V oldValue = e.value;
            if (!onlyIfAbsent || oldValue == null)
                e.value = value;
            afterNodeAccess(e);
            return oldValue;
        }
    }

    // 7. 新增节点：更新 modCount，检查是否超过阈值需要扩容
    ++modCount;
    if (++size > threshold)
        resize();
    afterNodeInsertion(evict);
    return null;
}
```

## get 流程

```java
final Node<K,V> getNode(int hash, Object key) {
    Node<K,V>[] tab; Node<K,V> first, e; int n; K k;

    if ((tab = table) != null && (n = tab.length) > 0 &&
        (first = tab[(n - 1) & hash]) != null) {

        // 先检查桶首节点（大多数情况命中）
        if (first.hash == hash &&
            ((k = first.key) == key || (key != null && key.equals(k))))
            return first;

        if ((e = first.next) != null) {
            if (first instanceof TreeNode)
                return ((TreeNode<K,V>)first).getTreeNode(hash, key);
            // 链表顺序查找
            do {
                if (e.hash == hash &&
                    ((k = e.key) == key || (key != null && key.equals(k))))
                    return e;
            } while ((e = e.next) != null);
        }
    }
    return null;
}
```

## 扩容与迁移

```java
// 节点迁移的关键逻辑（简化）
Node<K,V> loHead = null, loTail = null; // 留在原位的链表
Node<K,V> hiHead = null, hiTail = null; // 移动到高位的链表

do {
    next = e.next;
    // (e.hash & oldCap) 的结果只有 0 或 oldCap 两种
    if ((e.hash & oldCap) == 0) {
        // 该位为 0：节点留在原索引
        if (loTail == null) loHead = e;
        else loTail.next = e;
        loTail = e;
    } else {
        // 该位为 1：节点移动到 原索引 + oldCap
        if (hiTail == null) hiHead = e;
        else hiTail.next = e;
        hiTail = e;
    }
} while ((e = next) != null);

if (loTail != null) { loTail.next = null; newTab[j] = loHead; }
if (hiTail != null) { hiTail.next = null; newTab[j + oldCap] = hiHead; }
```

**为什么用 `e.hash & oldCap` 而不是取模？**

扩容后容量变为 `2n`，新桶下标变为 `(2n-1) & hash`，比旧下标 `(n-1) & hash` 多一位比较。新多出的那一位就是 `hash` 第 `log₂(n)` 位，而 `oldCap = n`，所以 `e.hash & oldCap` 恰好测试的是这一位。这样不需要重新计算完整的模，效率更高。

## 树化与反树化

### 树化（链表 → 红黑树）

```java
final void treeifyBin(Node<K,V>[] tab, int hash) {
    int n, index; Node<K,V> e;
    // table 容量小于 64 时优先扩容，不树化
    if (tab == null || (n = tab.length) < MIN_TREEIFY_CAPACITY)
        resize();
    else if ((e = tab[index = (n - 1) & hash]) != null) {
        TreeNode<K,V> hd = null, tl = null;
        do {
            TreeNode<K,V> p = replacementTreeNode(e, null);
            if (tl == null) hd = p;
            else { p.prev = tl; tl.next = p; }
            tl = p;
        } while ((e = e.next) != null);
        if ((tab[index] = hd) != null)
            hd.treeify(tab); // 构建红黑树
    }
}
```

### 树化阈值为什么选 8？

在理想随机哈希分布下，单桶节点数服从**泊松分布**（λ=0.5）：

| 节点数 | 概率 |
| --- | --- |
| 0 | 0.60653 |
| 1 | 0.30327 |
| 2 | 0.07582 |
| 3 | 0.01264 |
| 4 | 0.00158 |
| 5 | 0.000032 |
| 6 | 0.0000054 |
| 7 | 0.00000078 |
| 8 | 0.000000099 |

达到 8 个节点的概率约为 **0.0000001**，极为罕见。一旦出现，几乎可以断定是 `hashCode` 实现极差或有意制造冲突，此时用红黑树保护是合理的。

### 反树化阈值为什么是 6 而不是 8？

反树化（红黑树退化为链表）阈值是 6，而不是和树化阈值相同的 8。原因是避免在 7、8 附近频繁切换（插入触发树化，删除后立即反树化，又插入又树化……）。两个阈值之间留出 2 的缓冲可以防止这种"抖动"（thrashing）。

## 原子更新 API

不要使用 `get` + `put` 组合来做条件更新，这在单线程也不是原子的，且语义不清晰。应使用内置原子方法：

```java
Map<String, Integer> map = new HashMap<>();

// putIfAbsent：key 不存在时才插入
map.putIfAbsent("count", 0);

// computeIfAbsent：key 不存在时用函数计算 value
map.computeIfAbsent("list", k -> new ArrayList<>()).add("item");

// computeIfPresent：key 存在时更新
map.computeIfPresent("count", (k, v) -> v + 1);

// compute：无论是否存在都执行，可以返回 null 删除
map.compute("count", (k, v) -> v == null ? 1 : v + 1);

// merge：常用于计数累加
map.merge("count", 1, Integer::sum);
```

## JDK 7 与 JDK 8 主要差异

| 对比项 | JDK 7 | JDK 8+ |
| --- | --- | --- |
| 底层结构 | 数组 + 链表 | 数组 + 链表 + 红黑树 |
| 链表插入方式 | **头插法** | **尾插法** |
| 节点类型 | `Entry` | `Node`（普通）、`TreeNode`（树） |
| 哈希扰动 | 多次扰动（4次位运算） | 单次 h ^ (h >>> 16) |
| 冲突严重时 | O(n) 链表 | O(log n) 红黑树 |
| 并发扩容风险 | 头插法导致链表成环 → 死循环 | 尾插法避免成环，但仍不是线程安全 |

### JDK 7 头插法的并发死循环

JDK 7 扩容时用头插法将旧链表节点迁移到新 table，多线程同时扩容时可能出现：

1. 线程 A 和线程 B 同时触发扩容。
2. 线程 A 完成一部分后被挂起，此时链表节点顺序已发生变化。
3. 线程 B 恢复执行，head 和 next 的引用关系导致链表形成环。
4. 之后任何 `get` 操作在该桶中无限循环。

JDK 8 改为尾插法后，扩容迁移时链表顺序不会反转，不会形成环。但 `HashMap` 本身依然不是线程安全的，并发修改仍可能导致数据丢失或 size 计数错误，并发场景应使用 `ConcurrentHashMap`。

## equals 和 hashCode 合约

HashMap 中 key 的查找逻辑：

1. 用 `key.hashCode()` 计算哈希，定位桶。
2. 在桶中用 `==` 或 `key.equals(existing)` 精确匹配。

因此合约要求：

- **若 `a.equals(b)` 为 true，则 `a.hashCode() == b.hashCode()`**（否则 equals 的 key 分到不同桶，查不到）。
- `hashCode` 相同但 `equals` 不同是允许的（hash 冲突），只影响性能。
- 若将对象作为 key 后修改了影响 `hashCode` 的字段，对象将无法被找到（key 换桶了）。

```java
class BadKey {
    int value;
    // hashCode 依赖 value，但 value 可变
    public int hashCode() { return value; }
    public boolean equals(Object o) { return o instanceof BadKey bk && bk.value == this.value; }
}

Map<BadKey, String> map = new HashMap<>();
BadKey k = new BadKey();
k.value = 1;
map.put(k, "one");

k.value = 2; // 修改了影响 hashCode 的字段
map.get(k);  // null，key 在 hashCode=1 对应的桶里，但现在去找 hashCode=2 的桶
```

## 性能小结

| 操作 | 平均 | 最坏（冲突） | 最坏（树化后） |
| --- | --- | --- | --- |
| `put` | O(1) | O(n) | O(log n) |
| `get` | O(1) | O(n) | O(log n) |
| `remove` | O(1) | O(n) | O(log n) |
| `resize` | O(n) | O(n) | O(n) |
