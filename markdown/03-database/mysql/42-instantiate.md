# instantiate

## 归属说明

- `instantiate` 不是 MySQL 技术主题，通常表示“实例化对象”。
- 该条目更符合 Spring Bean 创建或 CGLIB 动态代理语境，应从 MySQL 重点复习内容中排除。

## Spring/CGLIB 语境

- 普通 Bean 可通过构造器、工厂方法或反射实例化。
- 存在方法覆盖或 lookup method 时，Spring 可能生成 CGLIB 子类再实例化。
- CGLIB 基于继承实现，无法覆盖 `final` 方法，也不能代理 `final` 类。

## 避免混淆

- MySQL instance 指数据库实例，包括进程、配置、数据目录、端口、socket、redo/undo 等运行时资源。
- MySQL 启动初始化不是 Java 对象实例化，相关内容应查看服务启动和基础架构文档。

## 建议后续整理

- 如果保留 MySQL 目录纯度，可将本文件移动到 Java 或 Spring 相关目录，并在 README 中删除该链接。
- 如果暂时不移动，应在复习时明确跳过，避免降低 MySQL 知识体系的一致性。
- 如果整理 Spring 内容，可扩展 BeanDefinition 加载、实例化、依赖注入、初始化回调、BeanPostProcessor、AOP 代理和销毁流程。
