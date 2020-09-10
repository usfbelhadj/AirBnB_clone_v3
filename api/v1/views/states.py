#!/usr/bin/python3
"""[handle all default RestFul API actions for state objects]
"""


from flask import Flask, abort, jsonify, make_response, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=["GET"])
def statesgetter():
    """[get all states]

    Returns:
        [json]: [description]
    """
    states = storage.all("State").values()
    sts = []
    for st in states:
        sts.append(st.to_dict())
    return jsonify(sts)


@app_views.route('/states/<state_id>', methods=["GET"])
def stategetter(state_id):
    """[get state by id]

    Args:
        state_id ([]): [description]

    Returns:
        [json]: [description]
    """
    stid = storage.get("State", state_id)
    if stid:
        return jsonify(stid.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=["DELETE"])
def deletestate(state_id):
    """[delete a state by id]

    Returns:
        [json response]: [description]
    """
    stid = storage.get("State", state_id)
    if stid:
        storage.delete(stid)
        storage.save()
    else:
        abort(404)
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>', methods=["POST"])
def createstate():
    """[create state]

    Returns:
        [type]: [description]
    """
    st = request.get_json()
    if st:
        n_st = State(**st)
        storage.new(st)
        storage.save()
        return jsonify(n_st.to_dict()), 201
    elif "name" not in st:
        abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route('/states/<state_id>', methods=["PUT"])
def updated(state_id):
    """[update state by id]

    Args:
        state_id ([type]): [description]
    """
    stid = storage.get("State", state_id)
    st = request.get_json()
    if st:
        for key, value in st.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(stid, key, value)
        storage.save()
        return jsonify(stid.to_dict()), 200
    elif st is None:
        abort(400, "Not a JSON")
    if stid is None:
        abort(404)
