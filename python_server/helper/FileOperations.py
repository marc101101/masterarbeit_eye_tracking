import json
import datetime
import time
import csv

class FileOperations:
    file_name_raw = ''
    header_file_row = ['system_timestamp','frame', 'face_id', 'timestamp', 'confidence', 'success', 'gaze_0_x',
                       'gaze_0_y', 'gaze_0_z', 'gaze_1_x', 'gaze_1_y', 'gaze_1_z', 'gaze_angle_x', 'gaze_angle_y',
                       'pose_Tx', 'pose_Ty', 'pose_Tz', 'pose_Rx', 'pose_Ry', 'pose_Rz']
    _config = {}

    def __init__(self):
        self.read_cam_config()

    def read_cam_config(self):
        #with open('cam_config', 'w') as outfile:
        #    return json.dump(config, outfile)
        config = json.load(open('../config/cam_config.json', 'r'))

    def create_raw_log_file(self):
        self.file_name_raw = 'gaze_raw_' + str(
            datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S')) + '.csv'
        self.write_to_csv(self.header_file_row)

    def write_to_csv(self, row):
        with open('data/' + self.file_name_raw, 'w') as csvFile:
            file_writer = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(row)

    def save_to_raw_log_file(self, data):
        data.insert(0, time.time())
        self.write_to_csv(data)
