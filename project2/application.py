import os
import time, datetime
import uuid

from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channel_logs = { 'General' : [] }

@app.route("/", methods=['GET', 'POST'])
def index():
    #if user is logged in go to messages
    if 'handle' in session:
        return redirect(url_for('messages', channel=session.get("last_channel")))

    #otherwise go to login form
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    #render login form if GET
    if request.method == "GET":
        return render_template("login.html", error="")

    #don't bother checking if handle is taken since its not in the project spec
    handle = request.form.get("handle")

    #add handle to user cookie
    session['handle'] = handle

    return redirect(url_for('messages', channel='General'))

@app.route("/logout")
def logout():

    if session.get('handle') == None:
        redirect(url_for("login"))

    session.pop("handle", None)
    session.pop("last_channel", None)

    return redirect(url_for("index"))

@app.route("/messages/<string:channel>", methods=["GET"])
def messages(channel):

    if session.get('handle') == None:
        return redirect(url_for("login"))

    #should redirect to 404
    if not channel in channel_logs.keys():
        return redirect(url_for("messages", channel="General"))

    session["last_channel"] = channel

    return render_template("messages.html", channel=channel, \
        chatlog=channel_logs[channel], channel_names=channel_logs.keys(), \
        sender=session.get('handle'))


@socketio.on('connect')
def handle_message():
    print("client connected!")
    return

@socketio.on('message')
def handle_my_event(data):
    data['sender'] = session['handle']
    data['timestamp'] = getCurrentTime()
    data['id'] = uuid.uuid4().hex

    #add message to channel logs
    channel_name = data['channel']

    #add message to channel logs
    channel_logs[channel_name].append(data)

    #limit storage of messages to last 100
    if len(channel_logs[channel_name]) > 100:
        channel_logs[channel_name].pop(0)

    #add to channel's chat log
    emit('broadcast_message', data, broadcast=True)
    return

@socketio.on('delete_message')
def delete_message(data):
    channel_name = data['channel']
    id = data['id']

    for index in range(len(channel_logs[channel_name])):
        message = channel_logs[channel_name][index]
        if message['id'] == id:
            channel_logs[channel_name].pop(index)
            break

    #add to channel's chat log
    emit('delete_message', data, broadcast=True)
    return


@socketio.on('add_channel')
def handle_message(data):
    name = data['name']
    channel_logs[name] = []

    emit('channel_added', name, broadcast=True)
    return

def getCurrentTime():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%H:%M %m-%d-%Y')


if __name__ == '__main__':
    socketio.run(app)