# -*- coding: utf-8 -*-

"""
Author-related RESTful API module.
"""

from typing import Any

from flask import Blueprint, request
from marshmallow import ValidationError

from .. import db
from ..models import Author, author_schema, authors_schema

author_bp = Blueprint(name='author', import_name=__name__)


@author_bp.route('/authors')
def get_authors():
    """
    Returns all the authors.
    :return:
    """
    authors = Author.query.all()
    return {
        'status': 'success',
        'data': authors_schema.dump(authors)
    }


@author_bp.route('/authors', methods=['POST'])
def add_author():
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


@author_bp.route('/authors/<int:id>')
def get_author_by_id(id: int):
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


@author_bp.route('/authors/<int:id>', methods=['PUT'])
def update_author(id: int):
    """
    Updates the author with the given ID.
    :param id: int
    :return:
    """
    author = Author.query.get_or_404(id, description='Author not found')

    try:
        updated_author = author_schema.load(request.get_json(), partial=True)
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
    }, 201


@author_bp.route('/authors/<int:id>', methods=['DELETE'])
def delete_author(id: int):
    """
    Deletes the author with the given ID.
    :param id: int
    :return:
    """
    author = Author.query.get_or_404(id, description='Author not found')
    db.session.delete(author)
    db.session.commit()
    return '', 204
