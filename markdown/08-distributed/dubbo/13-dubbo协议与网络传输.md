# Dubbo协议与网络传输

> 专题：Dubbo
> 来源：Dubbo.xmind

## 补充与实践

- 补充：Dubbo 3 支持 Triple 协议和应用级服务发现，适合云原生与多语言互通场景。
- 实践：接口超时应小于调用方整体超时预算，重试只适合幂等读或可重复操作。
- 排障：RPC 慢调用要同时看客户端等待、网络耗时、序列化、服务端线程池和业务执行。

## 脑图内容

## Dubbo协议与网络传输

### Dubbo协议

#### 结构组成

- header
  - magic high（1btye）
    - 0xda
  - magic low（1byte）
    - oxbb
  - request flag and serialization id(1byte)
    - 高四位-请求类型
      - FLAG_REQUEST
      - FLAG_TWOWAY
      - FLAG_EVENT
    - 低四位-序列化方式
  - response status（1byte）
    - 响应结果码，仅在响应报文里才设置
  - request id（8byte）
    - 请求ID
  - body length（4byte）
    - body内容大小

- body

#### 消费方编码

- NettyCodecAdapter

- DubboCodec

#### 提供者解码
