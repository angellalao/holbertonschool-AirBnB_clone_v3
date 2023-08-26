#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import Flask, abort, request, jsonify
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_of_state(state_id):
    """retrieves a list of all city objects of a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_obj_list = state.cities
    city_dict_list = []
    for obj in city_obj_list:
        city_dict = obj.to_dict()
        city_dict_list.append(city_dict)
    return jsonify(city_dict_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """retrieves city object based on ID"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes city object based on ID"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city():
    """creates new city object """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if 'name' not in data.keys():
        abort(400, description="Missing name")
    new_city = City(**data)
    new_city.state_id = state_id
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates a city object"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore_list = ["id", "state_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_list:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
