# -*- coding: utf-8 -*-

"""
Todo-related RESTful resources and API module.

Consider using flask.jsonify() to convert some other stuff to JSON
=> Automatically change the Content-Type of the Response to "application/json"
"""

from flask_restful import Resource, abort, reqparse

todos = {
    'todo1': {
        'task': 'Build an API'
    },
    'todo2': {
        'task': '?????'
    },
    'todo3': {
        'task': 'profit!'
    }
}

parser = reqparse.RequestParser()
parser.add_argument('task')


class TodoList(Resource):
    """
    Todo-List resource.
    """

    def get(self):
        """
        Returns all the Todo items.
        :return:
        """
        return todos

    def post(self):
        """
        Creates a new Todo item.
        :return:
        """
        args = parser.parse_args()
        task = {'task': args['task']}
        # Find the next Todo-ID
        todo_id_num = max(
            map(lambda x: int(x.lstrip('todo')), todos.keys())
        ) + 1
        todo_id = f'todo{todo_id_num}'
        todos[todo_id] = task
        return task, 201


def _abort_check(todo_id: str) -> None:
    """
    Helper function to abort if the given Todo-ID doesn't exist.
    :param todo_id: str
    :return: None
    """
    if todo_id not in todos:
        abort(404, message="Todo {todo_id} doesn't exist")


class Todo(Resource):
    """
    Todo item resource.
    """

    def get(self, todo_id: str):
        """
        Returns the Todo item with the specified Todo-ID.
        :param todo_id: str
        :return:
        """
        _abort_check(todo_id)
        return todos[todo_id]

    def put(self, todo_id: str):
        """
        Updates the Todo item with the specified Todo-ID.
        :param todo_id: str
        :return:
        """
        args = parser.parse_args()
        task = {'task': args['task']}
        todos[todo_id] = {
            'task': task
        }
        return task, 201

    def delete(self, todo_id: str):
        """
        Deletes the Todo item with the specified Todo-ID.
        :param todo_id: str
        :return:
        """
        _abort_check(todo_id)
        del todos[todo_id]
        return '', 204
