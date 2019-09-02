# Demo RESTful API Design (based on Flask Application)

## About RESTful API Design

### In the Past

Traditionally, we have a full, heavy web application, which contains all the functionalities.

<br>

### Now

Now we can split these functionalities to micro-services ("resources"), each implementing a single functionality. In this way, we can have a <u>lightweight web application</u> at the center, and it <u>interacts with these micro-services</u>. The <u>interaction</u> between the web application and these micro-services is done <u>through API</u>.

=> <u>If this architecture and the API design follow some kind of standard, it's called a "RESTful architecture", and the API design is called RESTful API</u>.

*Note: For RESTful API, the expected response content is JSON.*

<br>

## Documentation of this RESTful API

There are two resources on this Flask application:

* `TodoList`

  Route: `/todos`

  Supported methods:

  | Method | Description                | Response JSON                              | Response Status Code |
  | ------ | -------------------------- | ------------------------------------------ | -------------------- |
  | GET    | Returns all the Todo items | `{'todo1': {'task': 'Build an API'}, ...}` | 200 on success       |
  | POST   | Creates a new Todo item    | `{'task': {'posted_data'}}`                | 201 on success       |

* `Todo`

  Route: `/todos/<string:todo_id>`

  Supported methods:

  | Method | Description                                      | Response JSON                      | Response Status |
  | ------ | ------------------------------------------------ | ---------------------------------- | --------------- |
  | GET    | Returns the Todo item with the specified Todo-ID | `{'todo3': {'task': 'profit!'}}`   | 200 on success  |
  | PUT    | Updates the Todo item with the specified Todo-ID | `{'task': {'posted_update_data'}}` | 201 on success  |
  | DELETE | Deletes the Todo item with the specified Todo-ID | `''`                               | 204 on success  |

