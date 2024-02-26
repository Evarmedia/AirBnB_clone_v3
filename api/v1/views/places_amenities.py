#!/usr/bin/python3
''' a new view for the link between Place objects and Amenity objects that 
handles all default RESTFul API actions: '''

from flask import Flask, jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views

@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


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
