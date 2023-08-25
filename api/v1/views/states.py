#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import Flask, abort, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """retrieves a dictionary of all state objects"""
    obj_list = []
    obj_dict = storage.all(State)
    for obj in obj_dict.values():
        obj_list.append(obj)
    return jsonify(obj_list.to_dict())


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """retrieves state object based on ID"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """deletes state object based on ID"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates new state object """
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if 'name' not in data.keys():
        abort(400, description="Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updates a state object"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore_list = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_list:
            obj[key] = value
    obj.save()
    return jsonify(obj.to_dict()), 200
