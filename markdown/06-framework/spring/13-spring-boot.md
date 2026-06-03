# Spring Boot

> 专题：Spring
> 来源：Spring.xmind

## 补充与实践

- 补充：建议从问题背景、核心原理、适用场景、边界条件和生产案例五个维度整理该知识点。
- 实践：学习时结合监控指标、日志、配置参数和故障复盘，避免只停留在概念记忆。

## 脑图内容

## Spring Boot

### Starter

#### ComponentScan

#### META_INF/spring.factories

### SpringBootApplication

#### SpringContext创建(createApplicationContext)

#### bean加载(prepareContext)

#### Spring扩展属性的加载(refreshContext)

#### afterRefresh

### @EnableAutoConfiguration

#### EnableAutoConfigurationImportSelector

- isEnabled

### spring.factories加载

#### AutoConfigurationImportSelector.selectImports

- getCandidateConfigurations

#### ConfigurationClassPostProcessor

#### ConfigurationClassParser.processImports

### Componentscan的切入点

#### ClassPathBeanDefinitionScanner

### Conditional(@ConditionalOnProperty)

#### OnPropertyCondition.getMatchOutcome

### 属性自动化配置实现(@Value)

#### DefaultListableBeanFactory.resolveEmbeddedValue

- StringValueResolver
  - 1、初始化MutablePropertySources
  - 2、初始化PropertySourcesPropertyResolver
  - 3、初始化StringValueResolver
  - 4、StringValueResolver注册到ConfigurableListableBeanFactory

### Tomcat启动

#### EmbeddedWebApplicationContext.onRefresh

- createEmbeddedServletContainer
  - @ConditionalOnClass
