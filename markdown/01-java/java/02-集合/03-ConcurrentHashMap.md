# ConcurrentHashMap 深入

> 关联：[集合总览](README.md) | [HashMap](02-HashMap.md)

## JDK 7 实现：Segment 分段锁

JDK 7 的 `ConcurrentHashMap` 将 table 分成若干个 `Segment`，每个 `Segment` 继承 `ReentrantLock` 并持有一个小型 `HashEntry[]`。

```
ConcurrentHashMap
├── Segment[0]  ← ReentrantLock + HashEntry[]
├── Segment[1]  ← ReentrantLock + HashEntry[]
├── ...
└── Segment[15] ← 默认 16 个 Segment
```

```java
// JDK 7 Segment（简化）
static final class Segment<K,V> extends ReentrantLock {
    volatile HashEntry<K,V>[] table;
    int count;
    int modCount;
    int threshold;
    float loadFactor;
}
```

- `put`/`remove` 只锁目标 `Segment`，不同 `Segment` 上的操作可并发执行。
- `get` 不加锁，依赖 `volatile` 保证可见性。
- 默认 16 个 `Segment`，最大并发数等于 `Segment` 数量。
- `size()` 先尝试不加锁统计，失败后对所有 `Segment` 加锁重试。

**缺陷**：`Segment` 数量固定（创建时确定），无法动态调整并发度；结构复杂，内存占用较高。

## JDK 8 实现：CAS + synchronized

JDK 8 抛弃了 `Segment`，回归单层数组结构，对每个桶的首节点加 `synchronized`，并大量使用 CAS。

```
Node<K,V>[] table
├── [0]  → Node（链表头）或 TreeBin（树根包装）或 null
├── [1]  → ...
└── [n-1]→ ...
```

### 特殊节点类型

| 类型 | hash 值 | 作用 |
| --- | --- | --- |
| `Node` | 正常 hash | 普通链表节点 |
| `TreeBin` | `TREEBIN = -2` | 红黑树的包装容器（桶首节点） |
| `ForwardingNode` | `MOVED = -1` | 扩容中的占位节点，协助线程迁移 |
| `ReservationNode` | `RESERVED = -3` | `computeIfAbsent` 的占位节点 |

### table 初始化

```java
private final Node<K,V>[] initTable() {
    Node<K,V>[] tab; int sc;
    while ((tab = table) == null || tab.length == 0) {
        if ((sc = sizeCtl) < 0)
            Thread.yield(); // 已有线程在初始化，当前线程让步等待
        else if (U.compareAndSwapInt(this, SIZECTL, sc, -1)) {
            // CAS 将 sizeCtl 设为 -1，成功则由本线程初始化
            try {
                if ((tab = table) == null || tab.length == 0) {
                    int n = (sc > 0) ? sc : DEFAULT_CAPACITY;
                    table = (Node<K,V>[]) new Node[n];
                    sc = n - (n >>> 2); // sc = 0.75 * n，即新阈值
                }
            } finally {
                sizeCtl = sc; // 初始化完成后恢复 sizeCtl 为阈值
            }
            break;
        }
    }
    return tab;
}
```

`sizeCtl` 是多语义字段：
- `-1`：table 正在初始化
- `-(1 + 迁移线程数)`：正在扩容
- `0`：未初始化，使用默认容量
- `n`：已初始化，下次扩容的阈值

### put 流程

