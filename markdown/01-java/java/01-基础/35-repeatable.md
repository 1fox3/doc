# @Repeatable

Java 8 引入，允许同一注解在同一元素上重复标注，本质是语法糖，底层依赖**容器注解**。

## 使用步骤

1. 定义**可重复注解**，加上 `@Repeatable(容器注解.class)`。
2. 定义**容器注解**，必须包含返回可重复注解数组的 `value()` 方法。
3. 容器注解的 `@Retention` 必须 **≥** 可重复注解的 `@Retention`，否则编译报错。

编译器自动将多个重复注解包装进容器注解，运行期通过 `getAnnotationsByType()` 展开读取。

## 示例：权限校验

```java
// 1. 容器注解
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
public @interface RequireRoles {
    RequireRole[] value();
}

// 2. 可重复注解
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Repeatable(RequireRoles.class)
public @interface RequireRole {
    String value();
    boolean allRequired() default false;
}

// 3. 使用
public class OrderController {
    @RequireRole("ADMIN")
    @RequireRole("SUPER_ADMIN")
    public void deleteOrder(long orderId) {}

    @RequireRole(value = "OPERATOR", allRequired = true)
    @RequireRole(value = "FINANCE",  allRequired = true)
    public void exportBill() {}
}
```

## 示例：多规则校验

```java
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
@interface Validations { Validate[] value(); }

@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
@Repeatable(Validations.class)
@interface Validate {
    String rule();
    String message();
}

class UserForm {
    @Validate(rule = "notBlank",  message = "用户名不能为空")
    @Validate(rule = "maxLen:20", message = "用户名不超过20字符")
    @Validate(rule = "pattern:[a-zA-Z0-9_]+", message = "用户名只允许字母数字下划线")
    private String username;
}
```

## 反射读取

| 方法 | 说明 |
|------|------|
| `getAnnotation(T.class)` | 只返回单个注解，标注多个时返回 `null` |
| `getAnnotationsByType(T.class)` | 自动展开容器注解，返回所有重复注解数组，**推荐** |
| `getDeclaredAnnotationsByType(T.class)` | 同上，但不查找继承的注解 |

```java
Method m = OrderController.class.getMethod("deleteOrder", long.class);

RequireRole single = m.getAnnotation(RequireRole.class);   // null（标注多个时）
RequireRole[] all  = m.getAnnotationsByType(RequireRole.class); // length = 2
```

## 注意点

- **Retention 不匹配**：容器注解的 `@Retention` 必须 ≥ 可重复注解，通常两者都用 `RUNTIME`。
- **只标注一次**：字节码存的是可重复注解本身，`getAnnotationsByType` 两种情况都能正确处理，`getAnnotation(容器.class)` 在只标注一次时返回 `null`。
- **继承行为**：`@Inherited` 只对类注解有效，不会自动合并父子类的重复注解。
- **Spring 场景**：直接用 JDK 的 `getAnnotationsByType` 可能遗漏组合注解（`@AliasFor`），Spring 场景用 `AnnotatedElementUtils.getMergedRepeatableAnnotations`。

## 典型场景

| 场景 | 示例 |
|------|------|
| 权限控制 | `@RequireRole("ADMIN") @RequireRole("OPS")` |
| 定时任务多时间点 | `@Schedule("0 0 8 * * ?") @Schedule("0 0 20 * * ?")` |
| 字段多规则校验 | `@Validate(rule="notBlank") @Validate(rule="maxLen:20")` |
| 多数据源路由 | `@DataSource("master") @DataSource("slave")` |
