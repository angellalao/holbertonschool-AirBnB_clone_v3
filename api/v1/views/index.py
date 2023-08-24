#!/usr/bin/python3
"""create routes on app_views object"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def API_status():
    """return a json format status"""
    return jsonify({"status": "OK"})