```java
final V putVal(K key, V value, boolean onlyIfAbsent) {
    // 不允许 null key 或 null value
    if (key == null || value == null) throw new NullPointerException();

    int hash = spread(key.hashCode()); // 扰动函数

    for (Node<K,V>[] tab = table;;) {
        Node<K,V> f; int n, i, fh;

        if (tab == null || (n = tab.length) == 0)
            tab = initTable();                          // 懒初始化

        else if ((f = tabAt(tab, i = (n - 1) & hash)) == null) {
            // 目标桶为空：CAS 插入，无需加锁
            if (casTabAt(tab, i, null, new Node<>(hash, key, value, null)))
                break;

        } else if ((fh = f.hash) == MOVED)
            tab = helpTransfer(tab, f);                 // 桶上是 ForwardingNode，协助扩容

        else {
            V oldVal = null;
            synchronized (f) {                          // 锁住桶首节点
                if (tabAt(tab, i) == f) {               // 双重检查（防止 f 已被替换）
                    if (fh >= 0) {                      // 正常链表
                        // ... 链表遍历，尾插或更新
                    } else if (f instanceof TreeBin) {  // 红黑树
                        // ... 调用 TreeBin.putTreeVal
                    }
                }
            }
            // 检查是否需要树化
            if (binCount >= TREEIFY_THRESHOLD)
                treeifyBin(tab, i);
        }
    }
    addCount(1L, binCount); // 更新 size 并检查是否需要扩容
    return null;
}
```

### 扰动函数

```java
static final int spread(int h) {
    return (h ^ (h >>> 16)) & HASH_BITS; // HASH_BITS = 0x7fffffff
}
```

与 `HashMap` 类似，额外与 `HASH_BITS` 做 AND 是为了确保 hash 值为正数（特殊节点的 hash 值都是负数，用正负来区分节点类型）。

### volatile 读/CAS 写

```java
// 使用 Unsafe 进行 volatile 读，确保能看到其他线程的最新写入
static final <K,V> Node<K,V> tabAt(Node<K,V>[] tab, int i) {
    return (Node<K,V>) U.getObjectVolatile(tab, ((long)i << ASHIFT) + ABASE);
}

// CAS 写：期望 tab[i] 为 c，则将其替换为 v
static final <K,V> boolean casTabAt(Node<K,V>[] tab, int i, Node<K,V> c, Node<K,V> v) {
    return U.compareAndSwapObject(tab, ((long)i << ASHIFT) + ABASE, c, v);
}
```

`get` 操作完全不加锁，通过 `tabAt`（volatile 读）获取桶首节点，保证可见性。

## 扩容：多线程协作迁移

### 扩容触发

```java
private final void addCount(long x, int check) {
    // 更新 size 计数（见后文）
    // ...
    if (check >= 0) {
        Node<K,V>[] tab = table;
        long sc;
        while (s >= (long)(sc = sizeCtl) && tab != null && tab.length < MAXIMUM_CAPACITY) {
            int rs = resizeStamp(n); // 扩容戳，编码了扩容前的容量
            if (sc < 0) {
                // 其他线程正在扩容，尝试加入协助
                if (sc == (rs << RESIZE_STAMP_SHIFT) + MAX_RESIZERS) break;
                if (nextTable == null) break;
                if (transferIndex <= 0) break;
                if (U.compareAndSwapInt(this, SIZECTL, sc, sc + 1))
                    transfer(tab, nextTable); // 加入协助迁移
            } else if (U.compareAndSwapInt(this, SIZECTL, sc, (rs << RESIZE_STAMP_SHIFT) + 2)) {
                transfer(tab, null); // 本线程发起扩容
            }
        }
    }
}
```

### transfer 分段迁移

`transfer` 将 table 划分为若干 stride（步长，最小 16），每个线程认领一段区间迁移：

```java
private final void transfer(Node<K,V>[] tab, Node<K,V>[] nextTab) {
    int n = tab.length, stride;
    // stride = max(n / (8 * CPU核数), 16)
    if ((stride = (NCPU > 1) ? (n >>> 3) / NCPU : n) < MIN_TRANSFER_STRIDE)
        stride = MIN_TRANSFER_STRIDE;

    if (nextTab == null) { // 初始化新 table（第一个扩容线程负责）
        nextTab = (Node<K,V>[]) new Node[n << 1];
        nextTable = nextTab;
        transferIndex = n; // 从高位桶开始分配
    }

    for (int i = 0, bound = 0;;) {
        // 通过 CAS 领取下一段区间 [bound, i]
        while (advance) { /* 领取区间 */ }

        // 迁移当前桶
        Node<K,V> f = tabAt(tab, i);
        synchronized (f) {
            // 将链表拆成 lo 链和 hi 链（原理同 HashMap）
            // 将树节点拆分并判断是否需要反树化
        }
        // 迁移完成后设置 ForwardingNode 占位
        setTabAt(tab, i, fwd);
    }
}
```

