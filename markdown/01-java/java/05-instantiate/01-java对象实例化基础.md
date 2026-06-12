# Java 对象实例化基础

## `new` 的大致流程

执行 `new User()` 并不是简单调用构造方法，JVM 通常会经历以下步骤：

1. 检查目标类是否已经完成加载、解析和初始化。
2. 在堆上为对象分配内存。
3. 将对象内存初始化为零值。
4. 设置对象头，例如 Mark Word、Klass Pointer 等。
5. 执行实例字段初始化、实例初始化块和构造方法。

```java
public class NewObjectDemo {
    static class User {
        private final String name;

        User(String name) {
            this.name = name;
        }

        String name() {
            return name;
        }
    }

    public static void main(String[] args) {
        User user = new User("leo");
        System.out.println(user.name());
    }
}
```

## 类初始化与对象初始化

| 阶段 | 触发对象 | 典型内容 |
| --- | --- | --- |
| 类初始化 | 类 | `static` 字段、静态代码块 |
| 对象初始化 | 对象实例 | 实例字段、实例代码块、构造方法 |

```java
public class InitializationOrderDemo {
    static class Example {
        static {
            System.out.println("static block");
        }

        private String value = initField();

        {
            System.out.println("instance block");
        }

        Example() {
            System.out.println("constructor");
        }

        private String initField() {
            System.out.println("field init");
            return "ok";
        }
    }

    public static void main(String[] args) {
        new Example();
        new Example();
    }
}
```

输出顺序中，`static block` 只会在类初始化时执行一次；实例字段初始化、实例代码块、构造方法会随每次对象创建执行。

## 构造方法不是普通方法

构造方法用于对象初始化，不会被继承，也不会被子类覆盖。子类构造方法必须直接或间接调用父类构造方法。

```java
public class ConstructorDemo {
    static class Parent {
        Parent(String name) {
            System.out.println("parent: " + name);
        }
    }

    static class Child extends Parent {
        Child() {
            super("base");
            System.out.println("child");
        }
    }
}
```

## 内存分配关注点

JVM 为对象分配内存时可能使用指针碰撞、空闲列表、TLAB 等机制，具体取决于堆是否规整、垃圾收集器实现和运行时参数。

| 机制 | 说明 |
| --- | --- |
| 指针碰撞 | 堆内存规整时移动分配指针即可完成分配 |
| 空闲列表 | 堆内存不规整时从可用内存块列表中选择空间 |
| TLAB | 每个线程在 Eden 区预先分配一小块内存，减少并发分配锁竞争 |

面试中不必把对象实例化讲成固定单一路径，更稳妥的表达是：JVM 规范定义语义，HotSpot 会根据收集器、逃逸分析和 JIT 优化选择具体实现。
