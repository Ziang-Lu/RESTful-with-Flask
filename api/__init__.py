from flask_restful import Api

from . import todo
from app import app

api = Api(app)

api.add_resource(todo.TodoList, '/todos')
api.add_resource(todo.Todo, '/todos/<string:todo_id>')
