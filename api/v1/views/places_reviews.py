#!/usr/bin/python3
"""view for Review objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import Flask, abort, request, jsonify
from models.place import Place
from models.user import User
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """retrieves a list of all review objects of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review_obj_list = place.reviews
    review_dict_list = []
    for obj in review_obj_list:
        review_dict = obj.to_dict()
        review_dict_list.append(review_dict)
    return jsonify(review_dict_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """retrieves review object based on ID"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes review object based on ID"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates new review object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if 'user_id' not in data.keys():
        abort(400, description="Missing user_id")
    user_id = data.get('user_id')
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    if 'text' not in data.keys():
        abort(400, description="Missing text")
    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """updates a review object"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore_list = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_list:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
