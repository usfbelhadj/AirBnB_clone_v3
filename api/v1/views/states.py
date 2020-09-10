#!/usr/bin/python3
"""[handle all default RestFul API actions for state objects]
"""


from flask import Flask, abort, jsonify, make_response, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=["GET"], strict_slashes=False)
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
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=["POST"], strict_slashes=False)
def createstate():
    """[create state]

    Returns:
        [type]: [description]
    """
    st = request.get_json()
    if st is None:
        abort(400, "Not a JSON")
    elif "name" not in st.keys():
        abort(400, "Missing name")
    else:
        new_state = State(**st)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


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
