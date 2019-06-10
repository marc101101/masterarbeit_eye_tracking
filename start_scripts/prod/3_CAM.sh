#!/bin/bash
../../OpenFace/build/bin/FeatureExtraction -q -device 0 -gaze | python3  ../../client/client.py 192.168.188.20 cam_3