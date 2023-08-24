#!/usr/bin/python3
"""build Flask application and register blueprint"""
from api.v1.views import app_views
from flask import Flask
from flask import Blueprint
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def app_teardown():
    """removes current SQLAlchemy session"""
    storage.close()


if __name__ == "__main__":
    host_h = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port_h = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host_h, port=port_h, threaded=True)
