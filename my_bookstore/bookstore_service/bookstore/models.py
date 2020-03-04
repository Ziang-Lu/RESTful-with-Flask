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
    name = db.Column(db.String(NAME_MAX_LEN), nullable=False, unique=True)
    email = db.Column(db.String(EMAIL_MAX_LEN))


class Book(db.Model):
    """
    Book table.
    """
    __tablename__ = 'books'

    TITLE_MAX_LEN = 200

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(TITLE_MAX_LEN), nullable=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey('authors.id', ondelete='CASCADE'),
        nullable=False
    )
    author = db.relationship(Author, backref=db.backref('books', lazy=True))  # Define the lazy status for the backref
    description = db.Column(db.Text)
    date_published = db.Column(db.Date, nullable=False, default=datetime.today)


##### SCHEMAS #####


class AuthorSchema(ma.Schema):
    """
    Author schema.
    For serialization, an Author object will be serialized to a JSON dictionary
    defined by this AuthorSchema.
    For deserialization, a JSON dictionary is validated, and then will be
    deserialized to a dictionary defined by this AuthorSchema.
    """

    id = fields.Integer(dump_only=True)  # Mark this field to be "dump-only", so it can't be deserialized from a request
    name = fields.Str(
        required=True, validate=validate.Length(min=1, max=Author.NAME_MAX_LEN)
    )  # When doing deserialization, this field is required to exist in the JSON dictionary.
    email = fields.Email(
        validate=validate.Length(max=Author.EMAIL_MAX_LEN), load_only=True
    )  # Mark this field to be "load-only", so it can't be serialized

    books = fields.Nested(
        'BookSchema', many=True, only=('title', 'url_self'), dump_only=True
    )

    # Note: For naive implementation, fix the blueprint prefix of the endpoints
    url_self = ma.URLFor('api.author', id='<id>', _external=True)
    url_collection = ma.URLFor('api.authors', _external=True)

    class Meta:
        unknown = EXCLUDE  # When encountering a unknown fields, simply exclude it

    @post_load
    def post_load_process_name(self, data: dict, **kwargs) -> dict:
        """
        After deserialization, do some post-processing on "name".
        :param data: dict
        :param kwargs:
        :return: dict
        """
        # Process "name" field to be in title case
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
    author = fields.Nested(
        AuthorSchema, required=True, only=('name', 'url_self')
    )
    description = fields.Str()
    date_published = fields.Date()

    # Note: For naive implementation, fix the blueprint prefix of the endpoints
    url_self = ma.URLFor('api.book', id='<id>', _external=True)
    url_collection = ma.URLFor('api.books', _external=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load_process_title(self, data: dict, **kwargs) -> dict:
        """
        After deserialization, do some post-processing on "title".
        :param data: dict
        :param kwargs:
        :return: dict
        """
        # Process "title" field to be in title case
        data['title'] = data['title'].strip().title()
        return data


book_schema = BookSchema()
books_schema = BookSchema(many=True, only=('title', 'author', 'url_self'))
