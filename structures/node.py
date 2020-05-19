class Node:
    """
    Class that represents a point of lattice
    aka the point of Earth's surface
    """
    def __init__(self, x: int, y: int,
                 value: [float, int], coefficient: tuple = (1, 1),
                 directions: [list, tuple] = (None, None, None, None)):
        """
        Initializes Node with physical measures x, y and
        value using coefficient. Also adds directions
        :param x: int x pos
        :param y: int y pos
        :param value: float, int
        :param coefficient: scaling coefficients for x and y
        :param directions: neighbour vertices
        """

        self._x = x * coefficient[0]
        self._y = y * coefficient[1]
        self._value = value
        self.n, self.e, self.s, self.w = directions

    def get_x(self):
        """
        Getter for x
        :return: float
        """
        return self._x

    def get_y(self):
        """
        Getter for y
        :return: float
        """
        return self._y

    def get_z(self):
        """
        Getter for z (value)
        :return: float
        """
        return self._value

    def __hash__(self):
        """
        Computes a hash for object
        :return: int
        """
        return int(self._x ** 3 + self._y ** 3)

    def distance(self, node,
                 scale: [int, float] = 1000,
                 power_delta: [int, float] = 2.05,
                 power_absolute: [int, float] = 4,
                 min_z: [int, float] = 2000,
                 fixer: [int, float] = 1000):
        """
        Distance function of two Nodes.
        Penalizes the height
        :param node: Second Node
        :param scale: scaling z
        :param power_delta: powering z gradient
        :param power_absolute: powering z value
        :param min_z: min z for powering value
        :param fixer: fixer for powering value
        :return:
        """
        x1, y1, z1 = self.get_x(), self.get_y(), self.get_z()
        x2, y2, z2 = node.get_x(), node.get_y(), node.get_z()

        return ((x1 - x2)**2 + (y1 - y2)**2 +
                scale * ((z1 + fixer) / min_z)**power_absolute
                * abs(z1 - z2)**power_delta)**0.5
