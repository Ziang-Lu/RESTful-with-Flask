# Demo RESTful Architecure & API Design (based on a Flask Application)

## RESTful Architecture for Web Applications

***

Traditionally, we have a full, heavy web application, which contains all the functionalities.

***

Now, we can <u>split these functionalities to "services".</u> <u>Each "service" corresponds to a "resource" and implements a single functionality, and should be associated with a URI</u>.

In this way, we can have a <u>lightweight web application</u> at the center, and it <u>interacts with these services/resources (via the associated URI)</u>. The interaction between the web application and these services is done <u>through API (to the associated URI)</u>.

=> This kind of architecture is called <u>*RESTful*, which stands for "REpresentational State Transfer", architecture</u>.

e.g., A traditional e-commerce web application may be splitted into the following services/resources:

<img src="https://github.com/Ziang-Lu/Flask-Restful/blob/master/RESTful%20Architecture.png?raw=true">

<br>

## RESTful API

RESTful API, 也被称作"统一资源接口", 要求<u>用标准的HTTP methods (`GET`, `POST`, `PUT`, `DELETE`等) 来访问services/resources的URI</u>.

***

**注意!**

API传递的只是resource的"表示", 而不是resource本身, 而这种表示可以有很多种形式, 常见的有`json`和 `xml`等, 其中<u>`json`为最常见的API中resource表示形式</u>

***

<br>

## Documentation of this RESTful API

There are two resources on this Flask application:

* `TodoList`

  URI/Route: `/todos`

  Supported methods:

  | Method | Description                | Response JSON                              | Response Status Code |
  | ------ | -------------------------- | ------------------------------------------ | -------------------- |
  | GET    | Returns all the Todo items | `{'todo1': {'task': 'Build an API'}, ...}` | 200 on success       |
  | POST   | Creates a new Todo item    | `{'task': {'posted_data'}}`                | 201 on success       |

* `Todo`

  URI/Route: `/todos/<string:todo_id>`

  Supported methods:

  | Method | Description                                      | Response JSON                      | Response Status |
  | ------ | ------------------------------------------------ | ---------------------------------- | --------------- |
  | GET    | Returns the Todo item with the specified Todo-ID | `{'todo3': {'task': 'profit!'}}`   | 200 on success  |
  | PUT    | Updates the Todo item with the specified Todo-ID | `{'task': {'posted_update_data'}}` | 201 on success  |
  | DELETE | Deletes the Todo item with the specified Todo-ID | `''`                               | 204 on success  |

