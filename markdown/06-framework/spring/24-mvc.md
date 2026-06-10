# MVC

> 专题：Spring
> 来源：面试内容汇总/Spring.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 是什么

- `MVC` 是 `Spring` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `MVC` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `MVC`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `MVC` 展开，属于 `Spring` 的复习范围。
- 建议优先掌握：核心组件, 处理流程, @ControllerAdvice。
- 二级节点提示了主要拆分角度：DispatcherServlet, Handlermapping, HandlerAdapter, Handler, ViewResolver, 客户端（浏览器）发送请求， DispatcherServlet拦截请求。, DispatcherServlet 根据请求信息调用 HandlerMapping 。HandlerMapping 根据 uri 去匹配查找能处理的 Handler（也就是我们平常说的 Controller 控制器） ，并会将请求涉及到的拦截器和 Handler 一起封装。, DispatcherServlet 调用 HandlerAdapter适配执行 Handler, Handler 完成对用户请求的处理后，会返回一个 ModelAndView 对象给DispatcherServlet，ModelAndView 顾名思义，包含了数据模型以及相应的视图的信息。Model 是返回的数据对象，View 是个逻辑上的 View, ViewResolver 会根据逻辑 View 查找实际的 View。。
- 三级节点通常对应具体细节、API、机制或易错点：统一处理异常。

### 复习追问

- `核心组件` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `处理流程` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `@ControllerAdvice` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

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
