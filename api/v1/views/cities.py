#!/usr/bin/python3
"""[handle all default RestFul API actions for state objects]
"""


from flask import Flask, abort, jsonify, make_response, request
from models import storage
from models.state import State
from api.v1.views import app_views
from models.city import City


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def citygetter(city_id):
    """[get all states]
    Returns:
        [json]: [description]
    """
    states = storage.all("City").values()
    cities = []
    for city in states.cities:
        cities.append(city.to_dict())
    return jsonify(cities)

@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["GET"])
def citygetterst(state_id):
    """[get state by id]

    Args:
        state_id ([]): [description]

    Returns:
        [json]: [description]
    """
    stid = storage.get("State", state_id)
    if stid:
        return jsonify([city.to_dict() for city in state.cities])
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletecity(city_id):
    """[delete a state by id]

    Returns:
        [json response]: [description]
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def createcity(state_id):
    """[create state]

    Returns:
        [type]: [description]
    """
    ct = request.get_json()
    if ct is None:
        abort(400, "Not a JSON")
    elif "name" not in ct.keys():
        abort(400, "Missing name")
    else:
        new_state = City(**ct)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201
    


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updated(city_id):
    """[update state by id]

    Args:
        state_id ([type]): [description]
    """
    city = storage.get(City, city_id)
    ct = request.get_json()
    if ct:
        for key, value in ct.items():
            if key not in ["id", "created_at", "updated_at", "state_id"]:
                pass
            else:
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
    elif ct is None:
        abort(400, "Not a JSON")
    if city is None:
        abort(404)
