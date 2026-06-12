# 请求处理链路

## DispatcherServlet

`DispatcherServlet` 是 Spring MVC 的前端控制器，负责统一接收请求并调度后续组件。它本身不直接处理业务逻辑，而是通过策略接口完成请求匹配、方法调用、异常处理和结果渲染。

## 初始化过程

`DispatcherServlet` 初始化时会从容器中查找或创建默认策略组件，包括：

- `HandlerMapping`
- `HandlerAdapter`
- `HandlerExceptionResolver`
- `ViewResolver`
- `LocaleResolver`
- `MultipartResolver`

这些策略组件可以通过注册同类型 Bean 覆盖或扩展。

## 请求调度流程

1. 检查是否为文件上传请求，并通过 `MultipartResolver` 包装请求。
2. 遍历 `HandlerMapping`，找到匹配的 HandlerExecutionChain。
3. 执行拦截器 `preHandle`。
4. 选择支持该 Handler 的 `HandlerAdapter`。
5. 调用目标 Controller 方法。
6. 执行拦截器 `postHandle`。
7. 处理返回值并渲染视图或写出响应体。
8. 执行拦截器 `afterCompletion`。

## Servlet 过滤器与 MVC 拦截器

- Filter 属于 Servlet 规范，作用范围更靠前，可处理编码、认证、日志、跨域等通用逻辑。
- HandlerInterceptor 属于 Spring MVC，只对匹配到 Handler 的请求生效，可访问 HandlerMethod 和 ModelAndView。
- `@ControllerAdvice` 更适合做 Controller 层异常转换、数据绑定和全局模型增强。
