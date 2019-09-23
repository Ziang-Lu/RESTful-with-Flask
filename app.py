# -*- coding: utf-8 -*-

"""
Flask application module.
"""


from flask import Flask

app = Flask(__name__)

from api import api

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
