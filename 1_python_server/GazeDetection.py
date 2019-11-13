import math
from Intersection import Intersection
from AOI import AOI
import json
import datetime
import time
import csv
import numpy as np

class GazeDetection:
    file_name_raw = ''
    file_name_annotation = ''
    annotation_state = False
    annotation_test_person_id = None
    annotation_pos = None
    annotation_aoi = None
    header_file_row = []

    header_file_annotation = []
    config = {}
    config_file_name = 'config/cam_config.json'
    header_csv_config_file_name = 'config/header_csv_config.json'

    config_annotation = {}
    config_annotation_file_name = "config/aoi_config.json"

    session_data = []
    
    TRANSFORMED_COORDS_GAZE = 0.0
    TRANSFORMED_GAZES = 0.0

    def __init__(self):
        self.config = self.read_config(self.config_file_name)
        self.config_annotation = self.read_config(self.config_annotation_file_name)
        self.header_file_row = self.read_config(self.header_csv_config_file_name)['raw_header']
        self.header_file_annotation = self.read_config(self.header_csv_config_file_name)['annotation_header']

        self.create_raw_log_file()

    def main_method(self, body):
        self.save_to_raw_log_file(body)

        if(self.annotation_state):
            row = self.map_values(body)
            self.write_to_csv_annotation(row)

        return self.transform_data(body).tolist()

    def prep_aoi(self):
        aois = self.get_aois()

        # Intersektion Ojekte erstellen
        intersections = self.get_all_aois_intersection(self.TRANSFORMED_COORDS_GAZE, self.TRANSFORMED_GAZES, aois)

        # Kürzeste Entfernung für jeden Punkt
        distances = np.array(
            [self.set_closest_intersection_and_get_distance(intersections[i]) for i in range(len(intersections))])

        # Start- und Endpunkte der Blicke (Start = Ende, wenn kein Schnittpunkt => Entfernung INF)
        coords, gaze_end = self.get_gaze_pairs(self.TRANSFORMED_COORDS_GAZE, self.TRANSFORMED_GAZES, distances)

        # coords = np.swapaxes(coords, 0, 1)
        # gaze_end = np.swapaxes(gaze_end, 0, 1)

        #drawClass.plot_vectors_with_image_and_aois(coords, gaze_end, aois, 'Test')

        #for aoi in aois:
            #drawClass.plot_heatmap(aoi, aoi.title)

    # ANNOTATION METHODS ---------------------------------------------------------

    def start(self, test_frame):
        print("start")
        self.annotation_test_person_id = test_frame['test_person_id']
        self.annotation_pos = test_frame['position']
        self.annotation_aoi = test_frame['aoi']
        self.create_log_file(test_frame['test_person_id'])
        self.annotation_state = True
        return json.dumps("success")

    def next(self, test_frame):
        self.annotation_pos = test_frame['position']
        self.annotation_aoi = test_frame['aoi']
        print("next")
        return json.dumps("success")

    def stop(self):
        print("stop")
        self.file_name_annotation = ''
        self.annotation_state = False
        return json.dumps("success")

    def saveMetaDataOfAnnotation(self, meta):
        filename = "annotation/meta/" + str(meta['test_person_id']) + "_meta_" + str(
            datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S')) + '.json'
        with open(filename, 'w') as outfile:
            json.dump(meta, outfile)
            return json.dumps("success")

# FILE OPERATION METHODS ---------------------------------------------------------

    def read_config(self, file_name):
        with open(file_name, encoding='utf-8') as f:
            return json.load(f)

    def create_log_file(self, test_person_id):
        self.file_name_annotation = str(test_person_id) + "_annotation_" + str(
            datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S')) + '.csv'
        self.write_to_csv_annotation(self.header_file_annotation)

    def create_raw_log_file(self):
        self.file_name_raw = 'gaze_raw_' + str(
            datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S')) + '.csv'
        self.write_to_csv(self.header_file_row)

    def write_to_csv(self, row):
        with open('data/' + self.file_name_raw, 'a') as csvFile:
            file_writer = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(row)

    def write_to_csv_annotation(self, row):
        with open('annotation/' + self.file_name_annotation, 'a') as csvFile:
            file_writer = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(row)

    def save_to_raw_log_file(self, data):
        row = self.map_values(data)
        self.write_to_csv(row)

    def map_values(self, data):

        return_row = [
            data["client_id"],
            time.mktime(time.gmtime()),
            data["face_id"],
            data["frame_number"],
            data["landmark_detection_success"],
            data["landmark_detection_confidence"],
            data["gaze_direction_0_x"],
            data["gaze_direction_0_y"],
            data["gaze_direction_0_z"],
            data["gaze_direction_0_x"],
            data["gaze_direction_0_y"],
            data["gaze_direction_0_z"],
            data["gaze_angle_x"],
            data["gaze_angle_y"],
            data["pose_Tx"],
            data["pose_Ty"],
            data["pose_Tz"],
            data["pose_Rx"],
            data["pose_Ry"],
            data["pose_Rz"]
        ]

        number = 0
        while(number <= 55):
            return_row.append(data["eye_lmk_x_" + str(number)])
            number += 1

        number = 0
        while (number <= 55):
            return_row.append(data["eye_lmk_y_" + str(number)])
            number += 1

        number = 0
        while (number <= 55):
            return_row.append(data["eye_lmk_X_" + str(number)])
            number += 1

        number = 0
        while (number <= 55):
            return_row.append(data["eye_lmk_Y_" + str(number)])
            number += 1

        number = 0
        while (number <= 55):
            return_row.append(data["eye_lmk_Z_" + str(number)])
            number += 1

        if(self.annotation_state):
            return_row.insert(1, self.annotation_test_person_id)
            return_row.insert(2, self.annotation_pos)
            return_row.insert(3, self.annotation_aoi)

        return return_row

    def get_cam_config(self):
        try:
            return json.dumps(self.config)
        except Exception as e:
            return json.dumps([])

    def set_cam_config(self, config):
        try:
            with open('config/cam_config.json', 'w') as outfile:
                json.dump(config, outfile)
            self.config = config
            return json.dumps(config)
        except Exception as e:
            return json.dumps([])
    
    def get_annotation_config(self):
        try:
            return json.dumps(self.config_annotation)
        except Exception as e:
            return json.dumps([])

    def set_annotation_config(self, config):
        try:
            with open('config/aoi_config.json', 'w') as outfile:
                json.dump(config, outfile)
            self.config = config
            return json.dumps(config)
        except Exception as e:
            return json.dumps([])

# TRANSFORM COORDINATES METHODS ---------------------------------------------------------

    def transform_data(self, body):
        COORDS_GAZE = np.array([body['eye_lmk_X_0'], body['eye_lmk_Y_0'], body['eye_lmk_Z_0']])
        GAZES = np.array([body['gaze_direction_0_x'], body['gaze_direction_0_y'], body['gaze_direction_0_z']])

        coords = COORDS_GAZE
        directions = GAZES
        client_id = body['client_id']

        # normierte Blickrichtung auf Startkoordinaten addieren
        #gaze_ends = np.swapaxes(np.swapaxes(coords, 0, 1) + np.swapaxes(directions, 0, 1), 0, 1)
        gaze_ends = coords + directions

        # transformieren
        self.TRANSFORMED_COORDS_GAZE = self.apply_transformation(client_id, COORDS_GAZE, swap=False)
        gaze_ends = self.apply_transformation(client_id, gaze_ends, swap=False)

        # Blickrichtung zurückrechnen und normalisieren
        directions = gaze_ends - self.TRANSFORMED_COORDS_GAZE
        self.TRANSFORMED_GAZES = np.array([self.normalize(directions[i]) for i in range(len(directions))])

        return self.TRANSFORMED_GAZES

    def get_transformation_matrix(self, client_id):
        rot_x = self.rotate_x(math.radians(self.config[client_id]['rot_x']))
        rot_y = self.rotate_y(math.radians(self.config[client_id]['rot_y']))
        rot_z = self.rotate_z(math.radians(self.config[client_id]['rot_z']))

        s_x = self.scale_x(self.config[client_id]['s_x'])
        s_y = self.scale_y(self.config[client_id]['s_y'])
        s_z = self.scale_z(self.config[client_id]['s_z'])

        d = self.translate(self.config[client_id]['t_x'],
                           self.config[client_id]['t_y'],
                           self.config[client_id]['t_z'])

        rot_ax = self.rotate_y(math.radians(-90))
        swap_ax = self.scale_x(-1)

        return swap_ax @ rot_ax @ d @ s_z @ s_y @ s_x @ rot_z @ rot_x @ rot_y

    def apply_transformation(self, client_id, x, swap=True):
        tr = self.get_transformation_matrix(client_id)

        #x = np.swapaxes(x, 0, 1)

        x = np.insert(x, 3, 1, axis=0)
        # Transponieren weil matrix vorne stehen muss
        x = x @ tr.T

        x = np.delete(x, 3, axis=0)
        if swap:
            #return np.swapaxes(x, 0, 1)
            return x
        else:
            return x

# HELPER METHODS ----------------------------------------------------------------

    def normalize(self, x):
        retVal = x / np.linalg.norm(x)
        if math.isnan(retVal):
            return 0
        else:
            return retVal

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

# AOI METHODS -------------------------------------------------------------------

    def get_aois(self):
        return self.config_annotation

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
        #return np.array(
            #[self.get_single_aois_intersection(start_points[i], directions[i], aois) for i in range(len(start_points))])
        return np.array([Intersection(start_points, directions, aoi) for aoi in aois])

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
