#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions."""

from flask import abort, jsonify, request
from models.states import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_all_cities(state_id):
    """Get all city objects from the state in storage."""
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    else:
        cities_list = [city.to_dict() for city in state.cities]
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_single_city(city_id):
    """"Get the city object with the given id from storage."""
    city = storage.get(City, city_id)
    """Return the city object in JSON otherwise 404 error."""
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = storage.get(City, city_id)
    if city:
        """Delete the state object from storege and save changes
           and return empty JSON with status code 200
           otherwise return 404 error.
        """
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def add_city(state_id):
    """If the request data is not in JSON format
       and if 'name' key is missing in the JSON
       data return error 400.Otherwise add new State
       object with the JSON data
    """
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, 'Not a JSON or Missing name')

    city = City(**data)
    city.save()
    """ Return the newly created State object
        in JSON format with 201 status code.
    """
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a State object.
       Get the State object with
       the given ID from the storage.
     """

    city = storage.get(City, city_id)
    if not city:
        """Return 404 if state is not found."""
        abort(404)

    data = request.get_json()
    if not data:
        """Return 400 if request data is not JSON."""
        abort(400, 'Not a JSON')

    """Update the attributes of the State object with the JSON data."""
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    """Save the updated State object to the storage
       Return the updated State object in JSON format
       with 200 status code.
    """
    city.save()
    return jsonify(city.to_dict()), 200


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
