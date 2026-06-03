# Spring MVC

> 来源：面试内容汇总/Spring MVC.xmind

## 核心认知

- Spring MVC 围绕 DispatcherServlet 组织请求分发、参数绑定、调用控制器和视图/响应渲染。
- 理解 HandlerMapping、HandlerAdapter、Interceptor、MessageConverter 是排查 Web 问题的关键。

## 面试重点

- 请求处理链路、参数解析、数据绑定、异常处理、拦截器和过滤器区别。
- REST 接口返回、内容协商、JSON 序列化和统一响应/异常封装。

## 实践检查点

- 能定位接口 404、415、参数绑定失败和序列化异常。
- 能设计全局异常处理和请求链路日志。

## 版本与趋势

- Spring MVC 在 Spring 6 后同样迁移到 Jakarta Servlet API，过滤器、拦截器和异常处理链路仍是高频问题。
- 接口治理重点包括统一错误码、参数校验、幂等、限流、链路追踪和访问日志。

## 章节目录

- [基础](01-基础.md)
- [DispatcherServlet](02-dispatcherservlet.md)
- [重点组件](03-重点组件.md)
- [常用注解](04-常用注解.md)
- [instantiate](05-instantiate.md)
