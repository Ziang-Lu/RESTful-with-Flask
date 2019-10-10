# -*- coding: utf-8 -*-

"""
Flask models module.
"""

from datetime import datetime

from marshmallow import post_dump

from sample_flask import db, ma


class Author(db.Model):
    """
    Author table.
    """
    __tablename__ = 'authors'

    NAME_MAX_LEN = 100
    EMAIL_MAX_LEN = 120

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(NAME_MAX_LEN), nullable=False)
    email = db.Column(db.String(EMAIL_MAX_LEN))
    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return f"Author('{self.name}')"


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
    date_published = db.Column(db.Date, nullable=False, default=datetime.today)

    def __repr__(self):
        return f"Book('{self.title}' by '{self.author.name}')"


# Note:
# Schemas are only used with naive RESTful API implementation.

# class ProductSchema(ma.Schema):
#
#     # class Meta:
#     #     fields = ('id', 'name', 'description', 'price', 'qty', 'date_created')
#
#     id = fields.Integer(dump_only=True)  # Mark this field to be "read-only", so it won't be serialized.
#     name = fields.Str(required=True, validate=validate.Length(min=1))  # When doing deserialization, this field is required to exist in the JSON dictionary.
#     description = fields.Str(required=True)
#     price = fields.Float(
#         required=True, validate=validate.Range(min=0.0, min_inclusive=False)
#     )
#     qty = fields.Integer(required=True, validate=validate.Range(min=1))
#     date_created = fields.DateTime()


class AuthorSchema(ma.ModelSchema):
    """
    Author schema.
    For serialization, a Author object will be serialized to a JSON dictionary
    defined by this AuthorSchema.
    For deserialization, a JSON dictionary is validated, and then will be
    deserialized to:
    -> (by default) a dictionary defined by this AuthorSchema.
    -> (since we defined "model = Author") an Author object
    """

    class Meta:
        # Automatically create this schema according to model "Author", and for
        # deserialization, a JSON dictionary will be deserialized to an Author
        # object.
        model = Author
        # This field is loaded only, so it won't be serialized.
        load_only = ('email',)

    _links = ma.Hyperlinks({
        'self': ma.URLFor(
            'author_bp.get_author_by_id', id='<id>', _external=True
        ),
        'collection': ma.URLFor('author_bp.get_authors', _external=True)
    })

    @post_dump
    def marshal_collection_response(self, data: dict, **kwargs) -> dict:
        """
        After serialization, if returning a collection of authors, marshal the
        data for each author.
        :param data: dict
        :param kwargs:
        :return: dict
        """
        if self.many:
            data.pop('books')
            data['url'] = data['_links']['self']
            data.pop('_links')
        return data


class BookSchema(ma.ModelSchema):
    """
    Book schema.
    """

    class Meta:
        model = Book

    _links = ma.Hyperlinks({
        'self': ma.URLFor('book_bp.get_book_by_id', id='<id>', _external=True),
        'collection': ma.URLFor('book_bp.get_books', _external=True)
    })

    def marshal_collection_response(self, data: dict, **kwargs) -> dict:
        """
        After serialization, if returning a collection of books, marshal the
        data for each book.
        :param data: dict
        :param kwargs:
        :return: dict
        """
        if self.many:
            data['url'] = data['_links']['self']
            data.pop('_links')
        return data
