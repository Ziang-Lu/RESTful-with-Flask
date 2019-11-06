# -*- coding: utf-8 -*-

"""
Authentication-related RESTful API module.
"""

from typing import Optional

from flask import current_app, request
from flask_restful import Resource
from itsdangerous import (
    BadSignature, SignatureExpired,
    TimedJSONWebSignatureSerializer as Serializer
)
from marshmallow import ValidationError

from .. import bcrypt, db
from ..models import User, user_schema


class UserList(Resource):
    """
    Resource for a collections of users.
    """

    def post(self):
        """
        Adds a new user.
        :return:
        """
        try:
            user_data = user_schema.load(request.json)
        except ValidationError as e:
            return {
                'message': e.messages
            }, 400
        username = user_data['username']
        password = user_data['password']

        if User.query.filter_by(username=username).first():
            return {
                'status': 'error',
                'message': 'User already exist'
            }, 400

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


class UserAuth(Resource):
    """
    Resource for user authentication.
    """

    @classmethod
    def _verify_token(cls, token: str) -> Optional[User]:
        """
        Private static helper method to verify the given token.
        :param token: str
        :return: User or None
        """
        serializer = Serializer(secret_key=current_app['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except SignatureExpired:  # Valid token, but expired
            return None
        except BadSignature:  # Invalid token
            return None
        return User.query.get(data['id'])

    def get(self):
        """
        Handles user authentication.
        :return:
        """
        auth_data = request.json
        username_or_token = auth_data['username_or_token']
        password = auth_data['password']

        # Verify as if username_or_token is a token
        user = self._verify_token(username_or_token)
        username = None
        if user:
            username = user.username

        if username is None:
            # Verify the username and password combination
            user = User.query.filter_by(username=username_or_token).first()
            if user and bcrypt.check_password_hash(user.password, password):
                username = user.username

        if username is None:
            return {
                'status': 'error',
                'message': 'Authentication failed'
            }, 401

        return {
            'username': username
        }


class Token(Resource):
    """
    Resource for token.
    """

    def get(self):
        """
        Gets a token for the current logged-in user.
        :return:
        """
        user = User.query.filter_by(username=request.json['username']).first()
        token, duration = user.generate_token()
        return {
            'token': token.decode('ascii'),
            'duration in seconds': duration
        }
