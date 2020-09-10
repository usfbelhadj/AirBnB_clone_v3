#!/usr/bin/python3
"""[handle all default RestFul API actions for state objects]
"""


from flask import Flask, abort, jsonify, make_response, request
from models import storage
from models.state import State
from api.v1.views import app_views
from models.city import City
from models.amenity import Amenity
from models.user import User


@app_views.route('/users/<user_id>', strict_slashes=False)
def usergetter(user_id):
    """[get user by id]

    Args:
        state_id ([]): [description]

    Returns:
        [json]: [description]
    """
    user = storage.all("User").values()
    if user_id is not None:
        for obj in user:
            if obj.id == user_id:
                return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/users', strict_slashes=False)
def usergetterall():
    """[get all user]
    Returns:
        [json]: [description]
    """
    objs = []
    users_values = storage.all("User").values()
    for obj in users_values:
        objs.append(obj.to_dict())
    return jsonify(objs)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteUser(user_id):
    """[delete a state by id]

    Returns:
        [json response]: [description]
    """
    user = storage.get("User", user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def createuser():
    """[create state]

    Returns:
        [type]: [description]
    """
    cont = request.get_json()
    if cont is None:
        abort(400, "Not a JSON")
    elif "email" not in cont.keys():
        abort(400, "Missing email")
    elif "password" not in cont.keys():
        abort(400, "Missing password")
    else:
        user = User(**cont)
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def updateuser(user_id=None):
    """[update state by id]

    Args:
        state_id ([type]): [description]
    """
    user = storage.get(User, user_id)
    if user:
        cont = request.get_json()
        if cont is None:
            abort(400, "Not a JSON")
        for key, value in cont.items():
            if key in ['id', 'email', 'created_at', 'updated_at']:
                pass
            setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict())
    elif cont is None:
        abort(400, "Not a JSON")
    abort(404)
