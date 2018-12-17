import os

from flask import Flask, session, jsonify, abort, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("base.html")

@app.route("/api/<isbn>", methods=["GET"])
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
