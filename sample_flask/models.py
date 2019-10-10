# -*- coding: utf-8 -*-

"""
Flask models module.
"""

from datetime import datetime

from marshmallow import post_load, pre_load

from sample_flask import db, ma


# class ProductSchema(ma.Schema):
#     """
#     Product schema.
#     """
#
#     # class Meta:
#     #     fields = ('id', 'name', 'description', 'price', 'qty', 'date_created')
#
#     id = fields.Integer(dump_only=True)  # Mark this field to be "read-only"
#     name = fields.Str(required=True, validate=validate.Length(min=1))  # When doing deserialization, this field is required to exist in the JSON dictionary.
#     description = fields.Str(required=True)
#     price = fields.Float(
#         required=True, validate=validate.Range(min=0.0, min_inclusive=False)
#     )
#     qty = fields.Integer(required=True, validate=validate.Range(min=1))
#     date_created = fields.DateTime()


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


class AuthorSchema(ma.ModelSchema):
    """
    Author schema.
    For serialization, a Author object will be serialized to a JSON dictionary
    defined by this AuthorSchema.
    For deserialization, a JSON dictionary is validated, and then will be
    deserialized to:
    -> (by default) a dictionary defined by this AuthorSchema.
    """

    class Meta:
        """
        Automatically create this schema according to model "Author".
        """
        model = Author
        load_only = ('email',)

    _links = ma.Hyperlinks({
        'self': ma.URLFor('author_bp.get_author_by_id', id='<id>'),
        'collection': ma.URLFor('author_bp.get_authors')
    })

    @post_load
    def make_author(self, data: dict, **kwargs) -> Author:
        """
        After deserialization, the original JSON dictionary will be deserialized
        to an Author object.
        :param data: dict
        :return: Author
        """
        print('-------------------------')
        print(data)

        return Author(**data)


class BookSchema(ma.ModelSchema):
    """
    Book schema.
    """

    class Meta:
        """
        Automatically create this schema according to model "Book".
        """
        model = Book

    _links = ma.Hyperlinks({
        'self': ma.URLFor('book_bp.get_book_by_id', id='<id>'),
        'collection': ma.URLFor('book_bp.get_books')
    })

    @post_load
    def make_book(self, data: dict) -> Book:
        """
        After deserialization, the original JSON dictionary will be deserialized
        to a Book object.
        :param data: dict
        :return: Book
        """
        return Book(**data)
