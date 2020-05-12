from tiff_read.geotiff_reader import GeoTiffReader
import matplotlib.pyplot as plt


if __name__ == "__main__":
    reader = GeoTiffReader(path="geofiles/swizerland.tif", geo_corner=(50, 5))

    lattice = reader.make_lattice((41, 6), 1000)
    x, y, z = lattice.x_2d, lattice.y_2d, lattice.z_2d

    plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_surface(x, y, z, linewidth=0, antialiased=False)
