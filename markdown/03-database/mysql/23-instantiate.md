# instantiate

## 归属说明

- `instantiate` 不是 MySQL 核心知识点，更像 Spring/CGLIB 对象实例化相关术语。
- 如果该条目来自混合脑图，应从 MySQL 复习主线中剔除，避免和数据库实例启动、连接实例或存储引擎初始化混淆。

## Java/Spring 语境

- 无方法覆盖需求时，容器可直接通过构造器或反射实例化目标类。
- 存在方法注入、lookup method 或需要覆盖方法时，Spring 可能生成 CGLIB 子类，通过动态代理完成调用增强。
- CGLIB 通过继承生成子类，不能代理 `final` 类或 `final` 方法。

## 与 MySQL 的边界

- MySQL 的实例通常指一个运行中的 server 进程及其数据目录、端口、socket 和配置集合。
- MySQL 启动初始化应参考“服务启动”和“启动项和系统变量”，不要用 Java Bean 实例化概念解释数据库实例。

## 如果保留该文档的用途

- 可作为“脑图来源混入非 MySQL 条目”的标记，提醒后续整理时移动到 Java/Spring 目录。
- 如果面试复习围绕 MySQL，应跳过本条，不应把 CGLIB 代理和 MySQL 实例化混在同一回答。
- 如果需要整理 Spring Bean 生命周期，应补充实例化、属性填充、初始化、AOP 代理和销毁阶段，而不是放在数据库目录。
