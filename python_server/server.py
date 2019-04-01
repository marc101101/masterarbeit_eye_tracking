from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
from GazeDetection import GazeDetection

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

gaze_detection = GazeDetection()

@app.route("/gazeDetection", methods=['POST'])
def gazeDetection():
    if request.method == 'POST':
        return gaze_detection.main_method(request.get_json())
    else:
        return "403"

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)