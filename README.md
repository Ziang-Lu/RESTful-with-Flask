This repo talks about modern microservice architecture, RESTful architecture & API design, including an example RESTful web service.

# Demo RESTful Architecure & API Design (based on a Flask Application)

## (In the Past) Monolithic Architecture

We have a full, "monolithic", heavy web application, which contains all the functionalities.

-> Scalability problem:

<img src="https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/Monolithic%20Architecture%20Scalability.png?raw=true">

以上图所展示的情况为例:

在一个服务中, 某个component的负载已经达到了90%, 也就是到了不得不对服务能力进行扩容的时候了. 而该服务中的其他components的负载还没有到其处理能力的20%. 由于monolithic服务中的各个component是打包在一起的, 因此通过一个额外的服务实例虽然可以将需要扩容的component的负载降低到45%, 但是也使得其他各个component的利用率更为低下, 造成了资源的浪费.

-> 本质上, 这种不便都是由于monolithic服务中, 一个实例包含了该服务的所有功能所导致的.

<br>

## Service-Oriented-Architecture (SOA) (面向服务架构) for Web Applications

Now, we can <u>split these functionalities to "services".</u> <u>Each "service" corresponds to a "resource" and implements a single functionality, and should be associated with a URI</u>.

In this way, we can have a <u>lightweight web application (maybe even only the front-end)</u> at the center, and it <u>interacts with these services/resources (via the associated URI)</u>. The interaction between the application and these services is done <u>through API (to the associated URI)</u>.

e.g., A traditional e-commerce web application may be splitted into the following services/resources:

<img src="https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/SOA%20Architecture.png?raw=true">

<br>

### (In the past) Remote-Procedure-Call (RPC) (远程过程调用)

RPC风格曾是Web Service的主流, 最初是基于XML-RPC协议, 后来渐渐被SOAP协议取代. RPC风格的web service, 不仅可以用HTTP, 还可以用TCP或其他通信协议.

<u>但RPC风格的web service, 受开发web service所采用的语言的束缚比较大. e.g, 使用`.NET`框架开发的web service, 其客户端通常也需要用`C#`来实现; 而进入移动互联网时代后, RPC风格的web service很难在移动终端使用.</u>

详见: https://blog.igevin.info/posts/restful-architecture-in-general/

***

**具体于Java: Remote-Method-Invokation (RMI) (远程方法调用)**

具体解释和例子, 详见关于design pattern的Proxy Pattern:

https://github.com/Ziang-Lu/Design-Patterns/blob/master/3-Structural%20Patterns/6-Proxy%20Pattern/Proxy%20Pattern.md

*(其实也不是具体于Java, 因为在上面的repo中就有Python的例子, 因此本质上还是回归到了RPC.)*

注意, 至少是在RMI中, 往往有一个`RMI Registry` service的模式:

* Server-side的`RealSubject`需要在`RMI Registry`中register自己, 并指定一个`ObjectId`;
* Client-side根据这个`ObjectId`查找对应的`RealSubject`, 并获得相应的`stub` (本质上是一个"proxy"), 并通过对`stub`进行方法调用来执行`RealSubject`中对应的方法调用.
  * 对client-side来说, 仿佛就是在调用真正的`RealSubject`一样.

***

<br>

## => "Microservice" Architecture

<img src="https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/Microservice%20Architecture.png?raw=true">

=> Microservice架构可以让我们:

* 对负载高的service进行独立的扩容, 大大地提高了资源的利用率

* (在一个monolithic application中, 如果某个功能出现了问题, 导致了系统崩溃, 这将导致整个系统崩溃, 导致这个系统的所有功能都不可用.)

  而在一个microservice系统中, 如果某个功能出现了问题, 只会导致和该功能相关的内容无法访问, 而不会影响系统的其他功能.

  => 提高系统的robustness和availability

***

<br>

## RESTful Architecture & API

RESTful stands for "REpresentational State Transfer".

RESTful API, 也被称作"统一资源接口", 要求<u>用标准的HTTP methods (`GET`, `POST`, `PUT`, `DELETE`等) 来访问services/resources的URI, 操作对应的resource</u>.

=> URI中只包含resource的名称 (可以多层分级), 而通过标准的HTTP method来指明对该resource进行怎样的操作.

***

URI设计原则:

* URI中只包含resource的名称 (可以多层分级), 而通过标准的HTTP method来指明对该resource进行怎样的操作
* URI中使用小写字母和连字符`-`而不是`_`来提高URI可读性
* 不要在末尾使用`/`

***

e.g.,

```bash
# 获取全部articles
GET /blog/get-articles  # Wrong
GET /blog/articles  # Correct

# 添加一篇article
GET /blog/add-article  # Wrong
POST /blog/articles  # Correct

# 删除一篇article
GET /blog/delete-articles?id=1  # Wrong
DELETE /blog/articles/1  # Correct
```

***

### "无状态原则"

***

*由于client-side可能需要与不止一个server进行交互: 如果在server-side保存了有关client-side的任何状态, 那么在一个scale的系统的cluster中, 当client-side与不同server进行交互的时候 就需要在这些servers之间进行关于client-side的状态信息的同步, 大大地增加了系统的复杂度:*

* *如果该状态同步是synchronous的, 那么同时刷新那么多个server上的用户状态将导致对用户request的处理变得异常缓慢*
* *如果该状态同步是ascynchronous的, 那么用户在发送下一个请求时, 其他server将可能由于用户状态的不同步的原因无法正确地处理用户的request*

***

<u>=> 一个request中必须包含server (service)处理该request的全部信息 (其中包括标识该client-side的token), 而在server-side不应保存任何与client-side有关的信息, 即server-side不应保存任何与某个client-side关联的session.</u>

-> In other words, the server cannot store information provided by the client in one request, and use it in another request.

益处:

* 因为<u>server-side和client-side之间, 除了每次**独立地处理request**, 彼此没有任何信息 ("彼此不认识")</u>

  => 使得整个web app的各个component彼此相对独立, 更加灵活

  => 使得整个web app可以更scalable:

  * 不断地增多server数量
  * 增多可以支持的client-side种类

<img src="https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/Scalable%20RESTful.png?raw=true">

**注意!**

API传递的只是resource的"表示", 而不是resource本身, 而<u>`JSON`为最常见的API中resource表示形式</u>.

*=> 需要在request的header中指明: `Content-Type: application/json`*

<br>

事实上, 正是由于serialization/deserialization的便捷, 使得RESTful API可以轻松地使用`JSON`作为数据传输的载体 ("表示")

=> 使得server-side和client-side的开发独立开来, 造成了RESTful架构跨平台的特点

=> 使得RESTful取代RPC成为Web Service的主流

***

<br>

## License

This repo is distributed under the <a href="https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/LICENSE">MIT license</a>.

