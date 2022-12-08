"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DEFAULT_IMAGE_URL = 'https://i.pinimg.com/550x/18/b9/ff/18b9ffb2a8a791d50213a9d595c4dd52.jpg'

# now = datetime.datetime.utcnow


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ table for Users """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,
        autoincrement=True)

    first_name = db.Column(db.Text, nullable=False)

    last_name = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

class Post(db.Model):
    """ Posts made by users """

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
    primary_key=True,
    autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime,nullable=False, default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')
