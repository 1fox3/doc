# 集合

> 专题：Java 语言基础  
> 来源：面试内容汇总/Java.xmind

## 文档导航

| 文件 | 内容 |
| --- | --- |
| [README.md](README.md)（本文件） | 集合体系、泛型、迭代器、选型、面试追问 |
| [01-ArrayList.md](01-ArrayList.md) | ArrayList 扩容细节、SubList、迭代器实现 |
| [02-HashMap.md](02-HashMap.md) | HashMap 哈希函数、put/resize/树化全流程 |
| [03-ConcurrentHashMap.md](03-ConcurrentHashMap.md) | JDK 7/8 并发实现、CAS、计数机制 |
| [04-红黑树.md](04-红黑树.md) | 红黑树性质、旋转、插入/删除修复、Java 中的应用 |

## 学习重点

Java 集合不是单纯背 API，重点应放在数据结构、复杂度、扩容策略、迭代一致性、线程安全和适用场景上。

- 选择集合时先判断数据模型：顺序、唯一性、键值映射、优先级、并发读写、阻塞等待。
- 面试回答时优先说明底层结构、关键方法流程、边界条件和工程取舍。
- 并发场景不要直接用外部大锁包裹普通集合，优先考虑并发容器、不可变快照或业务级原子操作。
- `ConcurrentHashMap` 只能保证单次方法调用线程安全，复合业务逻辑要使用 `compute`、`merge`、`putIfAbsent` 等原子 API。

## 集合体系

### 类继承关系图

下面只列常见面试和工程中高频出现的接口、抽象类与实现类，省略部分内部实现细节。为了避免混淆，`extends` 表示类继承或接口继承，`implements` 表示类实现接口。

#### Collection 类继承

```text
Iterable
└── Collection
    └── AbstractCollection
        ├── AbstractList
        │   ├── ArrayList
        │   ├── AbstractSequentialList
        │   │   └── LinkedList
        │   └── Vector
        │       └── Stack
        ├── AbstractSet
        │   ├── HashSet
        │   │   └── LinkedHashSet
        │   ├── TreeSet
        │   └── CopyOnWriteArraySet
        ├── AbstractQueue
        │   ├── PriorityQueue
        │   ├── ArrayBlockingQueue
        │   ├── LinkedBlockingQueue
        │   ├── PriorityBlockingQueue
        │   ├── DelayQueue
        │   ├── SynchronousQueue
        │   ├── LinkedTransferQueue
        │   └── LinkedBlockingDeque
        └── ArrayDeque

CopyOnWriteArrayList
└── 直接继承 Object，实现 List
```

#### Collection 接口实现

```text
Collection
├── List
│   ├── ArrayList implements List, RandomAccess
│   ├── LinkedList implements List, Deque
│   ├── Vector implements List, RandomAccess
│   └── CopyOnWriteArrayList implements List, RandomAccess
├── Set
│   ├── HashSet implements Set
│   ├── LinkedHashSet extends HashSet implements Set
│   ├── SortedSet
│   │   └── NavigableSet
│   │       └── TreeSet implements NavigableSet
│   └── CopyOnWriteArraySet implements Set
└── Queue
    ├── Deque
    │   ├── ArrayDeque implements Deque
    │   ├── LinkedList implements Deque
    │   └── BlockingDeque
    │       └── LinkedBlockingDeque implements BlockingDeque
    ├── BlockingQueue
    │   ├── ArrayBlockingQueue implements BlockingQueue
    │   ├── LinkedBlockingQueue implements BlockingQueue
    │   ├── PriorityBlockingQueue implements BlockingQueue
    │   ├── DelayQueue implements BlockingQueue
    │   ├── SynchronousQueue implements BlockingQueue
    │   ├── TransferQueue
    │   │   └── LinkedTransferQueue implements TransferQueue
    │   └── BlockingDeque
    │       └── LinkedBlockingDeque implements BlockingDeque
    └── PriorityQueue implements Queue
```

#### Map 类继承与接口实现

```text
Dictionary
└── Hashtable implements Map

Map
├── AbstractMap
│   ├── HashMap implements Map
│   │   └── LinkedHashMap
│   ├── TreeMap implements NavigableMap
│   ├── WeakHashMap implements Map
│   ├── IdentityHashMap implements Map
│   └── ConcurrentHashMap implements ConcurrentMap
├── SortedMap
│   └── NavigableMap
│       └── TreeMap
├── ConcurrentMap
│   └── ConcurrentHashMap
└── Hashtable
```

关键点：

