import numpy as np
import math
import Intersection
import AOI
import json
import datetime
import time
import csv

import matplotlib.pyplot as plt
import numpy as np

from DrawCurrentData import DrawCurrentData

drawClass = DrawCurrentData()


class GazeDetection:
    file_name_raw = ''
    header_file_row = ['client_id', 'system_timestamp', 'frame', 'face_id', 'timestamp', 'confidence', 'success', 'gaze_0_x',
                       'gaze_0_y', 'gaze_0_z', 'gaze_1_x', 'gaze_1_y', 'gaze_1_z', 'gaze_angle_x', 'gaze_angle_y',
                       'pose_Tx', 'pose_Ty', 'pose_Tz', 'pose_Rx', 'pose_Ry', 'pose_Rz']
    config = {}
    config_file_name = 'config/cam_config.json'

    def __init__(self):
        self.read_cam_config()
        self.create_raw_log_file()

    def main_method(self, body):
        if self.valid_body(body):
            self.save_to_raw_log_file(body)
            self.transform_data(body)
        else:
            return "500"

    def read_cam_config(self):
        with open(self.config_file_name, 'r') as f:
            self.config = json.load(f)

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

    def get_cam_config(self, client_id):
        try:
            return json.dumps(self.config[client_id])
        except Exception as e:
            return json.dumps([])

    def transform_data(self, body):
        coords = []
        directions = []
        # normierte Blickrichtung auf Startkoordinaten addieren
        gaze_ends = np.swapaxes(np.swapaxes(coords, 0, 1) + np.swapaxes(directions, 0, 1), 0, 1)
        # transformieren
        TRANSFORMED_COORDS_GAZE = self.apply_transfromation(body, swap=False)
        gaze_ends = self.apply_transfromation(gaze_ends, swap=False)
        # Blickrichtung zurückrechnen und normalisieren
        directions = gaze_ends - TRANSFORMED_COORDS_GAZE
        TRANSFORMED_GAZES = np.array([self.normalize(directions[i]) for i in range(len(directions))])

    def valid_body(self, body):
        if len(body) >= 18:
            return True
        else:
            return False

    def get_transformation_matrix(self):
        rot_x = self.rotate_x(math.radians(-8))
        rot_y = self.rotate_y(math.radians(21))
        rot_z = self.rotate_z(math.radians(11))

        s_x = self.scale_x(0.4)
        s_y = self.scale_y(0.4)
        s_z = self.scale_z(0.4)

        d = self.translate(200, 400, 25)

        rot_ax = self.rotate_y(math.radians(-90))
        swap_ax = self.scale_x(-1)

        return swap_ax @ rot_ax @ d @ s_z @ s_y @ s_x @ rot_z @ rot_x @ rot_y

    def get_aois(self):
        schrank_oben = AOI([0, 330, 75], [800, 330, 75], [0, 496, 75], 'orange', 'Schrank oben')
        wand = AOI([0, 330, 1], [0, 200, 1], [800, 330, 1], 'blue', 'Wand zwischen Schränken')
        schrank_unten = AOI([0, 200, 156], [800, 200, 156], [0, 0, 156], 'white', 'Schrank unten')
        af = AOI([0, 200, 0], [800, 200, 0], [0, 200, 156], 'green', 'Arbeitsfläche')
        ks = AOI([800, 0, 156], [935, 0, 156], [800, 496, 156], 'cyan', 'Kühlschrank')

        return [schrank_oben, wand, schrank_unten, ks, af]

    def normalize(self, x):
        return x / np.linalg.norm(x)

    def apply_transformation(self, x, swap=True):
        tr = self.get_transformation_matrix()

        x = np.swapaxes(x, 0, 1)

        x = np.insert(x, 3, 1, axis=1)
        x = x @ tr.T

        x = np.delete(x, 3, axis=1)
        if swap:
            return np.swapaxes(x, 0, 1)
        else:
            return x

    def translate(self, x, y, z):
        return np.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ])

    def rotate_x(self, phi):
        return np.array([
            [1, 0, 0, 0],
            [0, math.cos(phi), -math.sin(phi), 0],
            [0, math.sin(phi), math.cos(phi), 0],
            [0, 0, 0, 1]
        ])

    def rotate_y(self, phi):
        return np.array([
            [math.cos(phi), 0, math.sin(phi), 0],
            [0, 1, 0, 0],
            [-math.sin(phi), 0, math.cos(phi), 0],
            [0, 0, 0, 1]
        ])

    def rotate_z(self, phi):
        return np.array([
            [math.cos(phi), -math.sin(phi), 0, 0],
            [math.sin(phi), math.cos(phi), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def scale_x(self, factor):
        return np.array([
            [factor, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def scale_y(self, factor):
        return np.array([
            [1, 0, 0, 0],
            [0, factor, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def scale_z(self, factor):
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, factor, 0],
            [0, 0, 0, 1]
        ])

    def aoi_to_point_and_normal(self, aoi):
        return aoi.p1, self.normalize(aoi.n)

    def aois_to_point_and_normal(self, aois):
        return np.array([self.aoi_to_point_and_normal(aoi) for aoi in aois])

    def intersect_aoi(self, start, direction, aoi):
        return self.intersect_plane(start, self.normalize(direction), aoi.p1, self.normalize(aoi.n))

    def intersect_aois(self, start, direction, aois):
        return np.array(
            [self.intersect_plane(start, self.normalize(direction), aoi.p1, self.normalize(aoi.n)) for aoi in aois])

    def get_distances_to_aois(self, start_points, direction_vectors, aois):
        return np.array([self.intersect_aois(start_points[i], direction_vectors[i], aois) for i in range(len(start_points))])

    def get_intersection_point(self, start, direction, distance):
        if distance < np.inf:
            return np.array(start + self.normalize(direction) * distance)
        else:
            return start

    def get_single_aoi_intersection(self, start, direction, aoi):
        return Intersection(start, direction, aoi)

    def get_single_aois_intersection(self, start, direction, aois):
        return np.array([Intersection(start, direction, aoi) for aoi in aois])

    def get_all_aois_intersection(self, start_points, directions, aois):
        return np.array(
            [self.get_single_aois_intersection(start_points[i], directions[i], aois) for i in range(len(start_points))])

    def set_closest_intersection_and_get_distance(self, intersections):
        closest = min(intersections, key=lambda x: x.distance)
        if closest.distance < np.inf:
            closest.aoi.points.append(closest.get_target())
        return closest.distance

    def get_gaze_pairs(self, coords, directions, distances):
        start_list = []
        end_list = []
        for i in range(len(coords)):
            if distances[i] < np.inf:
                start_list.append(coords[i])
                end_list.append(coords[i] + self.normalize(directions[i]) * distances[i])
        return np.array(start_list), np.array(end_list)

    # siehe: https://gist.github.com/rossant/6046463
    def intersect_plane(self, O, D, P, N):
        # Return the distance from O to the intersection of the ray (O, D) with the
        # plane (P, N), or +inf if there is no intersection.
        # O and P are 3D points, D and N (normal) are normalized vectors.
        denom = np.dot(D, N)
        if np.abs(denom) < 1e-6:
           return np.inf
        d = np.dot(P - O, N) / denom
        if d < 0:
            return np.inf
        return d

    def is_not_used(self):
        pass
