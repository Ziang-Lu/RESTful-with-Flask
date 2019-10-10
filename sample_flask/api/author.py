# -*- coding: utf-8 -*-

"""
Author-related RESTful API module.
"""

from typing import Any

from flask import Blueprint, request
from marshmallow import EXCLUDE, ValidationError, validate

from .. import db
from ..models import Author, AuthorSchema

author_bp = Blueprint(name='author_bp', import_name=__name__)

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)


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
        new_author = author_schema.load(request.get_json(), unknown=EXCLUDE)  # When encountering a unknown fields, simply exclude it
    except ValidationError as e:
        return {
            'message': e.messages
        }, 400

    print('---------------------')
    print(new_author)

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
    author = Author.query.get(id)
    if not author:
        return {
            'status': 'error',
            'message': 'Author not found'
        }, 404

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
    author = Author.query.get(id)
    if not author:
        return {
            'status': 'error',
            'message': 'Author not found'
        }, 404

    json_data = request.get_json()

    name = json_data.get('name')
    try:
        validate_name_field(name)
    except ValidationError as e:
        return {
            'message': e.messages
        }, 400

    email = json_data.get('email')
    try:
        validate_email_field(name)
    except ValidationError as e:
        return {
            'message': e.messages
        }

    if name:
        author.name = name
    if email:
        author.email = email

    db.session.commit()

    return {
        'status': 'success',
        'data': author_schema.dump(author)
    }, 201


def validate_name_field(name: Any) -> None:
    """
    Helper function to validate the given name field.
    :param name: Any
    :return: None
    """
    try:
        name = str(name)
    except TypeError:
        raise ValidationError('name must be string')

    length_validator = validate.Length(max=Author.NAME_MAX_LEN)
    length_validator(name)


def validate_email_field(email: Any) -> None:
    """
    Helper function to validate the given email field.
    :param email:
    :return:
    """
    try:
        email = str(email)
    except TypeError:
        raise ValidationError('email must be string')

    validators = [
        validate.Length(max=Author.EMAIL_MAX_LEN),
        validate.Email()
    ]
    for validator in validators:
        validator(email)


@author_bp.route('/authors/<int:id>', methods=['DELETE'])
def delete_author(id: int):
    """
    Deletes the author with the given ID.
    :param id: int
    :return:
    """
    author = Author.query.get(id)
    if not author:
        return {
            'status': 'error',
            'message': 'Author not found'
        }, 404

    db.session.delete(author)
    db.session.commit()
    return '', 204