- `Map` 不继承 `Collection`，它是独立的键值映射体系。
- `LinkedHashSet` 继承自 `HashSet`，底层使用 `LinkedHashMap` 维护插入顺序。
- `LinkedList` 继承自 `AbstractSequentialList`，同时实现 `List` 和 `Deque`，既能当列表，也能当双端队列。
- `TreeSet` 底层依赖 `TreeMap`，`HashSet` 底层依赖 `HashMap`，`LinkedHashSet` 底层依赖 `LinkedHashMap`。
- `BlockingQueue`、`BlockingDeque` 属于 `java.util.concurrent`，是并发包中的阻塞队列接口。
- `Vector`、`Stack`、`Hashtable` 是早期同步容器，新代码通常不优先选择。

### Collection

`Collection` 表示一组对象，是 `List`、`Set`、`Queue` 的根接口。

| 类型 | 特点 | 常见实现 | 典型场景 |
| --- | --- | --- | --- |
| `List` | 有序、可重复、按索引访问 | `ArrayList`、`LinkedList`、`Vector`、`CopyOnWriteArrayList` | 列表、分页结果、按顺序处理数据 |
| `Set` | 不重复 | `HashSet`、`LinkedHashSet`、`TreeSet`、`CopyOnWriteArraySet` | 去重、集合运算、唯一元素维护 |
| `Queue` | 队列语义 | `ArrayDeque`、`PriorityQueue`、`BlockingQueue` | FIFO、优先级任务、生产消费 |

### Map

`Map` 存储键值对，不继承 `Collection`。

| 类型 | 特点 | 常见实现 | 典型场景 |
| --- | --- | --- | --- |
| 哈希表 | 按 hash 定位，平均 O(1) | `HashMap`、`LinkedHashMap`、`ConcurrentHashMap` | 缓存、索引、快速查找 |
| 排序 Map | 按 key 排序，O(log n) | `TreeMap` | 范围查询、排序遍历 |
| 特殊 Map | 特殊 key 语义 | `WeakHashMap`、`IdentityHashMap` | 弱引用缓存、引用相等判断 |
| 旧实现 | 同步方法，历史遗留 | `Hashtable` | 不推荐新代码使用 |

## 泛型

集合使用泛型的主要价值是把类型错误提前到编译期，并减少显式强转。

```java
List<String> names = new ArrayList<>();
names.add("Alice");

// 编译失败：Integer 不能加入 List<String>
// names.add(123);

String first = names.get(0); // 不需要强转
```

注意：Java 泛型基于类型擦除，运行期不会保留完整泛型信息，所以 `List<String>` 和 `List<Integer>` 在运行期都是 `List`。

## 排序接口

### Comparable

`Comparable` 定义对象的自然顺序，属于内部排序规则，接口在 `java.lang` 包中。

```java
class User implements Comparable<User> {
    private final String name;
    private final int age;

    User(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public int compareTo(User other) {
        return Integer.compare(this.age, other.age);
    }
}
```

### Comparator

`Comparator` 定义外部排序规则，适合一个类需要多种排序方式的场景，接口在 `java.util` 包中。

```java
List<String> names = new ArrayList<>(List.of("Tom", "Alice", "Bob"));

names.sort(Comparator.comparingInt(String::length)
                     .thenComparing(Comparator.naturalOrder()));
```

排序规则要满足自反性、传递性和一致性，否则 `TreeSet`、`TreeMap`、排序算法可能出现异常或结果不可预期。

## 迭代器

### Iterator 与 Enumeration

| 对比项 | `Iterator` | `Enumeration` |
| --- | --- | --- |
| 引入时间 | JDK 1.2 | JDK 1.0 |
| 操作能力 | 读取，也可通过 `remove` 删除 | 只读取 |
| fail-fast | 多数集合迭代器支持 | 不支持 |
| 使用建议 | 推荐 | 仅历史类中可能遇到 |

### fail-fast

多数非并发集合的迭代器会记录创建时的修改次数。如果迭代期间集合被结构性修改，且不是通过迭代器自身修改，通常会抛出 `ConcurrentModificationException`。

```java
List<String> list = new ArrayList<>(List.of("a", "b", "c"));

Iterator<String> iterator = list.iterator();
while (iterator.hasNext()) {
    if ("b".equals(iterator.next())) {
        iterator.remove(); // 正确：通过迭代器删除
    }
}
```

fail-fast 是错误检测机制，不是并发安全保证，不能依赖它做业务控制。

## 不可修改集合

`Collections.unmodifiableList` 返回只读视图，底层集合被修改后，视图也会变化。

