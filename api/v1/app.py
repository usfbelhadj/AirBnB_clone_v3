#!/usr/bin/python3
"""
[flask app]
"""


from api.v1.views import app_views
from models import storage
from flask import Flask, make_response
from os import getenv
from flask import jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """"[calling close function]"
    """
    storage.close()


@app.errorhandler(404)
def errorhandle(er):
    """"[404 error handler]"

    Args:
        er ([type]): [description]
    """
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    api_host = getenv('HBNB_API_HOST', default='0.0.0.0')
    api_port = getenv('HBNB_API_PORT', default=5000)
    app.run(host=api_host, port=int(api_port), threaded=True)
