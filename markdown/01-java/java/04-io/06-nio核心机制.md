# NIO 核心机制

## 核心对象

| 对象 | 说明 |
| --- | --- |
| `Buffer` | 数据缓冲区，核心状态包括 `capacity`、`position`、`limit` |
| `Channel` | 数据通道，可读可写，常见实现有 `FileChannel`、`SocketChannel`、`ServerSocketChannel` |
| `Selector` | 多路复用器，可让一个线程监听多个 Channel 的就绪事件 |

## Buffer 状态

| 属性 | 含义 |
| --- | --- |
| `capacity` | 缓冲区容量，创建后固定 |
| `position` | 下一个读写位置 |
| `limit` | 当前可读或可写边界 |

常用切换方法：

| 方法 | 作用 |
| --- | --- |
| `flip()` | 写模式切换到读模式，`limit = position`，`position = 0` |
| `clear()` | 清空状态用于重新写入，不会真正擦除底层数据 |
| `compact()` | 保留未读数据并切换到写模式 |

```java
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;

public class ByteBufferDemo {
    public static String readFromBuffer() {
        ByteBuffer buffer = ByteBuffer.allocate(32);
        buffer.put("hello".getBytes(StandardCharsets.UTF_8));

        buffer.flip();
        byte[] bytes = new byte[buffer.remaining()];
        buffer.get(bytes);
        return new String(bytes, StandardCharsets.UTF_8);
    }
}
```

## FileChannel

`FileChannel` 适合文件通道读写，也支持 `transferTo`、`transferFrom` 等方法。在操作系统支持时，这类方法可能利用零拷贝减少用户态和内核态之间的数据复制。

```java
import java.io.IOException;
import java.nio.channels.FileChannel;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public class FileChannelCopyDemo {
    public static void copy(Path source, Path target) throws IOException {
        try (FileChannel in = FileChannel.open(source, StandardOpenOption.READ);
             FileChannel out = FileChannel.open(
                     target,
                     StandardOpenOption.CREATE,
                     StandardOpenOption.WRITE,
                     StandardOpenOption.TRUNCATE_EXISTING)) {
            long position = 0;
            long size = in.size();
            while (position < size) {
                position += in.transferTo(position, size - position, out);
            }
        }
    }
}
```

## Selector 多路复用

基本流程：

1. 创建 `Selector`。
2. 将 `Channel` 设置为非阻塞模式。
3. 将 `Channel` 注册到 `Selector`，声明关注事件。
4. 调用 `select()` 等待就绪事件。
5. 遍历 `selectedKeys()`，处理对应 IO 事件。
6. 移除已处理的 key，必要时关闭 Channel 和 Selector。

常见事件：

| 事件 | 含义 |
| --- | --- |
| `SelectionKey.OP_ACCEPT` | 服务端接收连接就绪 |
| `SelectionKey.OP_CONNECT` | 客户端连接完成 |
| `SelectionKey.OP_READ` | 可读 |
| `SelectionKey.OP_WRITE` | 可写 |

```java
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.nio.charset.StandardCharsets;
import java.util.Iterator;

public class NioEchoServerDemo {
    public static void start(int port) throws IOException {
        try (Selector selector = Selector.open();
             ServerSocketChannel server = ServerSocketChannel.open()) {
            server.bind(new InetSocketAddress(port));
            server.configureBlocking(false);
            server.register(selector, SelectionKey.OP_ACCEPT);

            while (true) {
                selector.select();
                Iterator<SelectionKey> iterator = selector.selectedKeys().iterator();
                while (iterator.hasNext()) {
                    SelectionKey key = iterator.next();
                    iterator.remove();

                    if (key.isAcceptable()) {
                        ServerSocketChannel serverChannel = (ServerSocketChannel) key.channel();
                        SocketChannel client = serverChannel.accept();
                        client.configureBlocking(false);
                        client.register(selector, SelectionKey.OP_READ, ByteBuffer.allocate(1024));
                    } else if (key.isReadable()) {
                        SocketChannel client = (SocketChannel) key.channel();
                        ByteBuffer buffer = (ByteBuffer) key.attachment();
                        int read = client.read(buffer);
                        if (read == -1) {
                            client.close();
                            continue;
                        }
                        buffer.flip();
                        client.write(StandardCharsets.UTF_8.encode("echo: "));
                        client.write(buffer);
                        buffer.clear();
                    }
                }
            }
        }
    }
}
```

## Scatter 与 Gather

Scatter 是从一个 `Channel` 读取数据到多个 `Buffer`；Gather 是从多个 `Buffer` 写入一个 `Channel`。它适合把一段连续数据拆成不同逻辑部分处理，例如“协议头 + 消息体”。

可以把它理解成：

| 操作 | 数据流向 | 说明 |
| --- | --- | --- |
| Scatter read | `Channel -> Buffer[]` | 读取时把数据依次分散到多个 Buffer |
| Gather write | `Buffer[] -> Channel` | 写出时把多个 Buffer 的内容依次聚合到一个 Channel |

Scatter 读取时，`Channel` 会先写满第一个 `Buffer`，再继续写第二个 `Buffer`。例如 `header` 容量是 8，`body` 容量是 1024，那么前 8 个字节进入 `header`，后面的字节进入 `body`。

Gather 写出时，`Channel` 会先读取第一个 `Buffer` 的剩余内容，再读取第二个 `Buffer` 的剩余内容。因此写出前要把每个 `Buffer` 都切换到读模式，也就是调用 `flip()`。

```java
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public class ScatterGatherDemo {
    public static void splitRead(Path path) throws IOException {
        ByteBuffer header = ByteBuffer.allocate(8);
        ByteBuffer body = ByteBuffer.allocate(1024);

        try (FileChannel channel = FileChannel.open(path, StandardOpenOption.READ)) {
            channel.read(new ByteBuffer[]{header, body});
        }

        header.flip();
        body.flip();

        // 此时 header 中是前 8 个字节，body 中是后续内容。
        System.out.println("header bytes: " + header.remaining());
        System.out.println("body bytes: " + body.remaining());
    }

    public static void mergeWrite(Path path, byte[] headerBytes, byte[] bodyBytes) throws IOException {
        ByteBuffer header = ByteBuffer.wrap(headerBytes);
        ByteBuffer body = ByteBuffer.wrap(bodyBytes);

        try (FileChannel channel = FileChannel.open(
                path,
                StandardOpenOption.CREATE,
                StandardOpenOption.WRITE,
                StandardOpenOption.TRUNCATE_EXISTING)) {
            channel.write(new ByteBuffer[]{header, body});
        }
    }
}
```

注意：

- Scatter/Gather 只是决定数据在多个 `Buffer` 之间的读写顺序，不会自动解析业务协议。
- `read(ByteBuffer[])` 和 `write(ByteBuffer[])` 都可能只处理部分数据，网络编程中通常需要循环读写。
- 如果用 `allocate()` 后手动 `put()` 写入 Buffer，写出前需要 `flip()`；如果用 `ByteBuffer.wrap(byte[])`，Buffer 默认已经处于可读状态，不需要再 `flip()`。

## NIO 实践关注

- `Selector` 线程不要执行耗时业务逻辑，耗时任务应交给业务线程池。
- 非阻塞写可能只写出部分数据，需要维护待写缓冲并关注 `OP_WRITE`。
- `ByteBuffer.allocateDirect` 可减少部分复制，但分配和释放成本高，适合生命周期长、复用率高的场景。
- 真实项目通常使用 Netty 等 Reactor 框架，而不是直接手写复杂 NIO 服务。
