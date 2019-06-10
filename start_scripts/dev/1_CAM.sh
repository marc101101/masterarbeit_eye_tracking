#!/bin/bash
../../OpenFace/build/bin/FeatureExtraction -q -device 0 -gaze | python3  ../../client/client.py 192.168.0.191 cam_1