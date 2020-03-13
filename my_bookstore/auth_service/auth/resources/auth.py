# -*- coding: utf-8 -*-

"""
Authentication-related RESTful API module.
"""

from flask import request
from flask_restful import Resource
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
        email = user_data['email']
        password = user_data['password']

        if User.query.filter_by(username=username).first():
            return {
                'status': 'error',
                'message': 'User already exist'
            }, 400

        new_user = User(
            username=username,
            email=email,
            password=bcrypt.generate_password_hash(password).decode('utf-8')
        )
        db.session.add(new_user)
        db.session.commit()
        return {
            'status': 'success',
            'data': {
                'new_user': user_schema.dumps(new_user),
                'access_token': new_user.gen_access_token()
            }
        }, 201


class UserAuth(Resource):
    """
    Resource for user authentication.
    """

    def get(self):
        """
        Handles user authentication.
        :return:
        """
        auth_data = request.json
        username_or_token = auth_data['username_or_token']
        password = auth_data['password']

        # Verify as if username_or_token is an access token
        found_username = None
        found_user = User.verify_access_token(username_or_token)
        if found_user:
            found_username = found_user.username
        else:
            # Verify the username and password combination
            user = User.query.filter_by(username=username_or_token).first()
            if user and bcrypt.check_password_hash(user.password, password):
                found_username = user.username

        if found_username is None:  # User not found
            return {
                'status': 'error',
                'message': 'User not found. Authentication failed.'
            }, 401
        return {
            'status': 'success',
            'data': found_username
        }


class AccessToken(Resource):
    """
    Resource for access token.
    """

    def get(self):
        """
        Gets an access token for the current logged-in user.
        :return:
        """
        user = User.query.filter_by(username=request.json['username']).first()
        access_token, duration = user.gen_access_token()
        return {
            'access token': access_token.decode('ascii'),
            'duration in seconds': duration
        }
