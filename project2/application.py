import os

from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)

print("Active on http://localhost:5000")

users = []
channel_logs = { 'General' : [] }

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

    #add user to general channel
    session['current_channel'] = 'General'

    return redirect(url_for('messages'))

@app.route("/logout")
def logout():

    if session.get('handle') == None:
        redirect(url_for("login"))

    #unregister user
    users.remove(session["handle"])
    session.pop("handle", None)

    return redirect(url_for("index"))

@app.route("/messages")
def messages():

    if session.get('handle') == None:
        return redirect(url_for("login"))

    cur_channel = session['current_channel']
    chatlog = channel_logs[cur_channel]
    return render_template("messages.html", channel=cur_channel, chatlog=chatlog)

@socketio.on('connect')
def handle_message():
    print("client connected!")
    return

@socketio.on('message')
def handle_my_event(data):
    print(data)
    data['sender'] = session['handle']

    #add to channel's chat log
    channel_logs[session['current_channel']].append(data)
    emit('broadcast_message', data, broadcast=True)
    return

if __name__ == '__main__':
    socketio.run(app)