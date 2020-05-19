from tiff_read.geotiff_reader import GeoTiffReader
from math import ceil


def to_javascript(coordinates, size):
    reader = GeoTiffReader(coordinates, k=ceil(size/20000))

    lattice = reader.make_lattice(coordinates, size=size)
    x, y, z = lattice.x_2d.tolist(), lattice.y_2d.tolist(), lattice.z_2d.tolist()

    return [x, y, z]


def make_path(point1, point2):
    coordinates = ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)
    size = max(0.75 * max(abs(point2[0] - point1[0]), abs(point2[1] - point1[1])) * 120, 5)

    reader = GeoTiffReader(coord=coordinates, k=ceil(size/8))

    lattice = reader.make_lattice(coordinates, size=size * 1000)
    x, y, z = lattice.x_2d.tolist(), lattice.y_2d.tolist(), lattice.z_2d.tolist()

    point1 = lattice.indexes(point1)
    point2 = lattice.indexes(point2)

    path = lattice.path(point1, point2)
    path_x = [el.get_x() for el in path]
    path_y = [el.get_y() for el in path]
    path_z = [el.get_z() + 30 for el in path]
    path = [path_x, path_y, path_z]

    ans = [[x, y, z], path]

    return ans
