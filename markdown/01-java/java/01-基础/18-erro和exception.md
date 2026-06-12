# Error和Exception

## Throwable 体系

```
Throwable
├── Error（严重错误，通常无法恢复）
│   ├── OutOfMemoryError
│   └── NoClassDefFoundError
└── Exception（可捕获处理）
    ├── 受检异常（非 RuntimeException，编译器强制处理）
    │   ├── IOException
    │   ├── ClassNotFoundException
    │   └── SQLException
    └── 非受检异常 RuntimeException（运行期异常，通常为编程错误）
        ├── NullPointerException
        ├── IllegalArgumentException
        ├── NumberFormatException
        └── ClassCastException
```

## Throwable 常用方法

| 方法 | 说明 |
|------|------|
| `getMessage()` | 返回异常的简要描述 |
| `toString()` | 返回异常的详细信息（类名 + message） |
| `getLocalizedMessage()` | 返回本地化描述，未覆盖时等同于 `getMessage()` |
| `printStackTrace()` | 在控制台打印完整堆栈信息 |

## 注意点

- 不要捕获 `Throwable` 或 `Error` 后继续正常执行，仅在框架边界做日志和隔离时允许。
- 不要空 catch，至少记录关键上下文。
- 对外接口统一异常响应，不要把内部堆栈直接暴露给调用方。
- 业务异常通常设计为 `RuntimeException` 子类，配合统一异常处理和错误码使用。
