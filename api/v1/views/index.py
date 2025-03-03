#!/usr/bin/python3
"""create routes on app_views object"""
from api.v1.views import app_views
from flask import jsonify
import models
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def status():
    """return a json format status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def count_obj():
    """retrieve the number of each objects by type"""
    cls = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}
    result_dict = {}
    for k, v in cls.items():
        number = models.storage.count(v)
        result_dict[k] = number
    return jsonify(result_dict)