```java
List<String> origin = new ArrayList<>(List.of("a", "b"));
List<String> view = Collections.unmodifiableList(origin);

origin.add("c");
System.out.println(view); // [a, b, c]

// view.add("d"); // UnsupportedOperationException
```

如果希望创建不可变快照，优先使用 `List.copyOf`、`Set.copyOf`、`Map.copyOf` 或 `List.of` 等工厂方法。

```java
List<String> snapshot = List.copyOf(origin);
origin.add("d");

System.out.println(snapshot); // [a, b, c]
```

## List

### ArrayList

`ArrayList` 基于 `Object[]` 动态数组实现，适合随机访问多、尾部追加多的场景。

- 默认首次扩容容量通常为 10。
- 扩容约为原容量的 1.5 倍。
- 支持 `RandomAccess`，按索引读取是 O(1)。
- 中间插入、删除需要移动元素，时间复杂度 O(n)。
- 非线程安全，迭代器是 fail-fast。

详细扩容机制、SubList、迭代器实现见 [01-ArrayList.md](01-ArrayList.md)。

### LinkedList

`LinkedList` 基于双向链表实现，同时实现 `List` 和 `Deque`。

- 随机访问需要从头或尾遍历，复杂度 O(n)。
- 已定位节点后的插入、删除成本低，但查找节点本身通常仍是 O(n)。
- 每个节点额外保存前驱、后继引用，内存开销更大。
- 适合队列、双端队列语义，不适合作为高频随机访问列表。

### Vector 与 Stack

`Vector` 方法使用 `synchronized` 修饰，是历史同步容器。`Stack` 继承自 `Vector`，也属于历史类。新代码通常使用 `ArrayList`、`ArrayDeque` 或并发容器替代。

### CopyOnWriteArrayList

`CopyOnWriteArrayList` 写入时复制底层数组，读操作无锁，适合读多写少、集合规模不大的场景。

```java
List<String> listeners = new CopyOnWriteArrayList<>();
listeners.add("listener-1");

for (String listener : listeners) {
    listeners.add("listener-2"); // 不影响当前快照迭代
}
```

缺点是写入成本高、内存占用高，不能用于高频写入场景。

## Set

### HashSet

`HashSet` 底层基于 `HashMap`，元素作为 key，value 使用固定占位对象。

- 不保证遍历顺序。
- 判断重复依赖 `hashCode` 和 `equals`。
- 自定义对象作为元素时必须正确实现 `equals` 和 `hashCode`。

### LinkedHashSet

`LinkedHashSet` 基于 `LinkedHashMap`，在去重基础上维护插入顺序。

### TreeSet

`TreeSet` 基于 `TreeMap`（红黑树），使用红黑树维护有序集合。

- 插入、删除、查找复杂度 O(log n)。
- 元素需要实现 `Comparable`，或者构造时传入 `Comparator`。
- 去重依据是排序比较结果 `compare == 0`，不完全等同于 `equals`。

## Map

### HashMap

`HashMap` 是最常用的哈希表实现，JDK 8 开始底层是数组 + 链表 + 红黑树。

详细哈希函数、put/get/resize 流程、树化机制见 [02-HashMap.md](02-HashMap.md)。

### LinkedHashMap

`LinkedHashMap` 在 `HashMap` 基础上增加双向链表，用于维护遍历顺序。

- `accessOrder=false`：按插入顺序遍历，默认行为。
- `accessOrder=true`：按访问顺序遍历，可实现 LRU。

```java
Map<Integer, String> lru = new LinkedHashMap<>(16, 0.75f, true) {
    @Override
    protected boolean removeEldestEntry(Map.Entry<Integer, String> eldest) {
        return size() > 3;
    }
};

lru.put(1, "a");
lru.put(2, "b");
lru.put(3, "c");
lru.get(1);
lru.put(4, "d");

System.out.println(lru.keySet()); // [3, 1, 4]
```

### TreeMap

`TreeMap` 基于红黑树，实现 `SortedMap` 和 `NavigableMap`，按 key 排序。

```java
TreeMap<Integer, String> map = new TreeMap<>();
map.put(10, "ten");
map.put(1, "one");
map.put(5, "five");

System.out.println(map.firstKey());        // 1
System.out.println(map.ceilingKey(6));     // 10
System.out.println(map.subMap(1, true, 10, false)); // {1=one, 5=five}
```

### IdentityHashMap

`IdentityHashMap` 使用 `==` 比较 key，而不是 `equals`，适合需要对象引用身份语义的特殊场景。

### WeakHashMap

`WeakHashMap` 的 key 是弱引用。当 key 没有其他强引用时，GC 后对应 entry 可能被回收。常用于不希望缓存阻止对象回收的场景。

