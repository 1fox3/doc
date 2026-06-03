# DispatcherServlet

> 专题：Spring MVC
> 来源：面试内容汇总/Spring MVC.xmind

## 补充与实践

- 补充：请求链路可拆为过滤器、DispatcherServlet、HandlerMapping、HandlerAdapter、参数解析、消息转换和异常处理。
- 实践：统一异常处理应区分业务异常、参数异常、系统异常和下游异常，并输出可观测的 trace 信息。
- 误区：Filter 属于 Servlet 容器链路，Interceptor 属于 Spring MVC 链路，二者生命周期和能力边界不同。

## 脑图内容

## DispatcherServlet

### 介绍

#### DispatcherServlet是Spring MVC框架的核心组件之一，是Spring MVC的前端控制器，也是一个Servlet

#### DispatcherServlet它是整个请求处理流程的核心，它负责接受所有的客户端请求，根据请求的URL调用对应的控制器，然后将控制器返回的视图名交给视图解析器进行解析，并最终将渲染结果返回给客户端

### 工作流程

#### 客户端发送的请求被前端控制器DispatcherServlet捕获

#### DispatcherServlet根据servlet.xml配置的请求URL进行解析，得到请求资源标识符URI，让后根据URI调用HandlerMapping获得该Handler配置的所有相关的对象

#### 返回一个HandlerExecutionChain执行链对象

#### DispatcherServlet根据Handler选择一个合适的HandlerAdapter，并开始执行拦截器的preHandler方法

#### 根据Request中的模型数据填充Handler入参，并还是执行Handler(Controller)

- 将请求数据转换成对象，将对象转换为指定的响应信息

- 对请求数据进行转换

- 对请求数据进行格式化

- 验证数据有效性并将结果存储到BindingResult或Error中

#### Handler执行完成后，向HandlerAdapter返回一个ModelAndView对象

#### HandlerAdapter然后向DispatcherServlet返回ModelAndView对象

#### 根据返回的ModelAndView选择一个格式的ViewResolver

#### ViewResolver返回一个View视图对象个DispatcherServlet

#### 使用Model和View开始渲染视图

#### 视图负责将渲染结果呈现给客户端页面
