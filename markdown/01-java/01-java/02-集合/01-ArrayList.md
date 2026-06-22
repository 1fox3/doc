# ArrayList 深入

> 关联：[集合总览](README.md)

## 内部结构

```java
public class ArrayList<E> extends AbstractList<E>
        implements List<E>, RandomAccess, Cloneable, Serializable {

    private static final int DEFAULT_CAPACITY = 10;

    // 两个共享空数组，用于区分"未指定容量"和"显式指定容量为 0"
    private static final Object[] EMPTY_ELEMENTDATA = {};
    private static final Object[] DEFAULTCAPACITY_EMPTY_ELEMENTDATA = {};

    transient Object[] elementData; // 实际存储数组，transient 使其不参与默认序列化
    private int size;               // 已存储元素数量（不等于数组长度）
}
```

`elementData` 被声明为 `transient` 是因为 `ArrayList` 自定义了序列化逻辑（`writeObject`/`readObject`），只序列化 `size` 和实际元素，跳过数组末尾的空槽，节省序列化体积。

## 初始化与懒加载

```java
// 无参构造：赋值特殊空数组，真正扩容发生在第一次 add
public ArrayList() {
    this.elementData = DEFAULTCAPACITY_EMPTY_ELEMENTDATA;
}

// 指定初始容量
public ArrayList(int initialCapacity) {
    if (initialCapacity > 0) {
        this.elementData = new Object[initialCapacity];
    } else if (initialCapacity == 0) {
        this.elementData = EMPTY_ELEMENTDATA;
    } else {
        throw new IllegalArgumentException(...);
    }
}
```

无参构造不会立即分配大小为 10 的数组，而是在第一次 `add` 时才真正分配。这样空列表对象的内存占用极小。

## 扩容流程

### 调用链

```
add(e)
  → ensureCapacityInternal(size + 1)
    → calculateCapacity(elementData, minCapacity)
    → ensureExplicitCapacity(minCapacity)
      → grow(minCapacity)          ← 真正分配新数组
```

### grow 方法

```java
private void grow(int minCapacity) {
    int oldCapacity = elementData.length;
    // 新容量 = 旧容量 + 旧容量 / 2 ≈ 1.5 倍
    int newCapacity = oldCapacity + (oldCapacity >> 1);

    // 如果计算出的新容量仍然不够，直接用 minCapacity
    if (newCapacity - minCapacity < 0)
        newCapacity = minCapacity;

    // 防止超出 MAX_ARRAY_SIZE
    if (newCapacity - MAX_ARRAY_SIZE > 0)
        newCapacity = hugeCapacity(minCapacity);

    elementData = Arrays.copyOf(elementData, newCapacity);
}

private static int hugeCapacity(int minCapacity) {
    if (minCapacity < 0) throw new OutOfMemoryError();
    return (minCapacity > MAX_ARRAY_SIZE) ? Integer.MAX_VALUE : MAX_ARRAY_SIZE;
}
```

`MAX_ARRAY_SIZE = Integer.MAX_VALUE - 8`，减 8 是因为部分 JVM 实现会在数组头部存储额外信息，留出余量避免 OOM。

### 第一次 add 的容量决策

```java
private static int calculateCapacity(Object[] elementData, int minCapacity) {
    if (elementData == DEFAULTCAPACITY_EMPTY_ELEMENTDATA) {
        // 无参构造的情况：第一次扩容至少为 DEFAULT_CAPACITY（10）
        return Math.max(DEFAULT_CAPACITY, minCapacity);
    }
    return minCapacity;
}
```

因此无参构造后第一次 `add`，数组长度从 0 直接变为 10，不是逐步增长的。

### 扩容次数估算

容量变化公式：`newCapacity = oldCapacity + (oldCapacity >> 1)`，即每次约 ×1.5（整数截断）。

| 元素数量 | 数组长度 | 扩容次数 | 容量变化路径 |
| --- | --- | --- | --- |
| 1 | 10 | 1 | 0→10 |
| 10 | 10 | 1 | 0→10 |
| 11 | 15 | 2 | 0→10→15 |
| 100 | 109 | 7 | 0→10→15→22→33→49→73→109 |
| 1000 | 1234 | 13 | 0→10→15→22→33→49→73→109→163→244→366→549→823→1234 |

### 提前分配容量

如果已知元素数量，应通过构造参数或 `ensureCapacity` 提前分配：

```java
List<Integer> list = new ArrayList<>(100_000);

// 或者在已有列表上扩容（通常用于批量添加前）
((ArrayList<Integer>) list).ensureCapacity(200_000);
```

