#!/usr/bin/python3
"""connect to api"""

from api.v1.views import app_views
from flask import jsonify, Flask, Blueprint
from models import storage


dbClass = {
  "amenities": "Amenities",
  "cities": "Cities",
  "places": "Places",
  "reviews": "Reviews",
  "states": "States",
  "users": "Users"
}


@app_views.route('/status', strict_slashes=False)
def objStatus():
    """return the status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def ret_cls():
    """return the number of objects"""
    ret_dic = {}
    for k, v in dbClass.items():
        ret_dic[k] = storage.count(v)
    return jsonify(ret_dic)


if __name__ == "__main__":
    pass
