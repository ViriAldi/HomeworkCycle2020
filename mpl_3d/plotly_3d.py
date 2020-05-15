from tiff_read.geotiff_reader import GeoTiffReader
import pandas as pd


def to_javascript(geo_corner, size):
    reader = GeoTiffReader("../geofiles/swizerland.tif", geo_corner)

    lattice = reader.make_lattice((45.976607, 7.658548), size=size)
    x, y, z = lattice.x_2d.tolist(), lattice.y_2d.tolist(), lattice.z_2d.tolist()

    return [x, y, z]
