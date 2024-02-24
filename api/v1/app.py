#!/usr/bin/python3
"""Flask Api application."""

import os
from flask import Flask
from flask_cors import CORS

from models import storage
from api.v1.views import app_views

"""Creatingg a variable app instance of Flask."""

app = Flask(__name__)
"""Creatingg a variable app instance of Flask."""
HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
PORT = int(os.getenv('HBNB_API_PORT', '5000'))
"""Enforce strict trally slashes on routes."""
app.url_map.strict_slashes = False
"""Register the blueprint app_views to Flask instance app."""
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': HOST}})

@app.teardown_appcontext
def teardown_engine(exception):
    """Remove current SQLAlchemy session object after each request."""
    storage.close()


if __name__ == "__main__":

    HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(
        host=HOST,
        port=PORT,
        threaded=True
        )
