# -*- coding: utf-8 -*-

"""
Authentication-related RESTful API module.
"""

from flask import g, request
from flask_restful import Resource
from marshmallow import ValidationError

from .. import auth, bcrypt, db
from ..models import User, user_schema


class UserItem(Resource):
    """
    Resource for a single user.
    """

    def post():
        """
        Adds a new user.
        :return:
        """
        try:
            user_data = user_schema.load(request.get_json())
        except ValidationError as e:
            return {
                'message': e.messages
            }, 400

        if User.query.filter_by(username=user_data['username']).first():
            return {
                'status': 'error',
                'message': 'User already exist'
            }, 400

        username, password = user_data['username'], user_data['password']
        new_user = User(
            username=username,
            password=bcrypt.generate_password_hash(password).decode('utf-8')
        )
        db.session.add(new_user)
        db.session.commit()
        return {
            'status': 'success',
            'data': user_schema.dump(new_user)
        }, 201


class Token(Resource):
    """
    Resource for token.
    """
    decorators = [auth.login_required]

    def get():
        """
        Gets a token for the current logged-in user.
        :return:
        """
        # After loggin in, we can access the user with "g.user"
        token, duration = g.user.generate_token()
        return {
            'token': token.decode('ascii'),
            'duration in seconds': duration
        }
