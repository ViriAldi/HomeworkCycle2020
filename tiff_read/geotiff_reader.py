from PIL import Image
import numpy as np
from structures.lattice_adt import Lattice, Node
from math import pi, cos

RADIUS = 6400 * 10**3


class GeoTiffReader:
    def __init__(self, path: str, geo_corner: tuple, step_sec: [float, int] = 3, k: int = 1):
        img = Image.open(path)
        self.np_array = np.array(img)
        self.corner = geo_corner
        self.step_sec = step_sec
        self.k = k

    def make_lattice(self, center, size):
        x_center = int((center[1] - self.corner[1]) * 3600 / self.step_sec)
        y_center = int((-center[0] + self.corner[0]) * 3600 / self.step_sec)

        arr = self.np_array[y_center - int(size // self.y_scale()):y_center + int(size // self.y_scale()),
                            x_center - int(size // self.x_scale()):x_center + int(size // self.x_scale()),
                            ]

        return Lattice(step=(self.x_scale(), self.y_scale()),
                       array2d=arr,
                       center=center)

    def x_scale(self):
        return (RADIUS * 2 * pi / (360 * 3600)) * self.step_sec

    def y_scale(self):
        return self.x_scale() * cos(self.corner[0])