## 插入与删除

### 尾部追加

```java
public boolean add(E e) {
    ensureCapacityInternal(size + 1);
    elementData[size++] = e;
    return true;
}
```

摊还 O(1)，只有触发扩容时才是 O(n)。

### 中间插入

```java
public void add(int index, E element) {
    rangeCheckForAdd(index);
    ensureCapacityInternal(size + 1);
    // index 之后的元素全部右移一位
    System.arraycopy(elementData, index, elementData, index + 1, size - index);
    elementData[index] = element;
    size++;
}
```

`System.arraycopy` 是 native 方法，底层是内存拷贝，比循环赋值快，但仍是 O(n)。

### 删除

```java
public E remove(int index) {
    rangeCheck(index);
    modCount++;
    E oldValue = elementData(index);
    int numMoved = size - index - 1;
    if (numMoved > 0)
        System.arraycopy(elementData, index + 1, elementData, index, numMoved);
    elementData[--size] = null; // 显式置 null，帮助 GC 回收
    return oldValue;
}
```

删除后末尾置 `null` 是为了释放对该对象的强引用，避免内存泄漏。

## modCount 与 fail-fast

`modCount` 是继承自 `AbstractList` 的字段，记录列表结构性修改次数（add、remove、扩容等）。

```java
// ArrayList 内的迭代器（简化版）
private class Itr implements Iterator<E> {
    int cursor;
    int lastRet = -1;
    int expectedModCount = modCount; // 创建时记录快照

    public E next() {
        checkForComodification();    // 每次 next 都检查
        // ...
    }

    final void checkForComodification() {
        if (modCount != expectedModCount)
            throw new ConcurrentModificationException();
    }
}
```

注意：`modCount` 不精确对应修改次数，多次扩容或批量操作可能只增加一次。`ConcurrentModificationException` 只能用于快速发现错误，不能作为线程安全的依据。

## SubList

`subList(fromIndex, toIndex)` 返回原列表的视图，不复制数据：

```java
List<String> origin = new ArrayList<>(List.of("a", "b", "c", "d"));
List<String> sub = origin.subList(1, 3); // [b, c]

sub.set(0, "B");
System.out.println(origin); // [a, B, c, d]，视图修改影响原列表

origin.add("e");
sub.get(0); // 抛 ConcurrentModificationException，原列表被结构性修改
```

对 SubList 的修改会立即反映到原列表。如果原列表在 SubList 存在期间发生结构性修改（增删元素），SubList 的任何操作都会抛 `ConcurrentModificationException`。

如果需要独立副本：

```java
List<String> copy = new ArrayList<>(origin.subList(1, 3));
```

## 排序

`ArrayList.sort` 委托给 `Arrays.sort`，后者对对象数组使用 TimSort。

```java
list.sort(Comparator.naturalOrder());
// 等价于
Collections.sort(list);
```

### TimSort 简介

TimSort 由 Tim Peters 于 2002 年为 Python 设计，Java 7 起用于对象数组排序。它是**归并排序 + 插入排序**的混合算法，针对真实数据通常含有局部有序区间的特点进行了优化。

**三个核心步骤：**

1. **识别 run**：扫描数组，找出自然升序或降序的连续子序列（降序 run 直接反转）
2. **短 run 补齐**：若 run 长度小于 minRun（通常 32~64），用插入排序向右延伸——插入排序在小规模近有序数据上常数极小
3. **按规则合并 run**：维护一个 run 栈，每压入新 run 后检查不变式 `|Z| > |Y| + |X|` 且 `|Y| > |X|`（X 栈顶、Y 次顶、Z 第三），**不满足时**立即归并相邻 run，保证归并树高度平衡

| 情形 | 时间复杂度 |
| --- | --- |
| 完全有序 / 完全逆序 | O(n) |
| 随机数据 | O(n log n) |

TimSort 是**稳定排序**，相等元素保持原始相对顺序。

### TimSort 演示

以数组 `[5, 3, 1, 4, 2, 8, 6, 7, 9, 10, 11, 12]` 为例，设 minRun = 4 演示完整流程。

---

**第一阶段：扫描并生成 run**

**run A**（从索引 0 开始）

```
原始：[ 5, 3, 1, | 4, 2, 8, 6, 7, 9, 10, 11, 12 ]
        ↑  ↑  ↑
        5 > 3 > 1，降序，下一个 4 打破顺序，自然 run 结束

自然 run = [5, 3, 1]，长度 3，降序 → 反转 → [1, 3, 5]

长度 3 < minRun 4，用二分插入排序向右借元素：
  取 a[3]=4，插入 [1, 3, 5] → [1, 3, 4, 5]

run A = [1, 3, 4, 5]，消耗索引 0~3
```

