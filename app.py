"""Blogly application."""

from flask import Flask, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
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

    return render_template("user_listing.html", users=users)

@app.post("/users-new")
def add_user():
    """adds a user to the table"""

    user_first_name = request.form.get("first_name")
    user_last_name = request.form.get("last_name")
    user_image_url = request.form.get("image_url") or None

    user = User(first_name=user_first_name, last_name=user_last_name, image_url=user_image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.get("/users-new")
def display_new_user_form():
    """displays the new user form"""

    return render_template("user_form.html")

@app.get("/users/<int:userid>")
def display_user_details(userid):
    """displays the users details"""

    user = User.query.get(userid)

    return render_template("user_detail.html", user = user)

@app.get("/users/<int:userid>/edit")
def display_user_edit_form(userid):
    """ displays user edit form """

    user = User.query.get(userid)

    return render_template("user_edit_form.html", user = user)

@app.post("/users/<int:userid>/edit")
def processes_edit_form(userid):
    """ processes the edit form and returns the user to the /users page """

    user = User.query.get(userid)
    user.first_name = request.form.get('first_name')
    user.last_name = request.form.get('last_name')
    user.image_url = request.form.get('image_url')

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.post("/users/<int:userid>/delete")
def delete_user(userid):
    """ deletes user from database """

    user = User.query.get(userid)
    posts = user.posts
    
    db.session.delete(posts)
    db.session.delete(user)
    # db.session.delete_all[(posts), (user)]
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int:userid>/posts/new")
def display_post_form(userid):
    """show form to add a post for that user"""

    user = User.query.get(userid)

    return render_template("post_add_form.html", user=user)

@app.post("/users/<int:userid>/posts/new")
def make_new_post(userid):
    """Handle add form; add post and redirect to the user detail page."""

    # post = Post.query.filter_by(uder_id=uderid)
    user = User.query.get(userid)

    title = request.form.get('title')
    content = request.form.get('content')

    new_post = Post(title = title, content = content, user_id = user.id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{userid}")

@app.get("/posts/<int:postid>")
def display_post(postid):
    """ show user's selected post """

    post = Post.query.get(postid)

    return render_template("post_details.html", post = post)

@app.get("/posts/<int:postid>/edit")
def display_post_edit_form(postid):
    """ show the post edit form """

    post = Post.query.get(postid)

    return render_template("post_edit_form.html", post = post)

@app.post("/posts/<int:postid>/edit")
def make_post_edits(postid):
    """ Handles editing of a post & redirects to post details """

    post = Post.query.get(postid)

    post.title = request.form.get("title")
    post.content = request.form.get("content")

    db.session.commit()

    return redirect(f"/posts/{post.id}")

@app.post("/posts/<int:postid>/delete")
def delete_post(postid):
    """ Deletes post from database """

    post = Post.query.get(postid)

    db.session.delete(post)
    db.session.commit()

    return redirect("/users")
