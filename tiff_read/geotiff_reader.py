from PIL import Image
import numpy as np
from structures.lattice_adt import Lattice
from math import pi, sin, cos

RADIUS = 6400 * 10**3


class GeoTiffReader:
    def __init__(self, path, geo_corner, step_sec, k=1):
        img = Image.open(path)
        self.np_array = np.array(img)
        self.corner = geo_corner
        self.step_sec = step_sec
        self.k = k

    def to_lattice(self):
        return Lattice((self.step, self.np_array))

    def x_scale(self):
        return (RADIUS * 2 * pi / (360 * 3600)) * self.step_sec

    def y_scale(self):
