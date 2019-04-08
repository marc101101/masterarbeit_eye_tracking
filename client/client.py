#!/usr/bin/python
import sys
import requests
import json


class Client:

    ip_address = ""
    client_name = ""

    def __init__(self, ip_address, client_name):
        self.ip_address = ip_address
        self.client_name = client_name
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
                        #if (len(frame_to_push) >= 23):
                            #print("Message received: " + str(frame_to_push))
                        try:
                            print("Message received: " + str(buff))
                            # outlet.push_sample(frame_to_push)
                            # self.push_to_server(frame_to_push)
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

    def push_to_server(self, frame_to_push):
        url = "http://" + str(self.ip_address) + ":5000/gazeDetection"

        headers = {
            'Content-Type': "application/json"
        }

        response = requests.request("POST",
                                    url,
                                    data=json.dumps(self.format_frame_to_push(frame_to_push)),
                                    headers=headers)

        print(response.text)

    def format_frame_to_push(self, frame_to_push):
        return {
            "client_id": self.client_name,
            "frame": float(frame_to_push[0]),
            "face_id": float(frame_to_push[1]),
            "timestamp": float(frame_to_push[2]),
            "confidence": float(frame_to_push[3]),
            "success": float(frame_to_push[4]),
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
            "eye_lmk_Z_0": float(frame_to_push[21])
        }


if __name__ == "__main__":
    print("INFO: Client  up and tracking")
    print("INFO: IP address - " + str(sys.argv[1]))
    print("INFO: Client name - " + str(sys.argv[2]))

    client = Client(sys.argv[1], sys.argv[2])

