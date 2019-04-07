#!/usr/bin/python

from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
from GazeDetection import GazeDetection
from flask_socketio import send, emit


app = Flask(__name__)
CORS(app)
socketIO = SocketIO(app)
mainClass = GazeDetection()


@app.route("/gazeDetection", methods=['POST'])
def gaze_detection():
    if request.method == 'POST':
        retVal = mainClass.main_method(request.get_json())
        ping(retVal)
        return "200"
    else:
        return "403"

@app.route('/ping')
def ping(data):
    socketIO.emit('ping event', data, namespace='/chat')


if __name__ == "__main__":
    socketIO.run(app, host="0.0.0.0", port=5000)
