import os

from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

print("Active on http://localhost:5000")

@app.route("/")
def index():
    return "Project 2: TODO is working"
