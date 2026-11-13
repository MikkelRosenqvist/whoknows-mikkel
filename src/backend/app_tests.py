import os
import re
import tempfile
import unittest

import app


class WhoKnowsTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database."""
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.app.config["SECRET_KEY"] = "test-key-only"
        app.app.config["WTF_CSRF_ENABLED"] = True
        app.app.config["DATABASE_PATH"] = self.db_path
        app.app.config["TESTING"] = True
        self.client = app.app.test_client()

        with app.app.app_context():
            app.init_db()

    def tearDown(self):
        """Clean up after each test."""
        os.close(self.db_fd)
        os.unlink(self.db_path)

    # Helper functions

    def get_csrf_token(self, path):
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

        match = re.search(
            r'name="csrf_token" value="([^"]+)"',
            response.get_data(as_text=True),
        )

        self.assertIsNotNone(match)
        return match.group(1)

    def register(self, username, password, password2=None, email=None):
        """Helper function to register a user."""
        if password2 is None:
            password2 = password
        if email is None:
            email = username + "@example.com"
        return self.client.post("/api/register", data={
            "username": username,
            "password": password,
            "password2": password2,
            "email": email,
            "csrf_token": self.get_csrf_token("/register"),
        }, follow_redirects=True)

    def login(self, username, password):
        """Helper function to login."""
        return self.client.post("/api/login", data={
            "username": username,
            "password": password,
            "csrf_token": self.get_csrf_token("/login"),
        }, follow_redirects=True)

    def register_and_login(self, username, password):
        """Registers and logs in in one go."""
        self.register(username, password)
        return self.login(username, password)

    def logout(self):
        """Helper function to logout."""
        return self.client.post(
        "/api/logout",
        data={
            "csrf_token": self.get_csrf_token("/"),
        },
        follow_redirects=True,
    )

    # Tests

    def test_register(self):
        """Make sure registering works."""
        rv = self.register("user1", "default")
        self.assertIn(b"You were successfully registered and can login now", rv.data)
        rv = self.register("user1", "default")
        self.assertIn(b"The username is already taken", rv.data)
        rv = self.register("", "default")
        self.assertIn(b"You have to enter a username", rv.data)
        rv = self.register("meh", "")
        self.assertIn(b"You have to enter a password", rv.data)
        rv = self.register("meh", "x", "y")
        self.assertIn(b"The two passwords do not match", rv.data)
        rv = self.register("meh", "foo", email="broken")
        self.assertIn(b"You have to enter a valid email address", rv.data)

    def test_login_logout(self):
        """Make sure logging in and logging out works."""
        rv = self.register_and_login("user1", "default")
        self.assertIn(b"You were logged in", rv.data)
        rv = self.logout()
        self.assertIn(b"You were logged out", rv.data)
        rv = self.login("user1", "wrongpassword")
        self.assertIn(b"Invalid password", rv.data)
        rv = self.login("user2", "wrongpassword")
        self.assertIn(b"Invalid username", rv.data)

    def test_search_page(self):
        """Make sure the search page loads."""
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 200)

    def test_api_search(self):
        """Make sure the API search endpoint returns JSON."""
        rv = self.client.get("/api/search?q=test")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b"search_results", rv.data)


    def test_register_requires_csrf_token(self):
        """Registration without a CSRF token must be rejected."""
        response = self.client.post(
            "/api/register",
            data={
                "username": "csrf_test",
                "email": "csrf@example.com",
                "password": "secret",
                "password2": "secret",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_logout_requires_post(self):
        """Logout must not be allowed through GET."""
        self.register_and_login("logout_test", "password123")

        response = self.client.get("/api/logout")

        self.assertEqual(response.status_code, 405)

    def test_logout_requires_csrf_token(self):
        """Logout without a CSRF token must be rejected."""
        self.register_and_login("logout_csrf", "password123")

        response = self.client.post("/api/logout")

        self.assertEqual(response.status_code, 400)

        with self.client.session_transaction() as session:
            self.assertIn("user_id", session)


if __name__ == "__main__":
    unittest.main()
