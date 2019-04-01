import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd

import csv


class MyHandler(FileSystemEventHandler):

    old_last_frame = 0

    def on_modified(self, event):
        with open('test_data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            print(list(csv_reader)[-1])

            current_last_frame = float(list(csv_reader)[-1][0])

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()