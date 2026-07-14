# 常见查找算法（Java实现）

| 算法 | 最好时间复杂度 | 平均时间复杂度 | 最坏时间复杂度 | 空间复杂度 | 需要有序数据 | 比较查找 |
| --- | --- | --- | --- | --- | --- | --- |
| 顺序查找 | O(1) | O(n) | O(n) | O(1) | 否 | 是 |
| 二分查找 | O(1) | O(log n) | O(log n) | O(1) | 是 | 是 |
| 插值查找 | O(1) | O(log log n)（分布均匀） | O(n) | O(1) | 是 | 是 |
| 斐波那契查找 | O(1) | O(log n) | O(log n) | O(1) | 是 | 是 |
| 树表查找（BST） | O(1) | O(log n) | O(n) | O(h) | 否 | 是 |
| 分块查找 | O(1) | O(√n) | O(√n) | O(1) | 块内可无序 | 是 |
| 哈希查找 | O(1) | O(1) | O(n) | O(n) | 否 | 否 |

## 1. 顺序查找

从头到尾依次比较，找到目标即返回下标，适合小规模或无序数据。

```java
public static int linearSearch(int[] arr, int target) {
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == target) {
            return i;
        }
    }
    return -1;
}
```

## 2. 二分查找

每次取中间元素比较，将查找区间缩小一半，要求数组有序。

```java
public static int binarySearch(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) {
            return mid;
        }
        if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1;
}
```

## 3. 插值查找

基于数值分布估算目标位置，分布越均匀越快，要求有序且数值型数据。

```java
public static int interpolationSearch(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left <= right && target >= arr[left] && target <= arr[right]) {
        if (arr[left] == arr[right]) {
            return arr[left] == target ? left : -1;
        }
        int pos = left + (int) (((long) (target - arr[left]) * (right - left))
                / (arr[right] - arr[left]));
        if (arr[pos] == target) {
            return pos;
        }
        if (arr[pos] < target) {
            left = pos + 1;
        } else {
            right = pos - 1;
        }
    }
    return -1;
}
```

## 4. 斐波那契查找

利用斐波那契数列划分区间进行查找，本质是二分查找的变体，要求有序。

```java
public static int fibonacciSearch(int[] arr, int target) {
    int n = arr.length;
    int fibMm2 = 0; // (m-2)'th Fibonacci
    int fibMm1 = 1; // (m-1)'th Fibonacci
    int fibM = fibMm2 + fibMm1; // m'th Fibonacci

    while (fibM < n) {
        fibMm2 = fibMm1;
        fibMm1 = fibM;
        fibM = fibMm2 + fibMm1;
    }

    int offset = -1;
    while (fibM > 1) {
        int i = Math.min(offset + fibMm2, n - 1);
        if (arr[i] < target) {
            fibM = fibMm1;
            fibMm1 = fibMm2;
            fibMm2 = fibM - fibMm1;
            offset = i;
        } else if (arr[i] > target) {
            fibM = fibMm2;
            fibMm1 = fibMm1 - fibMm2;
            fibMm2 = fibM - fibMm1;
        } else {
            return i;
        }
    }

    if (fibMm1 == 1 && offset + 1 < n && arr[offset + 1] == target) {
        return offset + 1;
    }
    return -1;
}
```

## 5. 树表查找（BST）

在二叉搜索树中按大小关系向左/右子树查找，树平衡时效率高。

```java
static class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;

    TreeNode(int val) {
        this.val = val;
    }
}

public static TreeNode bstSearch(TreeNode root, int target) {
    TreeNode cur = root;
    while (cur != null) {
        if (cur.val == target) {
            return cur;
        }
        cur = target < cur.val ? cur.left : cur.right;
    }
    return null;
}
```

## 6. 分块查找

先定位目标可能所在块，再在块内顺序查找，适合分块存储的数据。

```java
public static int blockSearch(int[] arr, int target, int blockSize) {
    if (arr.length == 0 || blockSize <= 0) {
        return -1;
    }

    int n = arr.length;
    int blockCount = (n + blockSize - 1) / blockSize;
    int[] blockMax = new int[blockCount];
    for (int b = 0; b < blockCount; b++) {
        int start = b * blockSize;
        int end = Math.min(start + blockSize, n);
        int max = arr[start];
        for (int i = start + 1; i < end; i++) {
            if (arr[i] > max) {
                max = arr[i];
            }
        }
        blockMax[b] = max;
    }

    int block = 0;
    while (block < blockCount && target > blockMax[block]) {
        block++;
    }
    if (block == blockCount) {
        return -1;
    }

    int start = block * blockSize;
    int end = Math.min(start + blockSize, n);
    for (int i = start; i < end; i++) {
        if (arr[i] == target) {
            return i;
        }
    }
    return -1;
}
```

## 7. 哈希查找

通过哈希函数直接定位槽位，平均查询很快，冲突严重时性能下降。

```java
import java.util.HashMap;
import java.util.Map;

public static int hashSearch(int[] arr, int target) {
    Map<Integer, Integer> indexMap = new HashMap<>();
    for (int i = 0; i < arr.length; i++) {
        indexMap.putIfAbsent(arr[i], i);
    }
    return indexMap.getOrDefault(target, -1);
}
```
