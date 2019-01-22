import os

from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

print("Active on http://localhost:5000")

users = []

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("login.html", error="")
    else:
        if request.form.get("handle") in users:
            return render_template("login.html", error="Sorry, that handle is currently taken")
        else:
            users.append(request.form.get("handle"))
            return redirect(url_for('messages'))

@app.route("/messages")
def messages():
    return render_template("messages.html")
