# main方法

## 核心规则

- 标准签名：`public static void main(String[] args)`，JVM 启动时只识别该签名。
- 可以重载，但 JVM 只调用标准签名的版本；作为静态方法可被子类继承，但无运行期多态重写意义。
- 去掉 `static` 后编译通过，运行时 JVM 找不到入口而失败。
- 可以用 `synchronized` 修饰，达到同步效果（极少使用）。
- Spring Boot 中 `main` 方法通常只负责调用 `SpringApplication.run` 启动应用上下文。
