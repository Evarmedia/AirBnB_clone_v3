#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions."""

from flask import abort, jsonify, request
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places_list = [place.to_dict() for place in city.places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_single_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_a_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    user = storage.get(User, user_id)

    if city is None:
        abort(404)

    if user is None:
        abort(404)

    data = request.get_json()

    if not request.json:
        abort(400, 'Not a JSON')

    if 'name' not in data:
        abort(400, 'Missing name')

    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200


"""Error Handlers."""


@app_views.errorhandler(404)
def not_found(error):
    """
    Returns a JSON response for 404 error (Not Found).
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    """
    Returns a JSON response for 400 error (Bad Request).
    """
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
