import os
import sqlite3

from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

################################################################################
# Configuration
################################################################################

app = Flask(__name__)

app.config["DATABASE_PATH"] = os.environ.get("DATABASE_PATH", "whoknows.db")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me-in-production")
app.config["DEBUG"] = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

PER_PAGE = 30


################################################################################
# Database Functions
################################################################################

def get_db():
    """Opens a new database connection if there is none yet for the current request."""
    if not hasattr(g, "db"):
        g.db = sqlite3.connect(app.config["DATABASE_PATH"])
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    """Creates the database tables."""
    db = sqlite3.connect(app.config["DATABASE_PATH"])
    with app.open_resource("schema.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
    print(f"Initialized the database: {app.config['DATABASE_PATH']}")


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


################################################################################
# Request Handlers
################################################################################

@app.before_request
def before_request():
    """Look up the current user before each request."""
    g.user = None
    if "user_id" in session:
        g.user = query_db("SELECT * FROM users WHERE id = ?", (session["user_id"],), one=True)


@app.teardown_appcontext
def close_db(exception):
    """Closes the database connection at the end of the request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


################################################################################
# Page Routes
################################################################################

@app.route("/")
def search():
    """Shows the search page."""
    q = request.args.get("q", None)
    language = request.args.get("language", "en")

    if not q:
        search_results = []
    else:
        search_results = query_db(
            "SELECT * FROM pages WHERE language = ? AND content LIKE ?",
            (language, f"%{q}%"),
        )

    return render_template("search.html", search_results=search_results, query=q)


@app.route("/about")
def about():
    """Displays the about page."""
    return render_template("about.html")


@app.route("/login")
def login():
    """Displays the login page."""
    if g.user:
        return redirect(url_for("search"))
    return render_template("login.html")


@app.route("/register")
def register():
    """Displays the registration page."""
    if g.user:
        return redirect(url_for("search"))
    return render_template("register.html")


################################################################################
# API Routes
################################################################################

@app.route("/api/search")
def api_search():
    """API endpoint for search. Returns search results as JSON."""
    q = request.args.get("q", None)
    language = request.args.get("language", "en")

    if not q:
        search_results = []
    else:
        rows = query_db(
            "SELECT * FROM pages WHERE language = ? AND content LIKE ?",
            (language, f"%{q}%"),
        )
        search_results = [dict(row) for row in rows]

    return jsonify(search_results=search_results)


@app.route("/api/login", methods=["POST"])
def api_login():
    """Logs the user in."""
    error = None
    user = query_db(
        "SELECT * FROM users WHERE username = ?",
        (request.form["username"],),
        one=True,
    )

    if user is None:
        error = "Invalid username"
    elif not check_password_hash(user["password"], request.form["password"]):
        error = "Invalid password"
    else:
        flash("You were logged in")
        session["user_id"] = user["id"]
        return redirect(url_for("search"))

    return render_template("login.html", error=error)


@app.route("/api/register", methods=["POST"])
def api_register():
    """Registers a new user."""
    if g.user:
        return redirect(url_for("search"))

    error = None
    if not request.form["username"]:
        error = "You have to enter a username"
    elif not request.form["email"] or "@" not in request.form["email"]:
        error = "You have to enter a valid email address"
    elif not request.form["password"]:
        error = "You have to enter a password"
    elif request.form["password"] != request.form["password2"]:
        error = "The two passwords do not match"
    elif query_db("SELECT id FROM users WHERE username = ?", (request.form["username"],), one=True) is not None:
        error = "The username is already taken"
    else:
        db = get_db()
        db.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (
                request.form["username"],
                request.form["email"],
                generate_password_hash(request.form["password"]),
            ),
        )
        db.commit()
        flash("You were successfully registered and can login now")
        return redirect(url_for("login"))

    return render_template("register.html", error=error)


@app.route("/api/logout")
def logout():
    """Logs the user out."""
    flash("You were logged out")
    session.pop("user_id", None)
    return redirect(url_for("search"))


################################################################################
# Main
################################################################################

if __name__ == "__main__":
    if not os.path.exists(app.config["DATABASE_PATH"]):
        init_db()
    app.run(host="0.0.0.0", port=8080, debug=app.config["DEBUG"])
