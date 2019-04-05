from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
from GazeDetection import GazeDetection


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
mainClass = GazeDetection()


@app.route("/gazeDetection", methods=['POST'])
def gaze_detection():
    if request.method == 'POST':
        return mainClass.main_method(request.get_json())
    else:
        return "403"


@app.route("/config", methods=['GET'])
def get_config():
    if request.method == 'GET':
        return mainClass.get_cam_config(request.args.get('clientId'))
    else:
        return "403"

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
