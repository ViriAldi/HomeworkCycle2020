from tiff_read.geotiff_reader import GeoTiffReader
import matplotlib.pyplot as plt
import numpy as np
import random
from mpl_toolkits import mplot3d


def save_vis(geo_corner):
    reader = GeoTiffReader("../geofiles/swizerland.tif", geo_corner)

    lattice = reader.make_lattice((45.976607, 7.658548), 10000)
    x, y, z = lattice.x_2d, lattice.y_2d, lattice.z_2d

    points = lattice.path((4, 2), (200, 200))
    x_p = list(map(lambda p: p.get_x(), points))
    y_p = list(map(lambda p: p.get_y(), points))
    z_p = list(map(lambda p: 2 * p.get_z(), points))

    plt.figure()
    ax = plt.axes(projection='3d')

    max_range = np.array([x.max() - x.min(), y.max() - y.min(), y.max() - y.min()]).max()
    Xb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][0].flatten() + 0.5 * (x.max() + x.min())
    Yb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][1].flatten() + 0.5 * (y.max() + y.min())
    Zb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][2].flatten() + 0.5 * (z.max() + z.min())

    for xb, yb, zb in zip(Xb, Yb, Zb):
        ax.plot([xb], [yb], [zb], 'w')

    ax.plot_surface(x, y, z, linewidth=0, antialiased=False, color="white", alpha=0.3)
    ax.plot(x_p, y_p, z_p, color="red")
    name = hex(random.randint(10**5, 10**10))[2:]
    plt.savefig(name, dpi=300)
    return name
