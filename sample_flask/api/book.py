# -*- coding: utf-8 -*-

"""
Book-related RESTful API module.
"""

from typing import Any

from flask import Blueprint, request
from marshmallow import EXCLUDE, ValidationError, validate

from .. import db
from ..models import Book, BookSchema

book_bp = Blueprint(name='book_bp', import_name=__name__)

book_schema = BookSchema()
books_schema = BookSchema(many=True)


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
        new_book = book_schema.load(request.get_json(), unknown=EXCLUDE)  # When encountering a unknown fields, simply exclude it
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
    book = Book.query.get(id)
    if not book:
        return {
            'status': 'error',
            'message': 'Book not found'
        }, 404

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
    book = Book.query.get(id)
    if not book:
        return {
            'status': 'error',
            'message': 'Book not found'
        }, 404

    json_data = request.get_json()
    title = json_data.get('title')
    try:
        validate_title_field(title)
    except ValidationError as e:
        return {
            'message': e.messages
        }, 400

    if title:
        book.title = title

    db.session.commit()

    return {
        'status': 'success',
        'data': book_schema.dump(book)
    }, 201


def validate_title_field(title: Any) -> None:
    """
    Helper function to validate the given title field.
    :param title: Any
    :return: None
    """
    try:
        title = str(title)
    except TypeError:
        raise ValidationError('title must be string')

    length_validator = validate.Length(max=Book.TITLE_MAX_LEN)
    length_validator(title)


@book_bp.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id: int):
    """
    Deletes the book with the given ID.
    :param id: int
    :return:
    """
    book = Book.query.get(id)
    if not book:
        return {
            'status': 'error',
            'message': 'Book not found'
        }, 404

    db.session.delete(book)
    db.session.commit()
    return '', 204

