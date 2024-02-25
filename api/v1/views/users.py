#!/usr/bin/python3
"""User objects that handle all default RESTFul API actions."""

from flask import abort, jsonify, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Get all user objects from the storage."""
    users = storage.all(User).values()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Get the user object with the given id from storage."""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """Add a new user object."""
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        abort(400, 'Not a JSON or Missing email or Missing password')

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a user object."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict()), 200


@app_views.errorhandler(404)
def not_found(error):
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
