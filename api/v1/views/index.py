#!/usr/bin/python3
"""Views for Airbnb Api."""
from flask import jsonify
from api.v1.views import app_views
from models import storage


# Create route /status on the object app_views
@app_views.route('/status')
def status():
    """Returns a JSON response for RESTful Api."""
    return jsonify(status="OK")
