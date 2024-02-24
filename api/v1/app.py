#!/usr/bin/python3
"""Flask Api application."""

from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

"""Creatingg a variable app instance of Flask."""
app = Flask(__name__)

"""Enabling cors and allowing origins."""
CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})

"""Register the blueprint app_views to Flask instance app."""
app.register_blueprint(app_views)

"""Enforce strict trally slashes on routes."""
app_url_map.strict_slashes = False


def teardown_engine(Exception):
    """Remove current SQLAlchemy session object after each request."""
    storage.close()


if __name__ == "__main__":

    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
