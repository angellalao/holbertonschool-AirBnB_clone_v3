#!/usr/bin/python3
"""view for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import Flask, abort, request, jsonify
from models.place import Place
from models.city import City
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_of_city(city_id):
    """retrieves a list of all place objects of a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_obj_list = city.places
    place_dict_list = []
    for obj in place_obj_list:
        place_dict = obj.to_dict()
        place_dict_list.append(place_dict)
    return jsonify(place_dict_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """retrieves place object based on ID"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes place object based on ID"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """creates new place object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if 'user_id' not in data.keys():
        abort(400, description="Missing user_id")
    if 'name' not in data.keys():
        abort(400, description="Missing name")
    user_id = data.get('user_id')
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    new_place = Place(**data)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updates a place object"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore_list = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_list:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
