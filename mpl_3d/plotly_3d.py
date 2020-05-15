from tiff_read.geotiff_reader import GeoTiffReader
import pandas as pd


def to_javascript(geo_corner, coordinates, size):
    reader = GeoTiffReader("../geofiles/swizerland.tif", geo_corner)

    lattice = reader.make_lattice(coordinates, size=size)
    x, y, z = lattice.x_2d.tolist(), lattice.y_2d.tolist(), lattice.z_2d.tolist()

    return [x, y, z]


def make_path(geo_corner, point1, point2):
    reader = GeoTiffReader("../geofiles/swizerland.tif", geo_corner)

    coordinates = ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)
    size = max(0.75 * max(abs(point2[0] - point1[0]), abs(point2[1] - point1[1])) * 120, 7)

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
