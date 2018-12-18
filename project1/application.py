import os

from flask import Flask, session, jsonify, abort, render_template, redirect, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from Models.User import User
from Models.Book import Book
from Models.Review import Review

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
    if 'username' in session:
        return redirect("/search")

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
    if not 'username' in session:
        return redirect("/login")

    if request.method == "GET":
        return render_template("search.html")

    query = request.form.get("search")
    books = Book.find(db, query)

    return render_template("search.html", search_results=books)


@app.route("/book/<string:bookId>", methods=["GET", "POST"])
def book(bookId):
    if not 'username' in session:
        return redirect("/login")

    #get book
    book = Book.get_by_id(db, bookId)

    #abort if that book is never found
    if book == None:
        abort(404)

    #process form submission
    if request.method == "POST":
        content = request.form.get("review_content")
        rating = request.form.get("rating")
        user = User.get_user_by_username(db, session['username'])
        user_id = user.get_user_id()

        #try to store review into DB
        try:
            Review.create(db, rating, content, user_id, book.bookId)
        except:
            reviews = Review.get_reviews_by_bookId(db, book.bookId)
            render_template("book.html", book=book, reviews=reviews, message="Error: could not submit review. Please try again later")

    reviews = Review.get_reviews_by_bookId(db, book.bookId)
    return render_template("book.html", book=book, reviews=reviews, message="")


@app.route("/api/<string:isbn>", methods=["GET"])
def api(isbn):
    response = {}

    #get book data from db
    book = Book.get_by_isbn(db, isbn)

    #send 404 not found if isbn isn't in db
    if book == None:
        abort(404)

    #otherwise add book info to result
    response['isbn'] = book.isbn
    response['title'] = book.title
    response['author'] = book.author
    response['year'] = book.year
    response['average_score'] = Review.get_avg_rating(db, book.bookId)
    response['review_count'] = Review.get_review_count(db, book.bookId)

    return jsonify(response)
