#!/usr/bin/python3
"""build Flask application and register blueprint"""
from api.v1.views import app_views
from flask import Flask
from flask import Blueprint
from flask import jsonify
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def app_teardown(exception):
    """removes current SQLAlchemy session"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """returns json formatted 404 status code response if page not found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host_name = os.getenv('HBNB_API_HOST', '0.0.0.0')
    host_port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host_name, port=host_port, threaded=True)
