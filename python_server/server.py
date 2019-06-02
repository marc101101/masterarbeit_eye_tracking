#!/usr/bin/python

from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from GazeDetection import GazeDetection

app = Flask(__name__)
CORS(app)
socketIO = SocketIO(app)
mainClass = GazeDetection()


# @app.route("/gazeDetection", methods=['POST'])
# def gaze_detection():
#     if request.method == 'POST':
#         retVal = mainClass.main_method(request.get_json())
#         ping(retVal)
#         return "200"
#     else:
#         return "403"

@socketIO.on('message')
def handle_message(message):
    print('received message: ' + str(message['client_id']))
    parsed_data = mainClass.main_method(message)
    emit_data_object = {
        'raw': message['client_id'],
        'parsed_data': parsed_data
    }
    emit('event', emit_data_object, broadcast=True)


@app.route('/config', methods=['GET'])
def get_config():
    if request.method == 'GET':
        return mainClass.get_cam_config()
    pass


@app.route('/config', methods=['POST'])
def set_config():
    if request.method == 'POST':
        return mainClass.set_cam_config(request.get_json())
    else:
        return "403"


if __name__ == "__main__":
    socketIO.run(app, host="0.0.0.0", port=5000)
