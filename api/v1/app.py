#!/usr/bin/python3
"""
Createw Flask app; and register the blueprint app_views to Flask instance app.
"""

from os import getenv
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)

# enable CORS and allow for origins:
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


#app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_engine(exception):
    """
    Removes the current SQLAlchemy Session object after each request.
    """
    storage.close()


# Error handlers for expected app behavior:
@app.errorhandler(404)
def not_found(error):
    """
    Return errmsg `Not Found`.
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host, port, threaded=True)
