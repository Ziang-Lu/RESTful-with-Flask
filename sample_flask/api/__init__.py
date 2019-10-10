from flask import Blueprint
from flask_restful import Api, Resource


class AuthorResource(Resource):
    pass


class BookResource(Resource):
    pass


# Create an API-related blueprint
api_bp = Blueprint(name='api_bp', import_name=__name__)

api = Api(api_bp)
api.add_resource(AuthorResource, '/authors')
api.add_resource(BookResource, '/books')
