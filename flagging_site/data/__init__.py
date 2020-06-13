"""
The data module contains exactly what you'd expect: everything related to data
processing, collection, and storage.
"""
#source: https://hackersandslackers.com/flask-sqlalchemy-database-models/
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        from . import routes  # Import routes
        db.create_all()  # Create database tables for our data models

        return app