#!/usr/bin/python3
"""
[index page]
"""

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State
from models import storage
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """[status]

    Returns:
        [type]: [string]
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def nobj():
    """[retrieve the number of each objects by type]
    """
    counts = {
        "amenities": storage.count("Amenity"),
        "states": storage.count("State"),
        "cities": storage.count("City"),
        "reviews": storage.count("Review"),
        "places": storage.count("Place"),
        "users": storage.count("User")
    }
    return jsonify(counts)
