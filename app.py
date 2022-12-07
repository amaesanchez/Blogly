"""Blogly application."""

from flask import Flask, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.get("/")
def send_to_users():
    """ redirect to users """
    return redirect("/users")

    # users = User.query.all()
    # return render_template

@app.get("/users")
def show_users():
    """displays users"""

    users = User.query.all()

    return render_template(user_listing.html, users=users)

@app.post("/users-new")
def add_user():
"""adds a user to the table"""

    user_first_name = request.form.get("first_name")
    user_last_name = request.form.get("last_name")
    user_image_url = request.form.get("image_url")

    user = User(first_name=user_first_name, last_name=user_last_name, image_url=user_image_url)

    db.session.commit()

    return redirect("/users")

@app.get("/users-new")
def display_new_user_form():
    """displays the new user form"""

    return render_template("user_form.html")

@app.get("/users/<int:user-id>")
def display_user_details():
    """displays the users details"""

    return render_template("user_detail.html")

