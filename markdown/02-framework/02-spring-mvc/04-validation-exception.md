# 异常处理、校验与拦截

## 参数校验

Spring MVC 集成 Bean Validation。常用方式：

- `@Valid` 或 `@Validated` 触发对象校验。
- `@NotNull`、`@NotBlank`、`@Size`、`@Min`、`@Max` 等声明字段约束。
- `BindingResult` 紧跟被校验参数时，可由业务代码自行处理校验结果。
- 方法参数级校验需要配合 `@Validated` 标注 Controller 类或配置方法校验。

## 全局异常处理

`@ControllerAdvice` 可集中定义异常处理逻辑。`@ExceptionHandler` 方法可根据异常类型返回统一错误响应。

典型分类包括：

- 参数绑定异常。
- 参数校验异常。
- 业务异常。
- 权限异常。
- 外部依赖异常。
- 未知系统异常。

## 拦截器

`HandlerInterceptor` 提供三个钩子：

- `preHandle`：Controller 执行前，可用于鉴权、幂等校验、链路信息初始化。
- `postHandle`：Controller 正常返回后、视图渲染前执行。
- `afterCompletion`：请求完成后执行，可用于清理 ThreadLocal、记录耗时。

拦截器只对 Spring MVC 匹配的 Handler 生效。静态资源、错误转发、异步请求恢复等场景需要结合配置确认是否进入拦截器。

## 跨域处理

跨域可通过 `@CrossOrigin`、`WebMvcConfigurer#addCorsMappings` 或 Filter 处理。认证系统中如果使用 Cookie 或 Authorization 头，需要同时正确配置允许来源、允许头、允许方法和凭证策略。
