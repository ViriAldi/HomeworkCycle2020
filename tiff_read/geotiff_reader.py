from PIL import Image
import numpy as np
from structures.lattice_adt import Lattice, Node
from math import pi, cos, floor, ceil
import os


RADIUS = 6400 * 10**3


class GeoTiffReader:
    def __init__(self, coord, step_sec: [float, int] = 1, k: int = 10):
        img = Image.open(self.find_image(coord))
        self.np_array = np.array(img)
        self.corner = (ceil(coord[0]), floor(coord[1]))
        self.step_sec = step_sec
        self.k = k

    def make_lattice(self, center, size):
        y_center = int((center[1] - self.corner[1]) * 3600 / self.step_sec)
        x_center = int((-center[0] + self.corner[0]) * 3600 / self.step_sec)

        arr = self.np_array[max(x_center - int(self.k * size // self.x_scale()), 0):x_center + int(self.k * size // self.x_scale()):self.k,
                            max(y_center - int(self.k * size // self.y_scale()), 0):y_center + int(self.k * size // self.y_scale()):self.k,
                            ]

        y_0 = max(y_center - int(self.k * size // self.y_scale()), 0) / 3600 + self.corner[1]
        x_0 = -max(x_center - int(self.k * size // self.x_scale()), 0) / 3600 + self.corner[0]

        return Lattice(step=(self.x_scale(), self.y_scale()),
                       array2d=arr,
                       corner=(x_0, y_0),
                       step_sec=self.step_sec,
                       k=self.k)

    def x_scale(self):
        return (RADIUS * 2 * pi / (360 * 3600)) * self.step_sec * self.k

    def y_scale(self):
        return self.x_scale() * cos(self.corner[0] * 2 * pi / 360)

    @staticmethod
    def find_image(coord):
        lat = str(floor(coord[0])).rjust(3, "0")
        lon = str(floor(coord[1])).rjust(3, "0")

        for filename in os.listdir("../geofiles"):
            if f"N{lat}E{lon}" in filename:
                path = f"../geofiles/{filename}"
                break

        return path
