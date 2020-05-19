from structures.linked_array_data_structure import *
import numpy as np
import heapq
from structures.node import Node


class Lattice:
    """
    Class that represents Lattice Data Structure
    """
    def __init__(self, step: tuple, array2d: np.ndarray, corner: tuple, step_sec: [float, int] = 1, k: int = 1):
        """
        Initializes the lattice
        :param step: x and y scaling (float, float)
        :param array2d: Array2D
        :param corner: Top left corner (lat, long)
        :param step_sec: step between points in arc seconds
        :param k: scaling for performance
        """
        self.step = step
        self.corner = corner
        self.sec = step_sec
        self.k = k
        self._elem = Array2D(*array2d.shape)
        self._construct(array2d)
        self._bind()

    def _construct(self, array2d):
        """
        Fills Lattice with Node objects
        :param array2d: Array2D
        :return:
        """
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):

                self._elem[row, col] = Node(x=row, y=col,
                                            value=array2d[row, col],
                                            coefficient=self.step)

    def _bind(self):
        """
        Binds nodes in Lattice (north, east, south, west)
        :return:
        """
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                curr_node = self[row, col]

                if row != 0:
                    curr_node.n = self[row-1, col]
                    self[row-1, col].s = curr_node

                if col != self.num_cols() - 1:
                    curr_node.e = self[row, col+1]
                    self[row, col+1].w = curr_node

                if row != self.num_rows() - 1:
                    curr_node.s = self[row+1, col]
                    self[row+1, col].n = curr_node

                if col != 0:
                    curr_node.w = self[row, col-1]
                    self[row, col-1].e = curr_node

    def __getitem__(self, item):
        """
        Returns the item by position
        :param item: position (int, int)
        :return: object
        """
        return self._elem.__getitem__(item)

    def __setitem__(self, key, value):
        """
        Sets the value bu position
        :param key: position (int, int)
        :param value: object
        :return:
        """
        self._elem.__setitem__(key, value)

    def num_rows(self):
        """
        Returns the number of rows
        :return: int
        """
        return self._elem.num_rows()

    def num_cols(self):
        """
        Returns the number of columns
        :return: int
        """
        return self._elem.num_cols()

    def _attribute_2d(self, attribute):
        """
        Returns numpy 2d array with given attribute taken from lattice
        :param attribute:
        :return:
        """
        ans = np.zeros((self.num_rows(), self.num_cols()))

        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                ans[row][col] = attribute(self[row, col])

        return ans

    @property
    def x_2d(self):
        """
        X attribute subarray
        :return: numpy.ndarray
        """
        return self._attribute_2d(Node.get_x)

    @property
    def y_2d(self):
        """
        Y attribute subarray
        :return: numpy.ndarray
        """
        return self._attribute_2d(Node.get_y)

    @property
    def z_2d(self):
        """
        Z attribute subarray
        :return: numpy.ndarray
        """
        return self._attribute_2d(Node.get_z)

    @staticmethod
    def neighbours(node):
        """
        Computes all diagonal neighbours of the node
        :param node: Node
        :return: list
        """
        ans = []

        if node.n and node.e:
            ans.append(node.n.e)
        else:
            ans.append(None)

        if node.e and node.s:
            ans.append(node.e.s)
        else:
            ans.append(None)

        if node.s and node.w:
            ans.append(node.s.w)
        else:
            ans.append(None)

        if node.w and node.n:
            ans.append(node.w.n)
        else:
            ans.append(None)

        return ans

    def path(self, point1, point2, kernel=Node.distance):
        """
        Finds the shortest path between two points of Lattice
        For distance measurement uses kernel function of two nodes
        By default it is distance function that penalizes height
        Uses Dejkstra Algorithm with priority queue. Complexity O(mlogn)
        :param point1: Node
        :param point2: Node
        :param kernel: function(Node, Node)
        :return: list of nodes
        """
        first = self[point1[0], point1[1]]
        last = self[point2[0], point2[1]]

        dist = {self[i, j]: 10 ** 9
                for i in range(self.num_rows())
                for j in range(self.num_cols())}

        parent = {}
        dist[first] = 0

        li = [_Pair(dist[x], x) for x in dist]
        heapq.heapify(li)

        while li:
            node = heapq.heappop(li)
            if node.a != dist[node.b]:
                continue

            node = node.b
            if node == last:
                break

            for node_ in [node.n, node.e, node.s, node.w] + self.neighbours(node):
                if node_:
                    dst = kernel(node, node_)

                    if dist[node_] > dist[node] + dst:
                        parent[node_] = node
                        dist[node_] = dist[node] + dst
                        heapq.heappush(li, _Pair(dist[node_], node_))

        path = []
        node = last
        while node != first:
            path.append(node)
            node = parent[node]
        path.append(node)

        return path

    def indexes(self, coords):
        """
        Return position of point on lattice by coordinates
        :param coords: (lat, long)
        :return: position (int, int)
        """
        y = (-coords[0] + self.corner[0]) * 3600 \
            / (self.sec * self.k)
        x = (coords[1] - self.corner[1]) * 3600 \
            / (self.sec * self.k)

        return int(y), int(x)


class _Pair:
    """
    Class of C++ pair representation
    """
    def __init__(self, a, b):
        """
        Initializes a pair with values a and b
        :param a:
        :param b:
        """
        self.a = a
        self.b = b

    def __lt__(self, other):
        """
        Compares two pairs by first element
        :param other:
        :return:
        """
        return self.a < other.a

    def __gt__(self, other):
        """
        Compares twp pairs by first element
        :param other:
        :return:
        """
        return self.a > other.a
