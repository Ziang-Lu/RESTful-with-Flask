# Demo RESTful Architecure & API Design (based on a Flask Application)

## RESTful Architecture for Web Applications

***

In the past:

-> We have a full, heavy web application, which contains all the functionalities.

***

Now, we can <u>split these functionalities to "services".</u> <u>Each "service" corresponds to a "resource" and implements a single functionality, and should be associated with a URI</u>.

In this way, we can have a <u>lightweight web application (maybe even only the front-end)</u> at the center, and it <u>interacts with these services/resources (via the associated URI)</u>. The interaction between the application and these services is done <u>through API (to the associated URI)</u>.

=> This kind of architecture is called <u>*RESTful*, which stands for "REpresentational State Transfer", architecture</u>.

e.g., A traditional e-commerce web application may be splitted into the following services/resources:

<img src="https://github.com/Ziang-Lu/Flask-Restful/blob/master/RESTful%20Architecture.png?raw=true">

<br>

## RESTful API

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

<u>一个request中必须包含server (service)处理该request的全部信息 (其中包括标识该client-side的token), 而在server-side不应保存任何与client-side有关的信息, 即server-side不应保存任何与某个client-side关联的session.</u>

In other words, the server cannot store information provided by the client in one request, and use it in another request.

益处:

* 因为<u>server-side和client-side之间, 除了每次**独立地处理request**, 彼此没有任何信息 ("彼此不认识")</u>

  => 使得整个web application的各个component彼此相对独立, 更加灵活

  => 使得整个web application可以更scalable:

  * 不断地增多server数量
  * 增多可以支持的client-side种类

<img src="https://github.com/Ziang-Lu/Flask-Restful/blob/master/Scalable%20RESTful.png?raw=true">

***

**注意!**

API传递的只是resource的"表示", 而不是resource本身, 而<u>`json`为最常见的API中resource表示形式</u>.

*=> 需要在request的header中指明: `Content-Type: application/json`*

***

<br>

## Documentation of this RESTful API

There are two resources on this Flask application:

* `Author`

  Route: `/authors`

  | Method | Description              | Response Status Code                            |
  | ------ | ------------------------ | ----------------------------------------------- |
  | GET    | Returns all the products | 200 on success                                  |
  | POST   | Creates a new product    | 201 on success, 400 on not enough data provided |

  Route: `/authors/<id>`

  | Method | Description                              | Reponse Status Code                                          |
  | ------ | ---------------------------------------- | ------------------------------------------------------------ |
  | GET    | Returns the author with the specified ID | 200 on success, 404 on product not found                     |
  | PUT    | Updates the author with the specified ID | 200 on success, 400 on invalid data provided, 404 on product not found |
  | DELETE | Deletes the author with the specified ID | 204 on success, 404 on product not found                     |

* `Book`

  Similar to `Author`

***

**Implementation Detail**

Basically, there are two ways to implement this RESTful API:

1. Naive implementation + `marshmallow`/`flask_marshmallow` for schema definition & deserialization (including validation) / serialization

2. Implementation with extension

   * `flask_restful`

     `flask_restful`  for defining resources + `flask_restful.reqparse`/`flask_restful.marshal()` for request parsing (validation & deserialization) and serialization

***

<br>

**Note on web service security**

For this web service that we wrote, it is <u>open to anyone</u>, which is <u>very unsafe</u>.

=> Thus, we <u>need a authentication mechanism</u>.

However, the <u>"stateless principle" of RESTful architecture requires that the clients needs to provide credentials in every request they send</u>.

=> Check out https://github.com/miguelgrinberg/flask-httpauth for a simple authentication system

* Pagination

