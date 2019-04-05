#!/usr/bin/python

import time
import csv
import sys

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pylsl import StreamInfo, StreamOutlet

class MyHandler(FileSystemEventHandler, file_to_watch, client_name):
    old_last_frame = 0
    info = StreamInfo(client_name, 'FD', 19, 100, 'float32', 'gum11127_Openface')
    outlet = StreamOutlet(info)

    def on_modified(self, event):
        with open(file_to_watch) as csv_file:

            csv_reader = list(csv.reader(csv_file, delimiter=','))
            csv_reader.reverse()
            current_last_frame = float(csv_reader[0][0])
            csv_reader.remove(csv_reader[-1])
            if (self.old_last_frame < current_last_frame):
                diff_old_current = int(self.old_last_frame - current_last_frame) * -1
                for x in range(0, diff_old_current):
                    try:
                        frame_to_push = csv_reader[x]
                        frame_to_push = self.format_frame_to_push(frame_to_push)
                        print(frame_to_push)
                        self.outlet.push_sample(frame_to_push)
                        print("Pushed_frame: " + str(frame_to_push[0]))
                    except Exception as e:
                        print(e)
                        break

                self.old_last_frame = current_last_frame
            else:
                print("INFO: Nothing changed")

    def format_frame_to_push(self, frame_to_push):
        frame_to_push = [
            float(frame_to_push[0]),  # frame
            float(frame_to_push[1]),  # face_id
            float(frame_to_push[2]),  # timestamp
            float(frame_to_push[3]),  # confidence
            float(frame_to_push[4]),  # success
            float(frame_to_push[5]),  # gaze_0_x
            float(frame_to_push[6]),  # gaze_0_y
            float(frame_to_push[7]),  # gaze_0_z
            float(frame_to_push[8]),  # gaze_1_x
            float(frame_to_push[9]),  # gaze_1_y
            float(frame_to_push[10]),  # gaze_1_z
            float(frame_to_push[11]),  # gaze_angle_x
            float(frame_to_push[12]),  # gaze_angle_y
            float(frame_to_push[293]),  # pose_Tx
            float(frame_to_push[294]),  # pose_Ty
            float(frame_to_push[295]),  # pose_Tz
            float(frame_to_push[296]),  # pose_Rx
            float(frame_to_push[297]),  # pose_Ry
            float(frame_to_push[298])  # pose_Rz

        ]
        return frame_to_push


if __name__ == "__main__":
    print(sys.argv)
    event_handler = MyHandler(sys.argv[0], sys.argv[1])
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    print("INFO: Observer up and tracking")
    print("INFO: File to watch" + str(sys.argv[0]))
    print("INFO: Client name" + str(sys.argv[1]))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
