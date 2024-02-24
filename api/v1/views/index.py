#!/usr/bin/python3
"""Views for Airbnb Api."""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', method=[GET])
def status():
    """Returns a JSON response for RESTful Api."""
    return jsonify({"status": "OK"})
