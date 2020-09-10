#!/usr/bin/python3
"""create a new view for City objects that handles all default RestFul API."""

from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def ret_allcities(state_id):
    """retrieve all City object of a State"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    li = []
    for city in state.li:
        li.append(city.to_dict())
    return jsonify(li)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def ret_city(city_id):
    """retrieve information from a given city"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())
