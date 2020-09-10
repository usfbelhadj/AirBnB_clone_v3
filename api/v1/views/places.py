#!/usr/bin/python3
"""[handle all default RestFul API actions for state objects]
"""


from flask import Flask, abort, jsonify, make_response, request
from models import storage
from models.state import State
from api.v1.views import app_views
from models.city import City
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def placegetter(place_id):
    """[get amenty by id]
    Returns:
        [json]: [description]
    """
    places = storage.all(Place).values()
    if place_id is not None:
        for obj in places:
            if obj.id == place_id:
                return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def getallplace(city_id=None):
    """[get all users]

    Args:
        state_id ([]): [description]

    Returns:
        [json]: [description]
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify([place.to_dict() for place in city.places])
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def deleteplace(place_id):
    """[delete request]
    Args:
        place_id ([str]): [place id]
    Returns:
        [json]: [200 on success or 404 status on failure]
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def createplace(city_id):
    """[create state]

    Returns:
        [type]: [description]
    """
    from models.place import Place
    city = storage.get(City, city_id)
    if city:
        cont = request.get_json()
        user = storage.get(User, cont['user_id'])
        if not cont:
            abort(400, "Not a JSON")
        if 'user_id' not in cont:
            abort(400, "Missing user_id")
        if not user:
            abort(404)
        if 'name' not in cont:
            abort(400, "Missing name")
        cont['city_id'] = city.id
        place = Place(**cont)
        storage.new(place)
        storage.save()
        return jsonify(place.to_dict()), 201
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updateplace(place_id=None):
    """[update state by id]

    Args:
        state_id ([type]): [description]
    """
    place = storage.get(Place, place_id)
    if place:
        cont = request.get_json()
        if cont is None:
            abort(400, "Not a JSON")
        for k, v in cont.items():
            if k in ['id', 'user_id', 'city_id', 'created_at',
                     'updated_at']:
                pass
            setattr(place, k, v)
        storage.save()
        return jsonify(place.to_dict())
    abort(404)
