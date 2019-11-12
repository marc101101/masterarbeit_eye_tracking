#!/usr/bin/python

from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from GazeDetection import GazeDetection

app = Flask(__name__)
CORS(app)
socketIO = SocketIO(app)
mainClass = GazeDetection()

@socketIO.on('message')
def handle_message(message):
    print('received message: ' + str(message['client_id']))
    parsed_data = mainClass.main_method(message)
    emit_data_object = {
        'raw': message,
        'parsed_data': parsed_data
    }
    emit('event', emit_data_object, broadcast=True)


@app.route('/config', methods=['GET'])
def get_cam_config():
    if request.method == 'GET':
        return mainClass.get_cam_config()
    pass


@app.route('/config', methods=['POST'])
def set_cam_config():
    if request.method == 'POST':
        return mainClass.set_cam_config(request.get_json())
    else:
        return "403"

@app.route('/annotation', methods=['GET'])
def get_annotation_config():
    if request.method == 'GET':
        return mainClass.get_annotation_config()
    pass


@app.route('/annotation', methods=['POST'])
def set_annotation_config():
    if request.method == 'POST':
        return mainClass.set_annotation_config(request.get_json())
    else:
        return "403"

@app.route('/annotate/start', methods=['POST'])
def start_annotate():
    if request.method == 'POST':
        return mainClass.start(request.get_json())

@app.route('/annotate/next', methods=['POST'])
def next_annotate():
    if request.method == 'POST':
        return mainClass.next(request.get_json())

@app.route('/annotate/stop', methods=['POST'])
def stop_annotate():
    if request.method == 'POST':
        return mainClass.stop()

@app.route('/meta/', methods=['POST'])
def meta():
    if request.method == 'POST':
        return mainClass.saveMetaDataOfAnnotation(request.get_json())


if __name__ == "__main__":
    socketIO.run(app, host="0.0.0.0", port=5000)
