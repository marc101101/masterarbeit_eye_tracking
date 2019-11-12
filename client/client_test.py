import socketio

## THIS IS A TEST SCRIPT - WHICH SIMULATES THE CLIENT
sio = socketio.Client()
sio.connect('http://0.0.0.0:5000')

message = {
    "client_id": "cam_1"
}

sio.emit('message', message)