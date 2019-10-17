# -*- coding: utf-8 -*-

"""
Book-related RESTful API module.
"""

from flask import Blueprint, request
from marshmallow import ValidationError

from .. import auth, db, limiter
from ..models import Book, book_schema, books_schema
from ..utils import RATELIMIT_NORMAL

book_bp = Blueprint(name='book', import_name=__name__)
# Rate-limit all the routes registered on this blueprint.
limiter.limit(RATELIMIT_NORMAL)(book_bp)


@book_bp.before_request
@auth.login_required
def before_request() -> None:
    """
    Before all the request to be handled by "book_bp" blueprint, do login check.
    This is done to avoid all the routes registered on this blueprint having to
    be explicitly decorated with "auth.login_required".
    :return: None
    """
    pass


@book_bp.route('/books')
def get_books():
    """
    Returns all the books.
    :return:
    """
    books = Book.query.all()
    return {
        'status': 'success',
        'data': books_schema.dump(books)
    }


@book_bp.route('/books', methods=['POST'])
def add_book():
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


@book_bp.route('/books/<int:id>')
def get_book_by_id(id: int):
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


@book_bp.route('/books/<int:id>', methods=['PUT'])
def update_book(id: int):
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
    }


@book_bp.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id: int):
    """
    Deletes the book with the given ID.
    :param id: int
    :return:
    """
    book = Book.query.get_or_404(id, description='Book not found')
    db.session.delete(book)
    db.session.commit()
    return '', 204
