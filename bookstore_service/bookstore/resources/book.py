# -*- coding: utf-8 -*-

"""
Book-related RESTful API module.
"""

from flask import request
from flask_restful import Resource
from flask_sqlalchemy import BaseQuery
from marshmallow import ValidationError

from .. import auth, db, limiter
from ..models import Book, book_schema, books_schema
from ..utils import RATELIMIT_NORMAL, paginate


class BookList(Resource):
    """
    Resource for a collection of books.
    """
    decorators = [
        auth.login_required,
        limiter.limit(RATELIMIT_NORMAL, per_method=True)
    ]

    @paginate(books_schema)
    def get(self) -> BaseQuery:
        """
        Returns all the authors.
        :return: BaseQuery
        """
        # For pagination, we need to return a query that hasn't run yet.
        return Book.query

    def post(self):
        """
        Adds a new book.
        :return:
        """
        try:
            new_book = book_schema.load(request.get_json())
        except ValidationError as e:
            return {
                'message': e.messages
            }, 400
        db.session.add(new_book)
        db.session.commit()
        return {
            'status': 'success',
            'data': book_schema.dump(new_book)
        }


class BookItem(Resource):
    """
    Resource for a single book.
    """
    decorators = [auth.login_required]

    def get(self, id: int):
        """
        Returns the book with the given ID.
        :param id: int
        :return:
        """
        book = Book.query.get_or_404(id, description='Book not found')
        return {
            'status': 'success',
            'data': book_schema.dump(book)
        }

    def put(self, id: int):
        """
        Updates the book with the given ID.
        :param id: int
        :return:
        """
        book = Book.query.get_or_404(id, description='Book not found')

        try:
            updated_book = book_schema.load(request.get_json())
        except ValidationError as e:
            return {
                'message': e.messages
            }

        if updated_book.title:
            book.title = updated_book.title
        if updated_book.author:
            book.author = updated_book.author
        if updated_book.description:
            book.description = updated_book.description
        db.session.commit()
        return {
            'status': 'success',
            'data': book_schema.dump(book)
        }

    def delete(self, id: int):
        """
        Deletes the book with the given ID.
        :param id: int
        :return:
        """
        book = Book.query.get_or_404(id, description='Book not found')
        db.session.delete(book)
        db.session.commit()
        return '', 204
