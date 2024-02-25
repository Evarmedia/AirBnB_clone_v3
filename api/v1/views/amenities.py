#!/usr/bin/python3
''' Amenity objects that handles all default RESTFul API actions.'''

from flask import abort, jsonify, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_all_amenities():
    """Get all amenities objects from the storage."""
    amenities = storage.all(Amenity).values()
    """Convert the object to dict and JSON."""
    amenities_list = [amenity.to_dict() for amenity in amenities]

    return jsonify(amenities_list)


@app_views.route('/amenities/<amenities_id>', methods=['GET'],
                 strict_slashes=False)
def get_single_amenities(amenities_id):
    """"Get the amenities object with the given id from storage."""
    amenities = storage.get(Amenity, amenities_id)
    """Return the amenities object in JSON otherwise 404 error."""
    if amenities:
        return jsonify(amenities.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenities_id>', methods=['DELETE'])
def delete_amenities(amenities_id):
    amenities = storage.get(Amenity, amenities_id)
    if amenities:
        """Delete the amenities object from storege and save changes
           and return empty JSON with status code 200
           otherwise return 404 error.
        """
        storage.delete(amenities)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def add_amenities():
    """If the request data is not in JSON format
       and if 'name' key is missing in the JSON
       data return error 400.Otherwise add new Amenity
       object with the JSON data
    """
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, 'Not a JSON or Missing name')

    amenities = Amenity(**data)
    amenities.save()
    """ Return the newly created State object
        in JSON format with 201 status code.
    """
    return jsonify(amenities.to_dict()), 201


@app_views.route('/amenities/<amenities_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenities(amenities_id):
    """Updates a State object.
       Get the State object with
       the given ID from the storage.
     """

    amenities = storage.get(Amenity, amenities_id)
    if not amenities:
        """Return 404 if state is not found."""
        abort(404)

    data = request.get_json()
    if not data:
        """Return 400 if request data is not JSON."""
        abort(400, 'Not a JSON')

    """Update the attributes of the Amenity object with the JSON data."""
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenities, key, value)
    """Save the updated State object to the storage
       Return the updated State object in JSON format
       with 200 status code.
    """
    amenities.save()
    return jsonify(amenities.to_dict()), 200


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
