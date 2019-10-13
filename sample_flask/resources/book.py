# -*- coding: utf-8 -*-

"""
Book-related RESTful API module.
"""

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from .. import auth, db
from ..models import Book, book_schema, books_schema


class BookList(Resource):
    """
    Resource for a collection of books.
    """
    decorators = [auth.login_required]

    def get(self):
        """
        Returns all the books.
        :return:
        """
        books = Book.query.all()
        return {
            'status': 'success',
            'data': books_schema.dump(books)
        }

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
        db.session.commit()
        return {
            'status': 'success',
            'data': book_schema.dump(book)
        }, 201

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
