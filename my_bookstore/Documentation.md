# Bookstore Web Service Documentation

* Base URL: `/bookstore`

  *Note that `/bookstore` is the application URL prefix, which is set up using `app.config['APPLICATION_ROOT']`*

* **API Entrance**: `/bookstore/` or `/bookstore/entrance`

  This returns some URLs that you can request to operate on the resources.

* **Defined Resources**:

  * `AuthorList`

    Route: `bookstore/authors`

    | Method | Description             | Request Form Schema                          | Response Status Code                                         |
    | ------ | ----------------------- | -------------------------------------------- | ------------------------------------------------------------ |
    | GET    | Returns all the authors |                                              | 200 on success                                               |
    | POST   | Creates a new author    | `name`: string<br>`email`: string [optional] | 201 on successful creation, 200 on found existing author, 400 on invalid data provided |

  * `AuthorItem`

    Route: `bookstore/authors/<int:id>`
  
    | Method | Description                              | Request Form Schema                                     | Reponse Status Code                                          |
    | ------ | ---------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------ |
    | GET    | Returns the author with the specified ID |                                                         | 200 on success, 404 on author not found                      |
  | PUT    | Updates the author with the specified ID | `name`: string [optional]<br>`email`: string [optional] | 200 on success, 404 on author not found, 400 on invalid data provided |
  | DELETE | Deletes the author with the specified ID |                                                         | 204 on success, 404 on author not found                      |
  
  * `BookList` & `BookItem`

    Similar to `Author`, but with request data schema as follows:
  
    | Field name    | Type   | Required? |
    | ------------- | ------ | --------- |
    | `title`       | string | True      |
    | `description` | string | False     |

<br>

### `Flask` Implementation Details

* Basically, there are two ways to implement this web service:

  1. Naive implementation with view functions

  2. Implementation with extension

     * `Flask-RESTful` for defining resources

     * `Flask_RESTPlus` for defining resources

       Basically, this is very similar to `Flask-RESTful`, since originally this project was forked from `Flask-RESTful`. The biggest advantage over `Flask_RESTful` is the auto-generated documentation using `Swagger` UI.

       *(In my implementation, I simply used `Flask-RESTful`. For the usage of `Flask-RESTPlus` and `Swagger` UI, check out their documentation: https://flask-restplus.readthedocs.io/en/stable/)*

* But either way can use `Marshmallow`/`Flask-Marshmallow` for schema definition & deserialization (including validation) / serialization.

* This web service is backed by `PostgreSQL` database. And thus `Flask-SQLAlchemy` module is used for ORM-related tasks.



### Authentication & Authorization

We <u>need a authentication mechanism</u>, so that the web service is only open to those registered users.

However, the <u>"stateless principle" of RESTful architecture requires that the clients need to provide credentials in every request they send</u>.

According to the author of `Flask-HTTPAuth` in his article https://blog.miguelgrinberg.com/post/restful-authentication-with-flask:

* Maintain a `users` table of registered users

  * For this, we define `User` data model and `UserSchema` for serialization/deserialization.
    * POST `/bookstore/users` with `username:password` authentication credentials to create a new user

* The client needs to provide credentials in every request they send. There are two ways to do the authentication:

  1. Provide `username:password` combination in every request

  2. First send `username:password` combination to the server, and get back a token

     * GET `/bookstore/token` with `username:password` or `token:<any-password>` authentication credentials to get a token for that user

     This token is only valid for some time, i.e., has an expiration time. During this period of time, the client can simply provide this token as the credential. In this way, the authentication mechanism becomes much simpler, and even safer since the token is only valid for some time.

     *Tricky side effect:*

     *In this mechanism, we can simply provide a valid token to get a new token, and so on, ... Any problem with this?*

Thus, <u>we separate a Flask-based `auth_service` out from `bookstore_service` as a separate web service, which is responsible for user authentication, including user registration, user authentication, and token generation</u>.

***

* *Why not go one step further, and separate `author_service` or `book_service` out?*

  *Well... we could've done that, but it requires a little bit more effort.*

  *This is because`Author` and `Book` has a tightly-coupled 1-to-many relationship, so separating them into different services leads to great inconvenience:*

  -> *A `Book` object has an attribute of `author`, which refers to an `Author` object. Imagine we try to separate them out into different services, then in order to pass the representations of `Author` and `Book` objects, we have to repeatedly define `Author`, `Book`, `AuthorSchema` and `BookSchema` in both `author_service` and `book_service`, which is redundant and violates the DIY principle.*

***

For this entire web service, this is the illustrative architecture:

<img src="https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/my_bookstore/Bookstore%20Web%20Service%20RESTful%20Architecture%20&%20API.png?raw=true">

***



### Additional Features

* Pagination for collection result

  All routes returning a collection of resources actually return paginated results, with information about pagination metadata as well as the URLs for the previous page, next page, first page, last page, etc.

<br>

### Deployment

The deployment of this web services follows the Docker-way, i.e., with

* **Linux Server**
* **Web Server (in `Docker` container) [`nginx`]**
* **Python Web App WSGI Server [`Gunicorn`]**

Check out https://github.com/Ziang-Lu/Flask-Blog/blob/master/Deployment%20Options.md#2-linux-server--web-server-in-docker-container--python-web-app-wsgi-server-in-docker-container

***

Thus, this web service can be deployed as follows:

<img src="https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/my_bookstore/Bookstore%20Web%20Service%20Deployment.png?raw=true">

***