## HashMap 与 Hashtable

| 对比项 | `HashMap` | `Hashtable` |
| --- | --- | --- |
| 线程安全 | 非线程安全 | 方法级 `synchronized` |
| 性能 | 通常更高 | 同步开销大 |
| null | 允许一个 null key，允许 null value | 不允许 null key/value |
| 继承关系 | 继承 `AbstractMap` | 继承 `Dictionary` |
| 默认容量 | 16 | 11 |
| 扩容 | 约 2 倍 | `2n + 1` |
| 底层结构 | JDK 8+ 数组 + 链表 + 红黑树 | 数组 + 链表 |
| 使用建议 | 常规首选 | 历史遗留，不推荐新代码 |

## 线程安全 Map

### Hashtable

`Hashtable` 通过同步方法保证线程安全，锁粒度大，并发性能差，不推荐新代码使用。

### Collections.synchronizedMap

`Collections.synchronizedMap(new HashMap<>())` 通过包装对象加互斥锁实现线程安全，复合操作仍需手动同步。

```java
Map<String, Integer> map = Collections.synchronizedMap(new HashMap<>());

synchronized (map) {
    if (!map.containsKey("a")) {
        map.put("a", 1);
    }
}
```

### ConcurrentHashMap

`ConcurrentHashMap` 是并发场景首选 Map。

| 对比项 | JDK 7 | JDK 8+ |
| --- | --- | --- |
| 核心结构 | `Segment` + 数组 + 链表 | 数组 + 链表 + 红黑树 |
| 加锁方式 | 分段锁，`Segment` 继承 `ReentrantLock` | CAS + `synchronized` 锁桶首节点 |
| 并发粒度 | 默认最多 16 个 Segment | 粒度更细，和桶分布有关 |
| 冲突处理 | 链表 | 链表 + 红黑树 |

详细实现见 [03-ConcurrentHashMap.md](03-ConcurrentHashMap.md)。

## Queue 与 Deque

### ArrayDeque

`ArrayDeque` 基于可扩容数组和双指针实现，适合作为栈或双端队列。

- 不允许存储 `null`。
- 通常比 `LinkedList` 更适合作为队列或栈。
- 非线程安全。

### PriorityQueue

`PriorityQueue` 使用数组实现二叉堆，默认小顶堆。

- 插入和删除堆顶复杂度 O(log n)。
- 获取堆顶 `peek` 是 O(1)。
- 非线程安全，不支持 `null`。
- 元素必须可比较，或者构造时传入 `Comparator`。

### BlockingQueue

阻塞队列适合生产者消费者模型，常用于线程池、异步任务、削峰。

| 实现 | 是否有界 | 特点 |
| --- | --- | --- |
| `ArrayBlockingQueue` | 有界 | 数组结构，创建时必须指定容量 |
| `LinkedBlockingQueue` | 可选有界 | 链表结构，不指定容量时容量很大 |
| `PriorityBlockingQueue` | 无界 | 按优先级出队 |
| `DelayQueue` | 无界 | 元素到期后才能出队 |
| `SynchronousQueue` | 无容量 | 生产和消费直接交接 |
| `LinkedTransferQueue` | 无界 | 支持 transfer 语义 |
| `LinkedBlockingDeque` | 可选有界 | 双端阻塞队列 |

#### 四组核心方法

| 行为 | 插入 | 删除 | 查看队首 |
| --- | --- | --- | --- |
| 抛异常 | `add` | `remove` | `element` |
| 返回特殊值 | `offer` | `poll` | `peek` |
| 一直阻塞 | `put` | `take` | 不支持 |
| 超时退出 | `offer(e, time, unit)` | `poll(time, unit)` | 不支持 |

生产环境使用阻塞队列时应优先选择有界队列，避免无限堆积导致 OOM。

## 常见对比

### ArrayList 与数组

| 对比项 | `ArrayList` | 数组 |
| --- | --- | --- |
| 长度 | 动态扩容 | 创建后固定 |
| 类型 | 泛型，不能直接存基本类型 | 可存基本类型和对象 |
| API | 提供增删改查方法 | 主要通过下标访问 |
| 使用灵活性 | 更高 | 更轻量 |
| 性能 | 有装箱和扩容成本 | 更直接 |

### ArrayList 与 LinkedList

| 对比项 | `ArrayList` | `LinkedList` |
| --- | --- | --- |
| 底层结构 | 动态数组 | 双向链表 |
| 随机访问 | O(1) | O(n) |
| 头部插入删除 | O(n) | 定位后 O(1) |
| 尾部追加 | 摊还 O(1) | O(1) |
| 内存占用 | 预留容量造成浪费 | 每个节点多两个引用 |
| 线程安全 | 否 | 否 |
| 适用场景 | 高频读取、尾部追加 | 队列、双端队列语义 |

