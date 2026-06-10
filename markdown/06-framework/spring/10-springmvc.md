# SpringMVC

> 专题：Spring
> 来源：Spring.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 详细说明

### 是什么

- `SpringMVC` 是 `Spring` 体系中的一个具体知识点，建议先明确它解决的问题、参与的核心对象以及在整体链路中的位置。
- 如果原脑图只记录了标题，复习时应补齐定义、适用场景、关键流程和边界条件，避免面试时只能说概念名。

### 为什么重要

- 这类知识点通常会连接到源码机制、工程实践或线上故障，面试官更关注你能否把概念落到实际问题。
- 准备时不要只背结论，要能说明它和相邻知识点的区别、取舍以及常见误用。

### 实践关注

- 整理至少一个业务或框架中的使用场景。
- 补充常见坑点、异常表现、排查手段和优化方向。
- 如果涉及配置或参数，记录默认值、调优依据和风险边界。

### 面试表达

- 回答 `SpringMVC` 时，可以按“定义 -> 原理/流程 -> 使用场景 -> 常见问题 -> 项目经验”的顺序展开。
- 如果不确定细节，优先讲清边界和排查思路，不要把不同组件或不同版本的行为混在一起。

### 复习检查

- 能用自己的话解释 `SpringMVC`，而不是只复述标题。
- 能说出至少一个生产场景、一个常见坑点和一个排查方向。

## 脑图解读

- 本节脑图围绕 `SpringMVC` 展开，属于 `Spring` 的复习范围。
- 建议优先掌握：使用, ContextLoaderListener。
- 二级节点提示了主要拆分角度：contextConfigLocation(applicationContext.xml), DispatcherServlet, Spring-servlet.xml, ServletContextListener, servlet容器生命周期, 初始化, 逻辑处理。
- 三级节点通常对应具体细节、API、机制或易错点：initWebApplictionContext, 1、初始化阶段, 2、运行阶段, 3、销毁阶段, 1、封装及验证初始化参数(ServletCOnfigPropertyValues), 2、当前Servlet实例转化为BeanWrapper实例(PropertyAccessorFactory.forBeanPropertyAccess), 3、注册相对于Resource的属性编辑器, 4、属性注入, 5、servletBean初始化(initServletBean), 1、保存当前线程的LocaleContext和RequestAttribute属性。

### 复习追问

- `使用` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？
- `ContextLoaderListener` 解决什么问题？核心机制是什么？有什么常见坑或替代方案？

## 脑图内容

## SpringMVC

### 使用

#### contextConfigLocation(applicationContext.xml)

#### DispatcherServlet

#### Spring-servlet.xml

### ContextLoaderListener

#### ServletContextListener

- initWebApplictionContext
  - 1、WebApplicationContext存在性验证，仅允许声明一次
  - 2、创建WebApplicationContext(createWebApplicationContext)
  - 3、将实例记录在servletContext中
  - 4、映射当前的类加载器与创建的实力到全局变量currentContextPerThread中

### DispatcherServlet

#### servlet容器生命周期

- 1、初始化阶段
  - servlet容器加载servlet类
  - servlet容器创建一个ServletConfig对象
  - servlet容器创建一个servlet对象
  - servlet容器调用servlet对象的init方法进行初始化

- 2、运行阶段
  - servlert收到请求后，会创建servletRequest和servletResponse对象
  - servletRequest和servletResponse作为参数调用service方法
  - 销毁servlertRequest和servletResponse对象

- 3、销毁阶段
  - servlet容器调用servlet对象的destrory方法，再销毁servlert对象
  - 同时销毁关联的servletConfig对象

#### 初始化

- 1、封装及验证初始化参数(ServletCOnfigPropertyValues)

- 2、当前Servlet实例转化为BeanWrapper实例(PropertyAccessorFactory.forBeanPropertyAccess)

- 3、注册相对于Resource的属性编辑器

- 4、属性注入

- 5、servletBean初始化(initServletBean)
  - initWebApplicationContext
    - 1、寻找或创建对应的WebApplicationContext实例
    - 2、通过contextAttribute进行初始化
    - 3、重新创建WebApplicationContext实例
    - 4、刷新(initStrategies)
      - 1、初始化MultipartResolver
        - 处理文件上传
      - 2、初始化LocaleResolver
        - 处理国际化配置
          - URL
          - Session
          - Cookie
      - 3、初始化ThemeResolver
        - 通过主题控制页面风格
          - Source(资源)
          - Resolver(解析)
            - Fixed
            - Cookie
            - Session
            - Abstract
          - Interceptor(拦截器)-改变主题
      - 4、初始化HandlerMappings
      - 5、初始化HandlerAdapters
        - HttpRequestHandleradapter
        - SimpleControllerHandlerAdapter
        - AnnotationMethodHandlerAdapter
      - 6、初始化HandlerExceptionResolvers
      - 7、初始化RequestToViewNameTranslator
      - 8、初始化ViewResolvers
      - 9、初始化FlashMapManager
  - initFrameworkServlet(设计为子类覆盖)

#### 逻辑处理

- 1、保存当前线程的LocaleContext和RequestAttribute属性

- 2、根据当前request创建对应的LocalContext和RequestAttributes并绑定到当前线程

- 3、委托给doService方法进一步处理
  - doDispatch
    - 1、MultipartContet类型的request处理
    - 2、根据request信息寻找对应的Handler
    - 3、没找到对应Handler的错误处理
    - 4、根据当前Handler寻找对应的HandlerAdapter
    - 5、缓存处理
    - 6、HandlerInterceptor处理
    - 7、逻辑处理
    - 8、异常视图处理
    - 9、根据视图跳转页面

- 4、请求处理结束后恢复线程到原始状态

- 5、请求处理结束后无论成功与否都发布事件通知
