#!/usr/bin/python3
"""Views for Airbnb Api."""
from flask import jsonify
from api.v1.views import app_views
from models import storage


# Create route /status on the object app_views
@app_views.route('/status' strict_slashes=False)
def status():
    """Returns a JSON response for RESTful Api."""
    response = {'status': 'OK'}
    return jsonify(response)

if __name__ == "__main__":
    pass
