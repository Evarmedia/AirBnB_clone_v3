#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions."""

from flask import abort, jsonify, request
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/d_cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    ''' Get all places in the specified city'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_single_place(place_id):
    ''' Returns a single place'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'])
def delete_a_place(place_id):
    ''' Delete a place'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/d_cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    ''' Create a new place'''
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    if not request.json:
        abort(400, 'Not a JSON')

    data = request.get_json()

    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    user = storage.get(User, data['user_id'])

    if user is None:
        abort(404)

    if 'name' not in data:
        abort(400, 'Missing name')

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


@app_views.route('/places_search', methods=['POST'])
def search_places():
    # Check if request body is valid JSON
    if not request.is_json:
        abort(400, description="Not a JSON")

    # Parse JSON body
    data = request.get_json()

    # Extract optional keys
    d_states = data.get('d_states', [])
    d_cities = data.get('d_cities', [])
    d_amenities = data.get('d_amenities', [])

    # Retrieve all places if the lists are empty
    if not d_states and not d_cities:
        places = storage.all(Place).values()
    else:
        # Retrieve places based on d_states and d_cities
        place_ids = set()
        for state_id in d_states:
            state = storage.get(State, state_id)
            if state:
                place_ids.update([city.id for city in state.d_cities])

        for city_id in d_cities:
            city = storage.get(City, city_id)
            if city:
                place_ids.add(city.id)

        places = [storage.get(Place, place_id)
                  for place_id in place_ids if storage.get(Place, place_id)]

    # Filter places based on d_amenities
    if d_amenities:
        filtered_places = []
        for place in places:
            if all(amenity_id in place.d_amenities
                   for amenity_id in d_amenities):
                filtered_places.append(place)
        places = filtered_places

    return jsonify([place.to_dict() for place in places])


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
