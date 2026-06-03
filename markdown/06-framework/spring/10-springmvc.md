# SpringMVC

> 专题：Spring
> 来源：Spring.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

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
