#!/usr/bin/python3
"""ReviewAPI"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=['GET'])
def reviewgetterall(review_id):
    """[get amenty by id]
    Returns:
        [json]: [description]
    """
    review = storage.get("Review", review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['GET'])
def reviewsgetter(place_id):
    """[get all users]

    Args:
        state_id ([]): [description]

    Returns:
        [json]: [description]
    """
    place = storage.get("Place", place_id)
    if place:
        return jsonify([review.to_dict() for review in place.reviews])
    abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def deletereview(review_id):
    """[delete a state by id]

    Returns:
        [json response]: [description]
    """
    review = storage.get("Review", review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['POST'])
def createreview(place_id):
    """[create state]

    Returns:
        [type]: [description]
    """
    from models.review import Review
    place = storage.get("Place", place_id)
    if place:
        cont = request.get_json()
        user = storage.get("User", cont['user_id'])
        if not cont:
            abort(400, "Not a JSON")
        if 'user_id' not in cont:
            abort(400, "Missing user_id")
        if not user:
            abort(404)
        if 'text' not in cont:
            abort(400, "Missing text")
        cont['place_id'] = place.id
        review = Review(**cont)
        storage.new(review)
        storage.save()
        return jsonify(review.to_dict()), 201
    abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def updatereview(review_id):
    """[update state by id]

    Args:
        state_id ([type]): [description]
    """
    review = storage.get("Review", review_id)
    if review:
        cont = request.get_json()
        if cont is None:
            abort(400, "Not a JSON")
        for key, value in cont.items():
            if key in ['id', 'created_at', 'updated_at',
                       'place_id', 'user_id']:
                pass
            setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict())
    abort(404)
