# switch支持的数据类型

## 支持类型

| 类别 | 具体类型 |
|------|----------|
| 基本类型 | `byte`、`short`、`char`、`int` |
| 包装类型 | `Byte`、`Short`、`Character`、`Integer` |
| 枚举 | `enum` |
| 字符串 | `String`（Java 7+） |
| 不支持 | `long`、`float`、`double`、`boolean` |

## 注意点

- `String` switch 底层先通过 `hashCode` 分组，再用 `equals` 精确匹配，不是简单整数跳转。
- Java 14+ 引入 switch expression 和模式匹配，表达能力更强。
