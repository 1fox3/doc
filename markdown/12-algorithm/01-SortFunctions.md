# 10大排序算法（Java实现）

| 算法 | 最好时间复杂度 | 平均时间复杂度 | 最坏时间复杂度 | 空间复杂度 | 稳定性 | 比较排序 |
| --- | --- | --- | --- | --- | --- | --- |
| 冒泡排序 | O(n) | O(n²) | O(n²) | O(1) | 稳定 | 是 |
| 选择排序 | O(n²) | O(n²) | O(n²) | O(1) | 不稳定 | 是 |
| 插入排序 | O(n) | O(n²) | O(n²) | O(1) | 稳定 | 是 |
| 希尔排序 | O(n log n)（依赖增量） | O(n^1.3~n^1.5)（常见） | O(n²) | O(1) | 不稳定 | 是 |
| 归并排序 | O(n log n) | O(n log n) | O(n log n) | O(n) | 稳定 | 是 |
| 快速排序 | O(n log n) | O(n log n) | O(n²) | O(log n)（递归栈） | 不稳定 | 是 |
| 堆排序 | O(n log n) | O(n log n) | O(n log n) | O(1) | 不稳定 | 是 |
| 计数排序 | O(n + k) | O(n + k) | O(n + k) | O(n + k) | 稳定 | 否 |
| 桶排序 | O(n + k) | O(n + k)（分布均匀） | O(n²) | O(n + k) | 视桶内排序而定 | 否（通常） |
| 基数排序 | O(d × (n + k)) | O(d × (n + k)) | O(d × (n + k)) | O(n + k) | 稳定 | 否 |

## 1. 冒泡排序

重复比较相邻两个元素，把较大的元素逐步“冒泡”到数组末尾。

```java
public static void bubbleSort(int[] arr) {
    int n = arr.length;
    for (int i = 0; i < n - 1; i++) {
        boolean swapped = false;
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                int tmp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = tmp;
                swapped = true;
            }
        }
        if (!swapped) {
            break;
        }
    }
}
```

## 2. 选择排序

每轮从未排序区间中选择最小值，放到当前轮次的起始位置。

```java
public static void selectionSort(int[] arr) {
    int n = arr.length;
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIdx]) {
                minIdx = j;
            }
        }
        if (minIdx != i) {
            int tmp = arr[i];
            arr[i] = arr[minIdx];
            arr[minIdx] = tmp;
        }
    }
}
```

## 3. 插入排序

将元素逐个插入到前面已排序区间中的正确位置，类似打扑克牌理牌。

```java
public static void insertionSort(int[] arr) {
    for (int i = 1; i < arr.length; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}
```

## 4. 希尔排序

按不同步长分组做插入排序，逐步缩小步长以减少整体移动次数。

```java
public static void shellSort(int[] arr) {
    int n = arr.length;
    for (int gap = n / 2; gap > 0; gap /= 2) {
        for (int i = gap; i < n; i++) {
            int temp = arr[i];
            int j = i;
            while (j >= gap && arr[j - gap] > temp) {
                arr[j] = arr[j - gap];
                j -= gap;
            }
            arr[j] = temp;
        }
    }
}
```

## 5. 归并排序

采用分治思想：先递归拆分，再将两个有序子数组合并成更大的有序数组。

```java
public static void mergeSort(int[] arr) {
    if (arr == null || arr.length <= 1) {
        return;
    }
    int[] temp = new int[arr.length];
    mergeSort(arr, 0, arr.length - 1, temp);
}

private static void mergeSort(int[] arr, int left, int right, int[] temp) {
    if (left >= right) {
        return;
    }
    int mid = left + (right - left) / 2;
    mergeSort(arr, left, mid, temp);
    mergeSort(arr, mid + 1, right, temp);
    merge(arr, left, mid, right, temp);
}

private static void merge(int[] arr, int left, int mid, int right, int[] temp) {
    int i = left, j = mid + 1, k = left;
    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j]) {
            temp[k++] = arr[i++];
        } else {
            temp[k++] = arr[j++];
        }
    }
    while (i <= mid) {
        temp[k++] = arr[i++];
    }
    while (j <= right) {
        temp[k++] = arr[j++];
    }
    for (int p = left; p <= right; p++) {
        arr[p] = temp[p];
    }
}
```

