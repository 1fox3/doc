# OQL

OQL 是 Object Query Language，常用于 MAT、VisualVM 等工具中查询堆转储里的对象、字段、引用关系和集合内容。

## 基本语法

```sql
select <表达式>
from <类或对象集合> <别名>
where <条件>
```

## 常用查询

查询所有字符串：

```sql
select s from java.lang.String s
```

查询长度大于 1000 的字符串：

```sql
select s from java.lang.String s where s.value.length > 1000
```

查询指定类实例：

```sql
select o from com.example.Order o
```

查询对象字段：

```sql
select {id: o.id, status: o.status} from com.example.Order o
```

查询 HashMap：

```sql
select m from java.util.HashMap m where m.size > 10000
```

## MAT 常用函数

- `toString(obj)`：显示对象字符串内容。
- `classof(obj)`：返回对象的 Class。
- `dominators(obj)`：返回支配对象。
- `outbounds(obj)`：返回对象引用出去的对象。
- `inbounds(obj)`：返回引用该对象的对象。
- `referrers(obj)`：返回引用者。
- `sizeof(obj)`：返回 shallow size。

## MAT 核心概念

- Shallow Heap：对象自身占用的内存，不包含它引用的对象。
- Retained Heap：如果该对象被回收后能够连带释放的总内存，更适合判断泄漏影响。
- Dominator：如果从 GC Roots 到对象 B 的所有路径都经过对象 A，则 A 支配 B。
- Immediate Dominator：离对象最近的支配者，Dominator Tree 基于这个关系构建。
- Path To GC Roots：查看对象为什么还活着，排查泄漏时通常选择排除弱引用、软引用等路径。

## 排查场景

### 查找大字符串

```sql
select {str: toString(s), len: s.value.length}
from java.lang.String s
where s.value.length > 4096
```

### 查找大集合

```sql
select {obj: l, size: l.size}
from java.util.ArrayList l
where l.size > 10000
```

### 查找 ClassLoader

```sql
select cl from java.lang.ClassLoader cl
```

### 查找线程对象

```sql
select t from java.lang.Thread t
```

### 查找 ThreadLocalMap

```sql
select t.threadLocals from java.lang.Thread t where t.threadLocals != null
```

### 查找 ClassLoader

```sql
select {loader: cl, parent: cl.parent} from java.lang.ClassLoader cl
```

### 查找大 byte 数组

```sql
select {array: a, size: a.@length} from byte[] a where a.@length > 1048576
```

## 使用建议

- 先看 Dominator Tree 和 Leak Suspects，再用 OQL 验证具体对象内容。
- 查询大堆时条件要尽量收敛，避免 OQL 本身消耗大量内存。
- 对集合内部结构查询要结合具体 JDK 版本，字段名可能不同。
- OQL 适合确认对象分布和字段值，不替代 GC Roots 引用链分析。
- MAT 的 OQL 语法和 VisualVM/OQL 细节并不完全一致，复杂查询要按工具实际支持调整。