其他线程对 `ForwardingNode` 所在桶进行 `put`/`get` 时：
- `get`：直接到 `nextTab` 中查找。
- `put`：调用 `helpTransfer`，加入迁移协作，完成后继续自己的 `put`。

## size 计数机制

与 `HashMap` 直接维护 `size` 不同，`ConcurrentHashMap` 采用类似 `LongAdder` 的计数方式：

```java
private transient volatile long baseCount;          // 基础计数
private transient volatile CounterCell[] counterCells; // 分散计数
```

- 低竞争时：CAS 更新 `baseCount`。
- CAS 失败（高竞争）时：选择或创建一个 `CounterCell`，累加到该格子。

`size()` / `mappingCount()` 时汇总所有格子：

```java
public long mappingCount() {
    long n = sumCount();
    return (n < 0L) ? 0L : n;
}

final long sumCount() {
    CounterCell[] as = counterCells;
    long sum = baseCount;
    if (as != null) {
        for (CounterCell a : as)
            if (a != null) sum += a.value;
    }
    return sum;
}
```

这种设计和 `LongAdder` 如出一辙，高并发下计数性能远优于单个 `AtomicLong`。

`size()` 返回 `int`，当实际大小超过 `Integer.MAX_VALUE` 时会截断，推荐使用 `mappingCount()` 返回 `long`。

## 迭代器：弱一致性

`ConcurrentHashMap` 的迭代器是**弱一致性**（weakly consistent）的，不是 fail-fast 的：

- 迭代期间不会抛 `ConcurrentModificationException`。
- 迭代器可能反映也可能不反映在迭代开始后发生的并发修改。
- 迭代创建时已存在的元素保证被访问到。
- 扩容期间新/旧 table 的节点都可能被遍历，但不会重复或遗漏已有元素。

## 复合操作与原子语义

`ConcurrentHashMap` 的单次方法是线程安全的，但组合多次调用不是原子的：

```java
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();

// 错误：get 和 put 之间可能有并发修改
Integer old = map.get("key");
map.put("key", old == null ? 1 : old + 1);

// 正确：原子操作
map.merge("key", 1, Integer::sum);

// 正确：computeIfAbsent 保证初始化只发生一次
map.computeIfAbsent("key", k -> new ArrayList<>()).add("value");
```

`computeIfAbsent` 在 key 不存在时会对目标桶加 `synchronized`，确保并发调用只有一个线程执行计算函数。

## 与 HashMap 对比

| 对比项 | `HashMap` | `ConcurrentHashMap` |
| --- | --- | --- |
| 线程安全 | 否 | 是 |
| null key/value | 允许 | 不允许 |
| 底层结构 | 数组 + 链表 + 红黑树 | 同左，加 ForwardingNode 等特殊节点 |
| 加锁粒度 | 无锁 | CAS（空桶）+ synchronized（桶首节点）|
| 扩容 | 单线程 | 多线程协作 |
| 计数 | `int size` | baseCount + CounterCell[] |
| 迭代器 | fail-fast | 弱一致性 |
| 适用场景 | 单线程 | 高并发 |

## 常见误区

### 误区 1：单次操作安全 ≠ 复合操作安全

```java
// 线程 A 和线程 B 同时执行以下代码
if (!map.containsKey("key")) {
    map.put("key", new ArrayList<>()); // 可能被两个线程各插入一次
}

// 正确：使用 putIfAbsent 或 computeIfAbsent
map.computeIfAbsent("key", k -> new ArrayList<>());
```

### 误区 2：size() 不精确

由于 `size()` 是近似值（各 CounterCell 的异步汇总），在多线程环境下它只是一个估算值，不应依赖它做精确判断。

### 误区 3：get 不加锁就是线程不安全

`get` 不加锁但依赖 volatile 语义确保可见性，是正确的设计。对于读多写少的场景，不加锁的 `get` 能显著提升吞吐量。
