#!/usr/bin/python3
"""[handle all default RestFul API actions for state objects]
"""


from flask import Flask, abort, jsonify, make_response, request
from models import storage
from models.state import State
from api.v1.views import app_views
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def amenitygetter(amenity_id):
    """[get amenty by id]
    Returns:
        [json]: [description]
    """
    amenity = storage.all(Amenity).values()
    if amenity_id is not None:
        for obj in amenity:
            if obj.id == amenity_id:
                return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/amenities', strict_slashes=False)
def amenitygetterall():
    """[get all users]

    Args:
        state_id ([]): [description]

    Returns:
        [json]: [description]
    """
    amenity = storage.all(Amenity).values()
    objs = []
    for obj in amenity:
        objs.append(obj.to_dict())
    return jsonify(objs)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteamenity(amenity_id):
    """[delete a state by id]

    Returns:
        [json response]: [description]
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def createamenity():
    """[create state]

    Returns:
        [type]: [description]
    """
    cont = request.get_json()
    if cont is None:
        abort(400, "Not a JSON")
    elif "name" not in cont.keys():
        abort(400, "Missing name")
    else:
        amenity = Amenity(**cont)
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def updateamenity(amenity_id=None):
    """[update state by id]

    Args:
        state_id ([type]): [description]
    """
    amenity = storage.get(Amenity, amenity_id)
    cont = request.get_json()
    if amenity:
        if cont is None:
            abort(400, "Not a JSON")
        for key, value in cont.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict())
    if amenity is None:
        abort(404)
