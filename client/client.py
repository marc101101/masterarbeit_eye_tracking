#!/usr/bin/python
import sys
import socketio


class ClientGazeLogger:

    client_name = ""
    sio = None

    def __init__(self, ip_address, client_name):
        self.client_name = client_name
        sio = socketio.Client()
        sio.connect('http://' + ip_address + ':5000')

        self.watch_data_stream()

    def watch_data_stream(self):
        k = 0

        try:
            buff = ''
            while True:
                buff += sys.stdin.read(1)
                if buff.startswith("relevant_entry"):
                    if buff.endswith('\n'):
                        print("Message received: " + str(buff))
                        frame_to_push = buff[:-1].split(",")
                        frame_to_push.pop(0)
                        counter = 0
                        for i in frame_to_push:
                            try:
                                frame_to_push[counter] = float(i)
                                pass
                            except Exception as e:
                                frame_to_push[counter] = 0
                                raise e

                            counter = counter + 1
                        try:
                            print("Message received: " + str(buff))
                            self.push_to_server(frame_to_push)
                        except Exception as e:
                            print(e)
                        buff = ''
                        k = k + 1
                else:
                    if buff.endswith('\n'):
                        print(buff[:-1])
                        buff = ''

        except KeyboardInterrupt:
            sys.stdout.flush()
            pass
        print("End of Log: " + str(k))

    def push_to_server(self, message):
        self.sio.emit('message', self.format_frame_to_push(message))

    def format_frame_to_push(self, frame_to_push):
        return {
            "client_id": self.client_name,
            "face_id": float(frame_to_push[0]),
            "frame": float(frame_to_push[1]),
            "timestamp": float(frame_to_push[2]),
            "success": float(frame_to_push[3]),
            "confidence": float(frame_to_push[4]),
            "gaze_0_x": float(frame_to_push[5]),
            "gaze_0_y": float(frame_to_push[6]),
            "gaze_0_z": float(frame_to_push[7]),
            "gaze_1_x": float(frame_to_push[8]),
            "gaze_1_y": float(frame_to_push[9]),
            "gaze_1_z": float(frame_to_push[10]),
            "gaze_angle_x": float(frame_to_push[11]),
            "gaze_angle_y": float(frame_to_push[12]),
            "pose_Tx": float(frame_to_push[13]),
            "pose_Ty": float(frame_to_push[14]),
            "pose_Tz": float(frame_to_push[15]),
            "pose_Rx": float(frame_to_push[16]),
            "pose_Ry": float(frame_to_push[17]),
            "pose_Rz": float(frame_to_push[18]),
            "eye_lmk_X_0": float(frame_to_push[19]),
            "eye_lmk_Y_0": float(frame_to_push[20]),
            "eye_lmk_Z_0": float(frame_to_push[21]),
            "eye_lmk_X_1": float(frame_to_push[22]),
            "eye_lmk_Y_1": float(frame_to_push[23]),
            "eye_lmk_Z_1": float(frame_to_push[24])
        }

    # Openface Logging: OpenFace/lib/local/Utilities/src/RecorderOpenFace.cpp
    # std::cout << "relevant_entry" << ","
    # << face_id << ", "
    # << frame_number << ", "
    # << timestamp << ", "
    # << landmark_detection_success << ", "
    # << landmark_detection_confidence << ", "
    # << gaze_direction0.x << ", "
    # << gaze_direction0.y << ", "
    # << gaze_direction0.z << ", "
    # << gaze_direction1.x << ", "
    # << gaze_direction1.y << ", "
    # << gaze_direction1.z << ", "
    # << gaze_angle[0] << ", "
    # << gaze_angle[1] << ", "
    # << head_pose[0] << ", "
    # << head_pose[1] << ", "
    # << head_pose[2] << ", "
    # << head_pose[3] << ", "
    # << head_pose[4] << ", "
    # << head_pose[5] << ", "
    # << eye_landmarks3D[0] << ", "
    # << eye_landmarks3D[55] << ", "
    # << eye_landmarks3D[110] << ", "
    # << eye_landmarks3D[1] << ", "
    # << eye_landmarks3D[56] << ", "
    # << eye_landmarks3D[111] << std::endl;


if __name__ == "__main__":
    print("INFO: Client  up and tracking")
    print("INFO: IP address - " + str(sys.argv[1]))
    print("INFO: Client name - " + str(sys.argv[2]))

    client = ClientGazeLogger(sys.argv[1], sys.argv[2])

