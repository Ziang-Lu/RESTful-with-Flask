# Demo RESTful Architecure & API Design (based on a Flask Application)

## Service-Oriented-Architecture (SOA) (面向服务架构) for Web Applications

***

In the past:

-> We have a full, heavy web application, which contains all the functionalities.

***

Now, we can <u>split these functionalities to "services".</u> <u>Each "service" corresponds to a "resource" and implements a single functionality, and should be associated with a URI</u>.

In this way, we can have a <u>lightweight web application (maybe even only the front-end)</u> at the center, and it <u>interacts with these services/resources (via the associated URI)</u>. The interaction between the application and these services is done <u>through API (to the associated URI)</u>.

e.g., A traditional e-commerce web application may be splitted into the following services/resources:

<img src="https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/RESTful%20Architecture.png?raw=true">

***

### "Microservice" Architecture

<img src="https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/Microservice%20Architecture.png?raw=true">

***

<br>

### (In the past) Remote-Procedure-Call (RPC) (远程过程调用)

RPC风格曾是Web Service的主流, 最初是基于XML-RPC协议, 后来渐渐被SOAP协议取代. RPC风格的web service, 不仅可以用HTTP, 还可以用TCP或其他通信协议.

<u>但RPC风格的web service, 受开发web service所采用的语言的束缚比较大. e.g, 使用`.NET`框架开发的web service, 其客户端通常也需要用`C#`来实现; 而进入移动互联网时代后, RPC风格的web service很难在移动终端使用.</u>

详见: https://blog.igevin.info/posts/restful-architecture-in-general/

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

**"无状态原则"**

*由于client-side可能需要与不止一个server进行交互: 如果在server-side保存了有关client-side的任何状态, 那么当client-side与不同server进行交互的时候 就需要在这些servers之间进行关于client-side的状态信息的同步, 大大地增加了系统的复杂度.*

<u>=> 一个request中必须包含server (service)处理该request的全部信息 (其中包括标识该client-side的token), 而在server-side不应保存任何与client-side有关的信息, 即server-side不应保存任何与某个client-side关联的session.</u>

-> In other words, the server cannot store information provided by the client in one request, and use it in another request.

益处:

* 因为<u>server-side和client-side之间, 除了每次**独立地处理request**, 彼此没有任何信息 ("彼此不认识")</u>

  => 使得整个web app的各个component彼此相对独立, 更加灵活

  => 使得整个web app可以更scalable:

  * 不断地增多server数量
  * 增多可以支持的client-side种类

<img src="https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/Scalable%20RESTful.png?raw=true">

***

**注意!**

API传递的只是resource的"表示", 而不是resource本身, 而<u>`JSON`为最常见的API中resource表示形式</u>.

*=> 需要在request的header中指明: `Content-Type: application/json`*

<br>

事实上, 正是由于serialization/deserialization的便捷, 使得RESTful API可以轻松地使用`JSON`作为数据传输的载体 ("表示")

=> 使得server-side和client-side的开发独立开来, 造成了RESTful架构跨平台的特点

=> 使得RESTful取代RPC成为Web Service的主流

***

<br>

## Documentation of Web Service RESTful API

In this project, we implemented a <u>"bookstore" web service in RESTful-architecture, which has `author`s and `book`s associated with them as the two resources</u>, based on a simple `Flask` application.

* Base URL: `/bookstore/v1`

  *Note that `/bookstore` is the application URL prefix, which is set up using `app.config['APPLICATION_ROOT']` plus proper WSGI setting, while`/v1` is hard-coded for versioning the API.*

* `Author`

  Route: `/authors`

  | Method | Description              | Request Data Schema                          | Response Status Code                            |
  | ------ | ------------------------ | -------------------------------------------- | ----------------------------------------------- |
  | GET    | Returns all the products |                                              | 200 on success                                  |
  | POST   | Creates a new product    | `name`: string<br>`email`: string [optional] | 201 on success, 400 on not enough data provided |

  Route: `/authors/<id>`

  | Method | Description                              | Request Data Schema                                     | Reponse Status Code                                          |
  | ------ | ---------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------ |
  | GET    | Returns the author with the specified ID |                                                         | 200 on success, 404 on product not found                     |
  | PUT    | Updates the author with the specified ID | `name`: string [optional]<br>`email`: string [optional] | 200 on success, 400 on invalid data provided, 404 on product not found |
  | DELETE | Deletes the author with the specified ID |                                                         | 204 on success, 404 on product not found                     |

* `Book`

  Similar to `Author`, but with request data schema as follows:
  
  | Field name    | Type   | Required ? |
  | ------------- | ------ | ---------- |
  | `title`       | string | True       |
  | `description` | string | False      |



### `Flask` Implementation Detail

* Basically, there are two ways to implement this web service:

  1. Naive implementation with view functions

  2. Implementation with extension

     * `Flask-RESTful` for defining resources

     * `Flask_RESTPlus` for defining resources

       Basically, this is very similar to `Flask-RESTful`, since originaly this project was forked from `Flask-RESTful`. The biggest advantage over `Flask_RESTPlus` is the auto-generated documentation using `Swagger` UI.

       *(In my implementation, I simply used `Flask-RESTful`. For the usage of `Flask-RESTPlus` and `Swagger` UI, check out their documentation: https://flask-restplus.readthedocs.io/en/stable/)*

* But either way can use `Marshmallow`/`Flask_Marshmallow` for schema definition & deserialization (including validation) / serialization.
* This web service is backed by `PostgreSQL` database.



### Note on web service security

For this web service that we wrote, it is <u>open to anyone</u>, which is <u>very unsafe</u>.

=> Thus, we <u>need a authentication mechanism</u>, so that the web service is only open to those registered users.

However, the <u>"stateless principle" of RESTful architecture requires that the clients needs to provide credentials in every request they send</u>.

According to the author of `flask-httpauth` in his article https://blog.miguelgrinberg.com/post/restful-authentication-with-flask, there are two ways to do the authentication:

* Maintain a `users` table of registered users

  * For this, we defined `User` data model and `UserSchema` for serialization/deserialization.
    * POST `/users` with `username:password` authentication credentials creates a new user

* The client needs to provide credentials in every request they send.

  1. Provide username-password combination in every request

  2. Send username-password to the server, and get back a token.

     * GET `/token` with `username:password` or `token:<any-password>` authentication credentials to get a token for that user

     This token is only valid for some time, i.e., has an expiration time. During this period of time, the user can simply provide this token as the credential.
     
     In this way, the authentication mechanism becomes much simpler, and even safer since the token is only valid for some time.



### Additional Features

* Rate limiting

  All routes are protected by rate limiting, implemented with `Flask-Limiter` and `Redis`.

* Pagination for collection result

  All routes returning a collection of resources actually returns paginated results, with information about pagination metadata as well as the URLs for the previous page, next page, first page, last page, etc.



### Deployment

The deployment of this web services follows the Docker-way, i.e., with **Linux Server** + **Web Server (in `Docker` container) [`nginx`]** + **Python Web App WSGI Server [`Gunicorn`]**

Check out https://github.com/Ziang-Lu/Flask-Blog/blob/master/Deployment%20Options.md#2-linux-server--web-server-in-docker-container--python-web-app-wsgi-server-in-docker-container

***

For a modern web application described at the very beginning, it can be deployed in `Docker` containers as such:

<img src="https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/Dockerized%20Web%20Services.png?raw=true">

***

<br>

## License

This repo is distributed under the <a href="https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/LICENSE">MIT license</a>.

