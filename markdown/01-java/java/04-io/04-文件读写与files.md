# 文件读写与 Files API

## 自动创建文件

以下 API 在目标文件不存在时通常可以创建文件，但不会自动创建不存在的父目录：

- `FileOutputStream`
- `FileWriter`
- `PrintWriter`
- `Files.newOutputStream`
- `Files.writeString`
- `Files.write`

如果父目录可能不存在，应先调用 `Files.createDirectories(path.getParent())`。

```java
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public class CreateFileDemo {
    public static void writeConfig(Path path, String content) throws IOException {
        Path parent = path.getParent();
        if (parent != null) {
            Files.createDirectories(parent);
        }
        Files.writeString(path, content, StandardCharsets.UTF_8);
    }
}
```

## 常见写文件方式

| API | 适用场景 |
| --- | --- |
| `FileOutputStream` | 写二进制数据或与旧代码集成 |
| `BufferedOutputStream` | 频繁小块写二进制数据 |
| `FileWriter` | 简单文本写入，但要注意默认编码问题 |
| `BufferedWriter` | 频繁小块写文本、按行写文本 |
| `PrintWriter` | 格式化文本输出 |
| `Files.write` | 一次性写入字节数组或多行文本 |
| `Files.writeString` | Java 11 起，一次性写入字符串 |

## 推荐的文本读写

```java
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class FilesTextDemo {
    public static void appendLine(Path path, String line) throws IOException {
        Path parent = path.getParent();
        if (parent != null) {
            Files.createDirectories(parent);
        }
        Files.writeString(
                path,
                line + System.lineSeparator(),
                StandardCharsets.UTF_8,
                java.nio.file.StandardOpenOption.CREATE,
                java.nio.file.StandardOpenOption.APPEND);
    }

    public static List<String> readAllLines(Path path) throws IOException {
        return Files.readAllLines(path, StandardCharsets.UTF_8);
    }
}
```

`readAllLines` 和 `readString` 会把文件内容一次性加载到内存，大文件应使用流式处理。

## 大文件流式处理

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public class LargeFileDemo {
    public static long countLines(Path path) throws IOException {
        long count = 0;
        try (BufferedReader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
            while (reader.readLine() != null) {
                count++;
            }
        }
        return count;
    }
}
```

## 文件复制

```java
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

public class FileCopyDemo {
    public static void copyByFiles(Path source, Path target) throws IOException {
        Path parent = target.getParent();
        if (parent != null) {
            Files.createDirectories(parent);
        }
        Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);
    }

    public static void copyByStream(Path source, Path target) throws IOException {
        Path parent = target.getParent();
        if (parent != null) {
            Files.createDirectories(parent);
        }
        try (InputStream in = Files.newInputStream(source);
             OutputStream out = Files.newOutputStream(target)) {
            in.transferTo(out);
        }
    }
}
```

## RandomAccessFile

`RandomAccessFile` 支持从指定位置读写，适合断点续传、固定格式文件、简单索引文件等场景。它既不是 `InputStream`，也不是 `OutputStream`，但可以通过 `getChannel()` 获取 `FileChannel`。

```java
import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;

public class RandomAccessFileDemo {
    public static void overwriteHeader(Path path, String header) throws IOException {
        try (RandomAccessFile file = new RandomAccessFile(path.toFile(), "rw")) {
            file.seek(0);
            file.write(header.getBytes(StandardCharsets.UTF_8));
        }
    }
}
```

## WatchService

`WatchService` 可以监听目录变化，常见事件包括 `ENTRY_CREATE`、`ENTRY_DELETE` 和 `ENTRY_MODIFY`。它用于目录级监听，不适合替代高精度实时事件系统。

```java
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.StandardWatchEventKinds;
import java.nio.file.WatchEvent;
import java.nio.file.WatchKey;
import java.nio.file.WatchService;

public class WatchServiceDemo {
    public static void watchOnce(Path directory) throws IOException, InterruptedException {
        try (WatchService watchService = directory.getFileSystem().newWatchService()) {
            directory.register(
                    watchService,
                    StandardWatchEventKinds.ENTRY_CREATE,
                    StandardWatchEventKinds.ENTRY_DELETE,
                    StandardWatchEventKinds.ENTRY_MODIFY);

            WatchKey key = watchService.take();
            for (WatchEvent<?> event : key.pollEvents()) {
                System.out.printf("%s: %s%n", event.kind(), event.context());
            }
            key.reset();
        }
    }
}
```
