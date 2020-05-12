from tiff_read.geotiff_reader import GeoTiffReader
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

if __name__ == "__main__":
    reader = GeoTiffReader(path="../geofiles/swizerland.tif", geo_corner=(50, 5))

    lattice = reader.make_lattice((45.976607, 7.658548), 5000)
    x, y, z = lattice.x_2d, lattice.y_2d, lattice.z_2d

    plt.figure()
    ax = plt.axes(projection='3d')

    max_range = np.array([x.max() - x.min(), y.max() - y.min(), y.max() - y.min()]).max()
    Xb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][0].flatten() + 0.5 * (x.max() + x.min())
    Yb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][1].flatten() + 0.5 * (y.max() + y.min())
    Zb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][2].flatten() + 0.5 * (z.max() + z.min())

    for xb, yb, zb in zip(Xb, Yb, Zb):
        ax.plot([xb], [yb], [zb], 'w')

    ax.plot_surface(x, y, z, linewidth=0, antialiased=False, color="white", alpha=0.3)
    plt.show()
