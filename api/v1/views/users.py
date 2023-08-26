#!/usr/bin/python3
"""view for User objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import Flask, abort, request, jsonify
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """retrieves a list of all user objects"""
    obj_list = []
    obj_dict = storage.all(User)
    for obj in obj_dict.values():
        obj_list.append(obj.to_dict())
    return jsonify(obj_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """retrieves user object based on ID"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(state_id):
    """deletes user object based on ID"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates new user object """
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if 'name' not in data.keys():
        abort(400, description="Missing name")
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """updates a user object"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore_list = ["id", "email", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_list:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
