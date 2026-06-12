# 参数绑定与返回值处理

## 参数解析

Spring MVC 使用 `HandlerMethodArgumentResolver` 解析 Controller 方法参数。常见注解和解析规则：

- `@PathVariable`：从 URI 模板变量绑定。
- `@RequestParam`：从查询参数或表单参数绑定。
- `@RequestHeader`：从请求头绑定。
- `@CookieValue`：从 Cookie 绑定。
- `@RequestBody`：通过 `HttpMessageConverter` 读取请求体。
- `@ModelAttribute`：绑定表单对象或模型属性。
- `Principal`、`HttpServletRequest`、`HttpServletResponse`：由框架直接注入。

## 类型转换

请求参数本质是字符串，Spring MVC 通过 `ConversionService`、`Converter`、`Formatter` 和 `PropertyEditor` 完成类型转换。建议优先使用 `Converter` 或 `Formatter` 扩展类型转换，避免使用全局副作用较强的旧式 `PropertyEditor`。

## 数据绑定

`WebDataBinder` 负责把请求参数绑定到 Java 对象，并配合校验器收集绑定错误。可通过 `@InitBinder` 定制允许字段、日期格式、转换器和校验器。

## 返回值处理

Spring MVC 使用 `HandlerMethodReturnValueHandler` 处理返回值：

- `@ResponseBody` 或 `ResponseEntity`：通过消息转换器写出响应体。
- `String`：可能表示视图名，也可能作为响应体，取决于注解。
- `ModelAndView`：同时携带模型和视图。
- `void`：可能由方法直接写响应，也可能推断默认视图。
- `Callable`、`DeferredResult`、`WebAsyncTask`：异步请求处理。

## REST 响应设计

REST 接口应明确状态码和响应体语义。创建资源可返回 `201 Created`，参数错误返回 `400 Bad Request`，认证失败返回 `401 Unauthorized`，权限不足返回 `403 Forbidden`，资源不存在返回 `404 Not Found`，服务端异常返回 `500 Internal Server Error`。
