#!/bin/bash
#sh ./1_download.sh && sh ./2_download.sh && sh ./3_download.sh && sh ./4_download.sh
scp -r pi@192.168.188.23:~/workspace/masterarbeit_eye_tracking/start_scripts/prod/processed /Users/markusguder/Desktop/backup/client_4

scp -r pi@192.168.188.22:~/workspace/masterarbeit_eye_tracking/start_scripts/prod/processed /Users/markusguder/Desktop/backup/client_3

scp -r pi@192.168.188.24:~/workspace/masterarbeit_eye_tracking/start_scripts/prod/processed /Users/markusguder/Desktop/backup/client_2

scp -r pi@192.168.188.21:~/workspace/masterarbeit_eye_tracking/start_scripts/prod/processed /Users/markusguder/Desktop/backup/client_1