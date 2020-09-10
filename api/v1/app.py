#!/usr/bin/python3
"""
[flask app]
"""


from api.v1.views import app_views
from models import storage
from flask import Flask, make_response
from os import getenv
from flask import jsonify
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r'/*': {"origins": "0.0.0.0"}})
swagger = Swagger(app)


@app.errorhandler(404)
def not_found(error):
    """"[404 error handler]"

    Args:
        er ([type]): [description]
    """
    return make_response(jsonify({'error': 'Not found'}), 404)
