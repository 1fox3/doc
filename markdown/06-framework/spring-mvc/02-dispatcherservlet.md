# DispatcherServlet

> 专题：Spring MVC
> 来源：面试内容汇总/Spring MVC.xmind

## 补充与实践

- 补充：请求链路可拆为过滤器、DispatcherServlet、HandlerMapping、HandlerAdapter、参数解析、消息转换和异常处理。
- 实践：统一异常处理应区分业务异常、参数异常、系统异常和下游异常，并输出可观测的 trace 信息。
- 误区：Filter 属于 Servlet 容器链路，Interceptor 属于 Spring MVC 链路，二者生命周期和能力边界不同。

## 详细说明

### 是什么

- `DispatcherServlet` 是 `Spring MVC` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `DispatcherServlet` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `DispatcherServlet`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `DispatcherServlet` 展开，属于 `Spring MVC` 的复习范围。
- 建议优先掌握：介绍, 工作流程。
- 二级节点提示了主要拆分角度：DispatcherServlet是Spring MVC框架的核心组件之一，是Spring MVC的前端控制器，也是一个Servlet, DispatcherServlet它是整个请求处理流程的核心，它负责接受所有的客户端请求，根据请求的URL调用对应的控制器，然后将控制器返回的视图名交给视图解析器进行解析，并最终将渲染结果返回给客户端, 客户端发送的请求被前端控制器DispatcherServlet捕获, DispatcherServlet根据servlet.xml配置的请求URL进行解析，得到请求资源标识符URI，让后根据URI调用HandlerMapping获得该Handler配置的所有相关的对象, 返回一个HandlerExecutionChain执行链对象, DispatcherServlet根据Handler选择一个合适的HandlerAdapter，并开始执行拦截器的preHandler方法, 根据Request中的模型数据填充Handler入参，并还是执行Handler(Controller), Handler执行完成后，向HandlerAdapter返回一个ModelAndView对象, HandlerAdapter然后向DispatcherServlet返回ModelAndView对象, 根据返回的ModelAndView选择一个格式的ViewResolver。
- 三级节点通常对应具体细节、API、机制或易错点：将请求数据转换成对象，将对象转换为指定的响应信息, 对请求数据进行转换, 对请求数据进行格式化, 验证数据有效性并将结果存储到BindingResult或Error中。

### 复习追问

- `介绍` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `工作流程` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

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
