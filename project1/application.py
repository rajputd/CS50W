import os

from flask import Flask, session, jsonify, abort, render_template, redirect, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from Models.User import User

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

if not os.getenv("SECRET_KEY"):
    raise RuntimeError("SECRET_KEY is not set")

#set SECRET_KEY
app.secret_key = os.getenv("SECRET_KEY")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    if not 'username' in session:
        return redirect("/login")

    return redirect("/search")

@app.route("/login", methods=["GET", "POST"])
def login():

    #if it is not a form submission render the form
    if request.method == "GET":
        return render_template("login.html", message="")

    #otherwise start authenticating user
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.get_user_by_username(db, username)

    # show invalid password/username message if authentication fails
    if not user.check_password(password):
        return render_template("login.html", message="Invalid username/password")

    #set up user session
    session['username'] = username

    return redirect("/search")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop('username', None)
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():

    #if it is not a form submission render the form
    if request.method == "GET":
        return render_template("register.html", message="")

    #otherwise start processing form inputs
    #get form parameters
    username = request.form.get("username")
    password = request.form.get("password")
    password_conf = request.form.get("password-conf")

    #if passwords don't match return an error
    if password != password_conf:
        return render_template("register.html", message="Passwords do not match")

    #set up model for user db queries
    userModel = User(db, username, password)

    #if user already exists then return an error
    if userModel.exists():
        return render_template("register.html", message="User already exists")

    #insert new user into DB
    try:
        userModel.register()
    #show an error message if something bad happens
    except:
        return render_template("register.html", message="We had an issue processing your registration, please try again at another time.")

    #display success
    return render_template("register.html", message="Successfully added user!")

@app.route("/search", methods=["GET", "POST"])
def search():
    return render_template("search.html")


@app.route("/api/<string:isbn>", methods=["GET"])
def api(isbn):
    response = {}

    #get book info
    q = f"SELECT * FROM books WHERE isbn='{isbn}' LIMIT 1"
    result = db.execute(q).fetchall()

    #send not found if isbn isn't in db
    if len(result) == 0:
        abort(404)

    #otherwise add book info to result
    response['isbn'] = result[0][1]
    response['title'] = result[0][2]
    response['author'] = result[0][3]
    response['year'] = result[0][4]

    #get review info
    q = f"""SELECT AVG(rating),
                COUNT(reviewer_id)
            FROM books
            JOIN reviews
                ON books.book_id = reviews.book_id
            WHERE isbn='{isbn}'"""
    result = db.execute(q).fetchall()

    #get review_count from query result
    response['review_count'] = result[0][1]

    #set average_score to none if there are no reviews for the book
    if response['review_count'] == 0:
        response['average_score'] = None
    else:
        response['average_score'] = float(result[0][0])

    return jsonify(response)
