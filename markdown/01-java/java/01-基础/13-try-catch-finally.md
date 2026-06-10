# try-catch-finally

> 专题：Java 语言基础
> 来源：面试内容汇总/Java.xmind

## 补充与实践

- 补充：异常处理要区分业务异常、系统异常和资源清理，重点掌握执行顺序与异常传播。
- 实践：资源关闭优先使用 `try-with-resources`，finally 中避免 return 或吞异常。
- 误区：finally 通常会执行，但不是绝对保证，例如 JVM 退出、进程被强杀或机器断电时不会执行。

## 详细说明

### 核心作用

- `try`：包裹可能抛出异常的代码。
- `catch`：捕获并处理指定类型的异常，可以有多个 catch，顺序应从具体异常到父类异常。
- `finally`：无论 try/catch 是否抛出异常，通常都会执行，常用于释放资源或做收尾动作。

### 执行顺序

- 正常执行：先执行 try，再执行 finally。
- 发生异常且被捕获：先执行 try 中异常前的代码，再执行匹配的 catch，最后执行 finally。
- 发生异常但未被捕获：先执行 try 中异常前的代码，再执行 finally，然后异常继续向外抛出。
- 如果 try 或 catch 中有 return，finally 通常仍会在方法真正返回前执行。

### finally 不一定执行的情况

- JVM 进程直接退出，例如 `System.exit(0)`。
- JVM 崩溃或进程被强杀，例如 `kill -9`。
- 执行 finally 前线程被强制终止或机器断电。
- CPU 关闭这种说法不准确，更准确地说是进程或虚拟机没有机会继续执行字节码。

### return 与 finally

- 如果 try/catch 和 finally 都有 return，finally 的 return 会覆盖前面的 return。
- 不建议在 finally 中写 return，因为它会吞掉异常或覆盖真实返回值，导致排查困难。
- 如果 finally 修改的是返回对象的内部状态，调用方可能看到修改后的对象；如果只是修改局部基本类型变量，通常不会改变已经确定的返回值。

### 资源释放

- 传统写法会在 finally 中关闭连接、流、锁等资源。
- Java 7 后更推荐 `try-with-resources`，由编译器自动生成关闭逻辑。
- 资源类需要实现 `AutoCloseable` 或 `Closeable`。

### try-with-resources 示例

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class TryWithResourcesDemo {
    public static String readFirstLine(String path) throws IOException {
        try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
            return reader.readLine();
        }
    }
}
```

### finally 覆盖 return 示例

```java
public class FinallyReturnDemo {
    public static int value() {
        try {
            return 1;
        } finally {
            return 2; // 不推荐：会覆盖 try 中的 return
        }
    }

    public static void main(String[] args) {
        System.out.println(value()); // 输出 2
    }
}
```

### 实践建议

- 不要用异常控制正常业务流程。
- catch 中至少要记录关键上下文，不能简单吞掉异常。
- 不要捕获过宽的异常后不处理，例如空 catch 或只打印堆栈。
- finally 中避免 return、throw 新异常或执行复杂业务逻辑。
- 资源关闭优先使用 try-with-resources。

### 复习检查

- 能用自己的话解释 `try-catch-finally`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `try-catch-finally` 展开，属于 `Java 语言基础` 的复习范围。
- 建议优先掌握：finally代码不一定执行。
- 二级节点提示了主要拆分角度：程序所在线程死亡, 关闭CPU。

### 复习追问

- `finally代码不一定执行` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## try-catch-finally

### finally代码不一定执行

#### 程序所在线程死亡

#### 关闭CPU
