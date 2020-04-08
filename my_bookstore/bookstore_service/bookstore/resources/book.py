# -*- coding: utf-8 -*-

"""
Book-related RESTful API module.
"""

from flask import request
from flask_restful import Resource
from flask_sqlalchemy import BaseQuery
from marshmallow import ValidationError

from .. import auth, db
from ..models import Author, Book, book_schema, books_schema
from ..utils import paginate


class BookList(Resource):
    """
    Resource for a collection of books.
    """
    decorators = [auth.login_required]

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
            new_book_data = book_schema.load(request.get_json())
        except ValidationError as e:
            return {
                'message': e.messages
            }, 400

        author_name = new_book_data['author_name']
        author = Author.query.filter_by(name=author_name)
        if not author:
            # Create a new author
            new_author = Author(name=author_name)
            # In order to get the assigned ID of the new author, we need to
            # commit the transaction.
            db.session.add(new_author)
            db.session.commit()

        new_book_data['author_id'] = author.id
        new_book = Book(**new_book_data)
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
            book_data_updates = book_schema.load(request.get_json())
        except ValidationError as e:
            return {
                'message': e.messages
            }

        if 'title' in book_data_updates:
            book.title = book_data_updates['title']
        if 'description' in book_data_updates:
            book.description = book_data_updates['description']
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
