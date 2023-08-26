#!/usr/bin/python3
"""view for Amenity objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import Flask, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """retrieves a list of all amenity objects"""
    obj_list = []
    obj_dict = storage.all(Amenity)
    for obj in obj_dict.values():
        obj_list.append(obj.to_dict())
    return jsonify(obj_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """retrieves amenity object based on ID"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes amenity object based on ID"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates new amenity object """
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if 'name' not in data.keys():
        abort(400, description="Missing name")
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """updates an amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore_list = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_list:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
