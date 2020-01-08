# -*- coding: utf-8 -*-

"""
Author-related RESTful API module.

In the naive implementation, we used two "GET" methods to access "Author"
resource, i.e., in a collection view and in a single view.
But here, we need to split the same "Author" resource into two resources, i.e.,
"AuthorList" for the collection view and "AuthorItem" for the single view.
"""

from flask import request
from flask_restful import Resource
from flask_sqlalchemy import BaseQuery
from marshmallow import ValidationError

from .. import auth, db, limiter
from ..models import Author, author_schema, authors_schema
from ..utils import RATELIMIT_NORMAL, paginate


class AuthorList(Resource):
    """
    Resource for a collection of authors.
    """
    decorators = [
        auth.login_required,
        limiter.limit(RATELIMIT_NORMAL, per_method=True)
    ]

    @paginate(authors_schema)
    def get(self) -> BaseQuery:
        """
        Returns all the authors in the specified page.
        :return: BaseQuery
        """
        # For pagination, we need to return a query that hasn't run yet.
        return Author.query

    def post(self):
        """
        Adds a new author.
        :return:
        """
        try:
            new_author = author_schema.load(request.get_json())
        except ValidationError as e:
            return {
                'message': e.messages
            }, 400

        db.session.add(new_author)
        db.session.commit()
        return {
            'status': 'success',
            'data': author_schema.dump(new_author)
        }, 201


class AuthorItem(Resource):
    """
    Resource for a single author.
    """
    decorators = [auth.login_required]

    def get(self, id: int):
        """
        Returns the author with the given ID.
        :param id: int
        :return:
        """
        author = Author.query.get_or_404(id, description='Author not found')
        return {
            'status': 'success',
            'data': author_schema.dump(author)
        }

    def put(self, id: int):
        """
        Updates the author with the given ID.
        :param id: int
        :return:
        """
        author = Author.query.get_or_404(id, description='Author not found')

        try:
            updated_author = author_schema.load(
                request.get_json(), partial=True
            )
        except ValidationError as e:
            return {
                'message': e.messages
            }, 400

        if updated_author.name:
            author.name = updated_author.name
        if updated_author.email:
            author.email = updated_author.email
        db.session.commit()
        return {
            'status': 'success',
            'data': author_schema.dump(author)
        }

    def delete(self, id: int):
        """
        Deletes the author with the given ID.
        :param id: int
        :return:
        """
        author = Author.query.get_or_404(id, description='Author not found')
        db.session.delete(author)
        db.session.commit()
        return '', 204
