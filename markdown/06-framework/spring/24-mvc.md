# MVC

> 专题：Spring
> 来源：面试内容汇总/Spring.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## MVC

### 核心组件

#### DispatcherServlet

#### Handlermapping

#### HandlerAdapter

#### Handler

#### ViewResolver

### 处理流程

#### 客户端（浏览器）发送请求， DispatcherServlet拦截请求。

#### DispatcherServlet 根据请求信息调用 HandlerMapping 。HandlerMapping 根据 uri 去匹配查找能处理的 Handler（也就是我们平常说的 Controller 控制器） ，并会将请求涉及到的拦截器和 Handler 一起封装。

#### DispatcherServlet 调用 HandlerAdapter适配执行 Handler

#### Handler 完成对用户请求的处理后，会返回一个 ModelAndView 对象给DispatcherServlet，ModelAndView 顾名思义，包含了数据模型以及相应的视图的信息。Model 是返回的数据对象，View 是个逻辑上的 View

#### ViewResolver 会根据逻辑 View 查找实际的 View。

#### DispaterServlet 把返回的 Model 传给 View（视图渲染）。

#### 把 View 返回给请求者（浏览器）

### @ControllerAdvice

#### @ExceptionHandler

- 统一处理异常
