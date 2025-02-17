#!/usr/bin/python3
"""
Creates a view for Amenity objects - handles all default RESTful API actions.
"""

from flask import abort, jsonify, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


# Route for retrieving all Amenity objects
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


# Route for retrieving a specific Amenity object by ID
@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


# Route for deleting a specific Amenity object by ID
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


# Route for creating a new Amenity object
@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an Amenity object"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    if 'name' not in data:
        abort(400, 'Missing name')

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


# Route for updating an existing Amenity object by ID
@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)

        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)


# Error Handlers:
@app_views.errorhandler(404)
def not_found(error):
    """Returns 404: Not Found"""
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    """Return Bad Request message for illegal requests to the API."""
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
