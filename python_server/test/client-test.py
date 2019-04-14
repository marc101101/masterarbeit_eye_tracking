import socketio

# standard Python
sio = socketio.Client()

sio.connect('http://localhost:5000')

test_data = {
    "client_id": "cam_1",
    "frame": 0,
    "face_id": 0,
    "timestamp": 0,
    "confidence": 0,
    "success": 0,
    "gaze_0_x": 0,
    "gaze_0_y": 0,
    "gaze_0_z": 0,
    "gaze_1_x": 0,
    "gaze_1_y": 0,
    "gaze_1_z": 0,
    "gaze_angle_x": 0,
    "gaze_angle_y": 0,
    "pose_Tx": 0,
    "pose_Ty": 0,
    "pose_Tz": 0,
    "pose_Rx": 0,
    "pose_Ry": 0,
    "pose_Rz": 0,
    "eye_lmk_X_0": 0,
    "eye_lmk_Y_0": 0,
    "eye_lmk_Z_0": 0,
    "eye_lmk_X_1": 0,
    "eye_lmk_Y_1": 0,
    "eye_lmk_Z_1": 0
}

sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)
sio.emit('message', test_data)

print("test")
