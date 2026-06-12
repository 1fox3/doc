# Spring MVC

Spring MVC 是基于 Servlet API 的 Web MVC 框架，核心是 `DispatcherServlet` 前端控制器和一组可插拔策略组件。请求从 Servlet 容器进入后，由 HandlerMapping 定位处理器，由 HandlerAdapter 调用目标方法，再经过参数解析、类型转换、数据绑定、返回值处理和视图或响应体渲染完成响应。

## 技术专题

- [请求处理链路](01-request-flow.md)
- [核心组件](02-core-components.md)
- [参数绑定与返回值处理](03-binding-return.md)
- [异常处理、校验与拦截](04-validation-exception.md)

## 基本链路

1. `DispatcherServlet` 接收请求。
2. 通过 `HandlerMapping` 查找 Handler 和拦截器链。
3. 通过 `HandlerAdapter` 调用 Controller 方法。
4. 使用 `HandlerMethodArgumentResolver` 解析方法参数。
5. 执行业务方法。
6. 使用 `HandlerMethodReturnValueHandler` 处理返回值。
7. 发生异常时交给 `HandlerExceptionResolver` 处理。
8. 返回 `ModelAndView`、视图渲染结果或 HTTP 响应体。
