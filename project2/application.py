import os

from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


print("Active on http://localhost:5000")

users = []

@app.route("/", methods=['GET', 'POST'])
def index():
    #if user is loged in go to messages
    if 'handle' in session:
        return redirect(url_for('messages'))

    #otherwise go to login form
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    #render login form if GET
    if request.method == "GET":
        return render_template("login.html", error="")

    #render error if handle is taken
    handle = request.form.get("handle")
    if handle in users:
        return render_template("login.html", error="Sorry, that handle is currently taken")

    #register handle and associate user with it
    users.append(handle)
    session['handle'] = handle

    return redirect(url_for('messages'))

@app.route("/logout")
def logout():
    #unregister user
    users.remove(session["handle"])
    session.pop("handle", None)

    return redirect(url_for("index"))

@app.route("/messages")
def messages():
    return render_template("messages.html")
