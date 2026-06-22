# try-catch-finally

## 执行顺序

| 场景 | 执行顺序 |
|------|----------|
| 正常执行 | `try` → `finally` |
| 异常被捕获 | `try`（异常前）→ `catch` → `finally` |
| 异常未被捕获 | `try`（异常前）→ `finally` → 异常向外抛出 |
| `try/catch` 中有 `return` | `finally` 在方法真正返回前仍会执行 |

## finally 不一定执行的情况

- `System.exit()` 导致 JVM 直接退出。
- JVM 崩溃或进程被强杀（如 `kill -9`）。
- 机器断电或线程在执行 `finally` 前被强制终止。

## return 与 finally

- `finally` 中有 `return` 会覆盖 `try/catch` 中的 `return`，且会吞掉异常。
- 不建议在 `finally` 中写 `return`、`throw` 新异常或执行复杂业务逻辑。

## 资源释放

- Java 7 后推荐 `try-with-resources`，资源类需实现 `AutoCloseable` 或 `Closeable`，编译器自动生成关闭逻辑。

## 注意点

- `catch` 顺序应从具体异常到父类异常。
- 不要用异常控制正常业务流程。
- `catch` 中至少记录关键上下文，不能空 catch 或只打印堆栈吞掉异常。

## 示例

```java
// try-with-resources：自动关闭资源
public static String readFirstLine(String path) throws IOException {
    try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
        return reader.readLine();
    }
}

// finally return 覆盖示例（不推荐）
public static int value() {
    try {
        return 1;
    } finally {
        return 2; // 实际返回 2，覆盖 try 中的 return
    }
}
```
