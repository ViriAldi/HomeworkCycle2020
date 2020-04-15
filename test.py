from PIL import Image
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import pandas


def read_data(path):

    im = Image.open(path)
    imarray = np.array(im)
    imarray = imarray.T

    return imarray


def get_elevation(coord, corner_coord, grid):

    corner_lat, corner_lon = corner_coord
    lat, lon = coord

    ind_lon = int(3 * abs(corner_lon - lon) // 0.00250)
    ind_lat = int(3 * abs(corner_lat - lat) // 0.00250)

    return grid[ind_lon][ind_lat]


def create_plot_data(coord, size, corner_coord, grid):

    # creating arrays with coordinates
    coords_x = np.array([x + 0.00083333 * i 
                for i in range(-size, size + 1)] * (2 * size + 1))
    coords_y = np.array([y + 0.00083333 * i for i in range(-size, size + 1) 
                for j in range(2 * size + 1)])
    coords_z = np.array([get_elevation(t, corner_coord, grid) 
                for t in zip(coords_x, coords_y)])

    # scaling coordinates
    coords_x = coords_x * 120000
    coords_y = coords_y * 100000

    # creating 2D arrays
    coords_x.resize(2 * size + 1, 2 * size + 1)
    coords_y.resize(2 * size + 1, 2 * size + 1)
    coords_z.resize(2 * size + 1, 2 * size + 1)

    return (coords_x, coords_y, coords_z)


def vizualize(plot_data):
    X, Y, Z = plot_data

    ax = plt.axes(projection='3d')
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False, rcount = 500, ccount = 500)

    # Create cubic bounding box to simulate equal aspect ratio
    max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max()
    Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(X.max()+X.min())
    Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(Y.max()+Y.min())
    Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(Z.max()+Z.min())

    for xb, yb, zb in zip(Xb, Yb, Zb):
        ax.plot([xb], [yb], [zb], 'w')

    plt.grid()
    plt.show()


if __name__ == "__main__":
    x, y = [45.976607, 7.658548]
    size = 30
    grid = read_data("geofiles/swizerland.tif")
    plot_data = create_plot_data((x, y), size, (50, 5), grid)

    vizualize(plot_data)
