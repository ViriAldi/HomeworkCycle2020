from tiff_read.geotiff_reader import GeoTiffReader
import pandas as pd


def save_csv(geo_corner, size):
    reader = GeoTiffReader("../geofiles/swizerland.tif", geo_corner)

    lattice = reader.make_lattice((45.976607, 7.658548), size=size)
    x, y, z = lattice.x_2d, lattice.y_2d, lattice.z_2d

    df = pd.DataFrame(z)
    df.to_csv("../app/static/data_z.csv")

    df = pd.DataFrame(x)
    df.to_csv("../app/static/data_x.csv")

    df = pd.DataFrame(y)
    df.to_csv("../app/static/data_y.csv")

    # points = lattice.path((4, 2), (200, 200))
    # x_p = list(map(lambda p: p.get_x(), points))
    # y_p = list(map(lambda p: p.get_y(), points))
    # z_p = list(map(lambda p: 2 * p.get_z(), points))

