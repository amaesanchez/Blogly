from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, connect_db, Post

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

connect_db(app)

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        second_user = User(
            first_name="test2_first",
            last_name="test2_last",
            image_url=None,
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        test_post = Post(
            title="This is a test",
            content="hurray you passed maybe",
            user_id=test_user.id
        )

        db.session.add(test_post)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """ renders users_listing template """
        with self.client as c:
            resp = c.get("/users")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_add_user_to_table(self):
        """ checks redirection location is /users """
        with self.client as c:
            resp = c.post("/users-new", data={
                "first_name" : "Arlaine",
                "last_name" : "Ditto",
                "image_url" : None
            })

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")

    def test_add_user_redirection_followed(self):
        """ adds user to the table in blogly and redirects to /users page """
        with self.client as c:
            resp = c.post("/users-new", data={
                "first_name" : "Arlaine",
                "last_name" : "Ditto",
                "image_url" : None
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Arlaine Ditto", html)

    def test_displays_user_details(self):
        """ renders the user details page """
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test1_first", html)

    def test_displays_user_edit_form(self):
        """ renders user edit form """
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}/edit")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edit a user", html)




class PostViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        second_user = User(
            first_name="test2_first",
            last_name="test2_last",
            image_url=None,
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        test_post = Post(
            title="This is a test",
            content="hurray you passed maybe",
            user_id=test_user.id
        )

        db.session.add(test_post)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_displays_new_post_form(self):
        """ renders form to add new post """
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}/posts/new")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Add Post for test1_first test1_last", html)

    def test_add_new_post(self):
        """ adds new post to the posts table in blogly and checks
            redirection location is the user details page """

        with self.client as c:

            resp = c.post("/users/1/posts/new", data={
                "title" : "I like cheese",
                "content" : "because it's dope",
                "user_id" : self.user_id
            })

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f"/users/{self.user_id}")

    def test_add_new_post_redirection(self):
        """ checks that when new post is added, page redirects to user
            details page """

        with self.client as c:

            resp = c.post(f"/users/{self.user_id}/posts/new", data={
                "title" : "I like cheese",
                "content" : "because it's dope",
                "user_id" : self.user_id
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("I like cheese", html)

    def test_display_post(self):
        """ test that post details loads """
        with self.client as c:

            resp = c.get(f"/posts/{self.post_id}")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("By test1_first test1_last", html)
