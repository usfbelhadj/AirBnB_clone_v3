#!/usr/bin/python3
"""
Create a new view for Amenity objects that handles all default RestFul API
"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/api/v1/amenities', methods=['GET'], strict_slashes=False)
def ret_amenit():
    """retrieve the list of all amenity objects"""
    for amenity in storage.all('Amenity').values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_obj(amenity_id):
    """retrieve Amenity object"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    amenities = []
    for amenity in storage.all('Amenity').values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete Amenity object"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/api/v1/amenities', methods=['POST'], strict_slashes=False)
def creat_amenity():
    """ create a new amenity object"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    kwargs = request.get_json()
    kwargs['amenity_id'] = amenity_id
    amenity = Amenity(**kwargs)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def updat_amenity(amenity_id):
    """update an exist amenity object"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for k, v in all('Amenity').values():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict())
