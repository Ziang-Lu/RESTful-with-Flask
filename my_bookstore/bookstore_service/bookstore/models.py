# -*- coding: utf-8 -*-

"""
Bookstore-related models module.
"""

from datetime import datetime

from marshmallow import EXCLUDE, fields, post_load, validate

from . import db, ma

##### MODELS #####


class Author(db.Model):
    """
    Author table.
    """
    __tablename__ = 'authors'

    NAME_MAX_LEN = 100
    EMAIL_MAX_LEN = 120

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(NAME_MAX_LEN), nullable=False, unique=True, index=True
    )  # Since we'll frequently query names, we create an index on it.
    email = db.Column(db.String(EMAIL_MAX_LEN))

    books = db.relationship(
        'Book',
        lazy=False,
        cascade='all, delete-orphan',
        backref=db.backref('author', lazy=False)
    )  # Author.books and Book.author are both eager-loading.


class Book(db.Model):
    """
    Book table.
    """
    __tablename__ = 'books'

    TITLE_MAX_LEN = 200

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(TITLE_MAX_LEN), nullable=False)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('authors.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )  # When the author is updated or deleted, all of his/her books are updated or deleted as well.
    description = db.Column(db.Text)
    date_published = db.Column(db.Date, nullable=False, default=datetime.today)


##### SCHEMAS #####


class AuthorSchema(ma.Schema):
    """
    Author schema.
    """

    id = fields.Integer(dump_only=True)
    name = fields.Str(
        required=True, validate=validate.Length(min=1, max=Author.NAME_MAX_LEN)
    )
    email = fields.Email(
        validate=validate.Length(max=Author.EMAIL_MAX_LEN), load_only=True
    )

    books = fields.Nested(
        'BookSchema', many=True, only=('title', 'url_self'), dump_only=True
    )

    url_self = ma.URLFor('api.author', id='<id>', _external=True)
    url_collection = ma.URLFor('api.authors', _external=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load_process_name(self, data: dict, **kwargs) -> dict:
        """
        After deserialization, process the "name" field to be in title case.
        :param data: dict
        :param kwargs:
        :return: dict
        """
        data['name'] = data['name'].strip().title()
        return data


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True, only=('name', 'url_self'))


class BookSchema(ma.Schema):
    """
    Book schema.
    """

    id = fields.Integer(dump_only=True)
    title = fields.Str(
        required=True, validate=validate.Length(min=1, max=Book.TITLE_MAX_LEN)
    )
    author_name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=Author.NAME_MAX_LEN),
        load_only=True
    )
    author = fields.Nested(
        'AuthorSchema', only=('name', 'url_self'), dump_only=True
    )
    description = fields.Str()
    date_published = fields.Date()

    url_self = ma.URLFor('api.book', id='<id>', _external=True)
    url_collection = ma.URLFor('api.books', _external=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load_process_title(self, data: dict, **kwargs) -> dict:
        """
        After deserialization, process the "title" field to be in title case.
        :param data: dict
        :param kwargs:
        :return: dict
        """
        data['title'] = data['title'].strip().title()
        return data


book_schema = BookSchema()
books_schema = BookSchema(many=True, only=('title', 'author', 'url_self'))