**run B**（从索引 4 开始）

```
原始：[ ..., | 2, 8, | 6, 7, 9, 10, 11, 12 ]
               ↑  ↑
               2 < 8，升序，下一个 6 < 8，打破顺序，自然 run 结束

自然 run = [2, 8]，长度 2，升序，无需反转

长度 2 < minRun 4，二分插入排序补齐：
  取 a[6]=6，插入 [2, 8] → [2, 6, 8]
  取 a[7]=7，插入 [2, 6, 8] → [2, 6, 7, 8]

run B = [2, 6, 7, 8]，消耗索引 4~7
```

**run C**（从索引 8 开始）

```
原始：[ ..., | 9, 10, 11, 12 ]
               ↑   ↑   ↑   ↑
               全程升序，到达数组末尾

自然 run = [9, 10, 11, 12]，长度 4 = minRun，无需补齐

run C = [9, 10, 11, 12]，消耗索引 8~11
```

---

**第二阶段：run 栈 + 合并**

每压入一个 run，检查栈是否满足不变式 `|Y| > |X|`（X 栈顶、Y 次顶），不满足则立即归并。

```
① 压入 A(4)
   栈：[ A(4) ]

② 压入 B(4)
   栈：[ A(4), B(4) ]
   检查：|A|=4 > |B|=4？不满足 → 归并 A + B

   归并 [1,3,4,5] 和 [2,6,7,8]（标准双路归并）：
   比较头元素：1<2 取1, 2<3 取2, 3<6 取3, 4<6 取4, 5<6 取5, 剩余[6,7,8]直接追加
   结果：[1, 2, 3, 4, 5, 6, 7, 8]

   栈：[ AB(8) ]

③ 压入 C(4)
   栈：[ AB(8), C(4) ]
   检查：|AB|=8 > |C|=4？满足 → 不合并

④ 数组遍历完毕，强制合并栈内剩余 run：
   归并 AB(8) + C(4)（逐元素比较）：
   比较 1 vs 9：取1, 比较 2 vs 9：取2 ... 比较 8 vs 9：取8，AB 耗尽，追加 C
   结果：[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
   注：追加 C 是因为 AB 末尾元素(8) < C 首元素(9)，这是本例数据的特殊情况，
       若 C=[1,3,4,5] 则需完整的逐元素交叉比较，归并始终不会跳过比较。
```

---

**整体流程对比**

```
原始数组  ：[ 5,  3,  1,  4,  2,  8,  6,  7,  9, 10, 11, 12 ]
识别 run  ：|--run A(逆序补齐)--|--run B(短run补齐)--|---run C---|
归并后    ：[ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12 ]
```

> **关键点**：run C 的 `[9,10,11,12]` 完全不需要排序，直接参与归并。如果输入数据本身就有大量有序区间，TimSort 能跳过大量比较，这正是它在近似有序数据上达到 O(n) 的原因。

## toArray 的陷阱

```java
List<String> list = new ArrayList<>(List.of("a", "b"));

// 返回 Object[]，类型是 Object[]，即使运行时元素都是 String
Object[] arr1 = list.toArray();

// 返回 String[]，正确做法
String[] arr2 = list.toArray(new String[0]);
```

`toArray()` 返回的是 `Object[]`，即使将其强转为 `String[]` 也会在运行时抛 `ClassCastException`。应始终使用 `toArray(T[])`。

传入长度为 0 的数组（`new String[0]`）是惯用写法，JVM 会根据反射信息推断正确类型，实际上不会使用这个传入的数组来存储结果（内部会新建合适大小的数组）。

## trimToSize

```java
list.trimToSize();
```

将底层数组收缩到与 `size` 相等，释放多余的预留空间。适合在构建完列表后需要长期持有且不再增减的场景。

## 性能小结

| 操作 | 时间复杂度 | 备注 |
| --- | --- | --- |
| `get(index)` | O(1) | 数组随机访问 |
| `add(e)` 尾部 | 摊还 O(1) | 扩容时 O(n) |
| `add(index, e)` 中间 | O(n) | 需要移动元素 |
| `remove(index)` | O(n) | 需要移动元素 |
| `contains(o)` | O(n) | 线性扫描 |
| `sort` | O(n log n) | TimSort |
| 扩容 | O(n) | Arrays.copyOf |
