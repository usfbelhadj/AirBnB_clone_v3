#!/usr/bin/python3
"""
[flask app]
"""




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


@app.teardown_appcontext
def close(self):
    """"[calling close function]"
    """
    storage.close()


if __name__ == "__main__":
    api_host = getenv('HBNB_API_HOST', default='0.0.0.0')
    api_port = getenv('HBNB_API_PORT', default='5000')
    app.run(host=api_host, port=int(api_port), threaded=True)