### ArrayDeque 与 LinkedList

| 对比项 | `ArrayDeque` | `LinkedList` |
| --- | --- | --- |
| 底层结构 | 可扩容循环数组 | 双向链表 |
| null | 不允许 | 允许 |
| 内存局部性 | 更好 | 较差 |
| 扩容 | 需要 | 不需要数组扩容 |
| 推荐用法 | 栈、队列、双端队列首选 | 需要 List 能力时使用 |

## 选型建议

| 场景 | 推荐 |
| --- | --- |
| 按索引高频读取 | `ArrayList` |
| 去重且不关心顺序 | `HashSet` |
| 去重且保留插入顺序 | `LinkedHashSet` |
| 去重且排序 | `TreeSet` |
| key-value 快速查找 | `HashMap` |
| 按 key 排序或范围查询 | `TreeMap` |
| 读多写少并发列表 | `CopyOnWriteArrayList` |
| 并发 key-value 访问 | `ConcurrentHashMap` |
| 栈、队列、双端队列 | `ArrayDeque` |
| 生产者消费者 | `BlockingQueue` |
| 优先级任务 | `PriorityQueue` 或 `PriorityBlockingQueue` |

## 面试追问

### ArrayList 扩容为什么是 1.5 倍？

- 1.5 倍是在空间浪费和扩容频率之间做折中。
- 扩容过小会导致频繁复制数组，扩容过大会浪费内存。
- 扩容需要创建新数组并复制旧元素，时间复杂度 O(n)，在高频追加大量数据时可能产生性能抖动。
- 如果能预估元素数量，应通过构造参数或 `ensureCapacity` 提前设置容量。

### HashMap 容量为什么要保持 2 的幂？

- 容量是 2 的幂时，可以用 `(n - 1) & hash` 替代取模计算，定位桶下标更高效。
- `n - 1` 的二进制低位全是 1，可以更充分利用 hash 的低位，减少分布偏斜。
- 扩容为 2 倍后，节点迁移只需要判断 hash 的某一位，要么留在原下标，要么移动到 `原下标 + oldCapacity`。

### HashMap 什么时候链表转红黑树？

- 单个桶中链表节点数达到 `TREEIFY_THRESHOLD`（默认 8）时，可能触发树化。
- 如果 table 容量小于 `MIN_TREEIFY_CAPACITY`（默认 64），不会直接树化，而是优先扩容。
- 容量较小时冲突往往来自桶数量不足，扩容可以重新分散节点，树化反而会增加结构复杂度和内存开销。

### ConcurrentHashMap 为什么不允许 null key 和 null value？

- 并发场景下，`get(key)` 返回 `null` 无法区分 key 不存在还是 value 本身为 null。
- 这种歧义会影响并发判断和原子操作语义。
- `HashMap` 是非并发容器，可以通过 `containsKey` 再次判断，但 `ConcurrentHashMap` 中这种组合判断不是天然原子的。

### TreeSet 中 compareTo 返回 0 但 equals 返回 false 会怎样？

- `TreeSet` 判断元素是否重复依赖排序比较结果，而不是直接依赖 `equals`。
- 如果 `compare` 返回 0，`TreeSet` 会认为两个元素相同，即使 `equals` 返回 false。

```java
record User(String name, int age) {}

Set<User> users = new TreeSet<>(Comparator.comparingInt(User::age));
users.add(new User("Alice", 18));
users.add(new User("Bob", 18));

System.out.println(users.size()); // 1，因为 age 相同，比较结果为 0
```

### Collections.unmodifiableList 和 List.copyOf 有什么区别？

- `Collections.unmodifiableList` 返回只读视图，不能通过视图修改，但原集合变化会反映到视图中。
- `List.copyOf` 返回不可变快照，创建后不受原集合后续变化影响。
- `List.copyOf` 不允许元素为 `null`，如果原集合包含 `null` 会抛出 `NullPointerException`。

### fail-fast 和 fail-safe 有什么区别？

- fail-fast 迭代器检测到结构性并发修改时会尽快抛出 `ConcurrentModificationException`，典型如 `ArrayList`、`HashMap`。
- fail-safe 通常指基于快照或弱一致性的迭代，不会因为并发修改直接抛异常，典型如 `CopyOnWriteArrayList`、`ConcurrentHashMap`。
- fail-fast 不是线程安全机制，只是一种尽早暴露错误的检测手段。