## 6. 快速排序

通过基准值分区，把小于基准的放左边、大于基准的放右边，再递归排序两侧。

```java
public static void quickSort(int[] arr) {
    quickSort(arr, 0, arr.length - 1);
}

private static void quickSort(int[] arr, int left, int right) {
    if (left >= right) {
        return;
    }
    int pivot = arr[left + (right - left) / 2];
    int i = left, j = right;
    while (i <= j) {
        while (arr[i] < pivot) {
            i++;
        }
        while (arr[j] > pivot) {
            j--;
        }
        if (i <= j) {
            int tmp = arr[i];
            arr[i] = arr[j];
            arr[j] = tmp;
            i++;
            j--;
        }
    }
    if (left < j) {
        quickSort(arr, left, j);
    }
    if (i < right) {
        quickSort(arr, i, right);
    }
}
```

## 7. 堆排序

先构建大顶堆，再反复把堆顶最大值交换到末尾并调整堆结构。

```java
public static void heapSort(int[] arr) {
    int n = arr.length;
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(arr, n, i);
    }
    for (int i = n - 1; i > 0; i--) {
        int tmp = arr[0];
        arr[0] = arr[i];
        arr[i] = tmp;
        heapify(arr, i, 0);
    }
}

private static void heapify(int[] arr, int heapSize, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < heapSize && arr[left] > arr[largest]) {
        largest = left;
    }
    if (right < heapSize && arr[right] > arr[largest]) {
        largest = right;
    }
    if (largest != i) {
        int tmp = arr[i];
        arr[i] = arr[largest];
        arr[largest] = tmp;
        heapify(arr, heapSize, largest);
    }
}
```

## 8. 计数排序

统计每个数值出现次数，再按计数结果回填，适合整数范围不大的场景。

```java
public static void countingSort(int[] arr) {
    if (arr.length <= 1) {
        return;
    }
    int min = arr[0], max = arr[0];
    for (int num : arr) {
        if (num < min) {
            min = num;
        }
        if (num > max) {
            max = num;
        }
    }
    int[] count = new int[max - min + 1];
    for (int num : arr) {
        count[num - min]++;
    }
    int idx = 0;
    for (int i = 0; i < count.length; i++) {
        while (count[i]-- > 0) {
            arr[idx++] = i + min;
        }
    }
}
```

## 9. 桶排序

将数据按区间分配到多个桶中，桶内分别排序后再按顺序合并。

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public static void bucketSort(int[] arr) {
    if (arr.length <= 1) {
        return;
    }
    int min = arr[0], max = arr[0];
    for (int num : arr) {
        if (num < min) {
            min = num;
        }
        if (num > max) {
            max = num;
        }
    }

    int bucketCount = arr.length;
    double interval = (double) (max - min + 1) / bucketCount;
    List<List<Integer>> buckets = new ArrayList<>(bucketCount);
    for (int i = 0; i < bucketCount; i++) {
        buckets.add(new ArrayList<>());
    }

    for (int num : arr) {
        int bucketIndex = (int) ((num - min) / interval);
        if (bucketIndex == bucketCount) {
            bucketIndex--;
        }
        buckets.get(bucketIndex).add(num);
    }

    int idx = 0;
    for (List<Integer> bucket : buckets) {
        Collections.sort(bucket);
        for (int num : bucket) {
            arr[idx++] = num;
        }
    }
}
```

## 10. 基数排序

按个位、十位、百位等位数从低到高依次排序，利用稳定排序完成整体有序。

```java
public static void radixSort(int[] arr) {
    if (arr.length <= 1) {
        return;
    }

    int max = arr[0];
    for (int num : arr) {
        if (num > max) {
            max = num;
        }
    }

    int exp = 1;
    int[] output = new int[arr.length];
    while (max / exp > 0) {
        int[] count = new int[10];
        for (int num : arr) {
            count[(num / exp) % 10]++;
        }
        for (int i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }
        for (int i = arr.length - 1; i >= 0; i--) {
            int digit = (arr[i] / exp) % 10;
            output[count[digit] - 1] = arr[i];
            count[digit]--;
        }
        System.arraycopy(output, 0, arr, 0, arr.length);
        exp *= 10;
    }
}
```
