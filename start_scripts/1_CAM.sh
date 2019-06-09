#!/bin/bash
../../OpenFace/build/bin/FeatureExtraction -device 0 -gaze -q | python3  ../client/client.py 192.168.0.191 cam_1