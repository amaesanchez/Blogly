from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""Models for Blogly."""

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
