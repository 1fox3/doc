# 核心组件

## HandlerMapping

`HandlerMapping` 负责根据请求路径、HTTP 方法、请求头、参数等条件查找 Handler。常用实现是 `RequestMappingHandlerMapping`，负责解析 `@RequestMapping`、`@GetMapping`、`@PostMapping` 等注解。

## HandlerAdapter

`HandlerAdapter` 屏蔽不同 Handler 调用方式。`RequestMappingHandlerAdapter` 负责调用基于注解的 Controller 方法，并整合参数解析、数据绑定、消息转换和返回值处理。

## HttpMessageConverter

`HttpMessageConverter` 负责 HTTP 请求体和 Java 对象之间的转换，也负责 Java 对象到响应体的序列化。

常见转换器包括：

- `MappingJackson2HttpMessageConverter`：JSON 与对象转换。
- `StringHttpMessageConverter`：字符串响应。
- `ByteArrayHttpMessageConverter`：字节数组响应。
- `FormHttpMessageConverter`：表单数据处理。

`@RequestBody` 和 `@ResponseBody` 都依赖消息转换器。

## ViewResolver

传统 MVC 返回视图名时，`ViewResolver` 负责把逻辑视图名解析为具体视图。前后端分离项目通常直接返回 JSON，视图解析使用较少。

## HandlerExceptionResolver

异常解析器负责把 Controller 抛出的异常转换为 `ModelAndView` 或 HTTP 响应。常见机制包括 `@ExceptionHandler`、`@ResponseStatus`、`ResponseStatusException` 和全局 `@ControllerAdvice`。
