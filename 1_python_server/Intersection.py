import numpy as np


class Intersection(object):

    def __init__(self, start, direction, aoi):
        self.start = start
        self.direction = self.normalize(direction)
        self.aoi = aoi
        self.distance = self.intersect_plane(self.start, direction, self.aoi.p1, self.normalize(self.aoi.n))
        self.end = self.start + self.distance * self.direction
        self.hit_x = False
        self.hit_y = False
        self.hit_z = False
        self.is_hit = False
        self.hit()

    def hit(self):
        if self.end[0] >= self.aoi.x - 1 and self.end[0] <= self.aoi.x + self.aoi.w + 1:
            self.hit_x = True
        if self.end[1] >= self.aoi.y - 1 and self.end[1] <= self.aoi.y + self.aoi.h + 1:
            self.hit_y = True
        if self.end[2] >= self.aoi.z - 1 and self.end[2] <= self.aoi.z + self.aoi.d + 1:
            self.hit_z = True
        if self.hit_z and self.hit_y and self.hit_x:
            self.is_hit = True
        else:
            self.distance = np.inf
            self.is_hit = False

    def get_target(self):
        return self.start + self.direction * self.distance

    def normalize(self, x):
        return x / np.linalg.norm(x)


    # siehe: https://gist.github.com/rossant/6046463
    def intersect_plane(self, O, D, P, N):
        # Return the distance from O to the intersection of the ray (O, D) with the
        # plane (P, N), or +inf if there is no intersection.
        # O and P are 3D points, D and N (normal) are normalized vectors.
        denom = np.dot(D, N)
        if np.abs(denom).any() < 1e-6:
            return np.inf
        d = np.dot(P - O, N) / denom
        if d < 0:
            return np.inf
        return d
