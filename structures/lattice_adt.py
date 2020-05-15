from structures.linked_array_data_structure import *
import numpy as np
import heapq


class Lattice:
    def __init__(self, step: tuple, array2d: np.ndarray, center: tuple, step_sec: [float, int] = 3):
        self.step = step
        self.center = center
        self.sec = step_sec
        self._elem = Array2D(*array2d.shape)
        self._construct(array2d)
        self._bind()

    def _construct(self, array2d):
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                coords = (self.center[0] - (row - self.num_rows() / 2) * (self.sec / 3600),
                          self.center[1] + (col - self.num_cols() / 2) * (self.sec / 3600))

                self._elem[row, col] = Node(x=row, y=col,
                                            value=array2d[row, col],
                                            coefficient=self.step,
                                            geo_coord=coords)

    def _bind(self):
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
        return self._elem.__getitem__(item)

    def __setitem__(self, key, value):
        self._elem.__setitem__(key, value)

    def num_rows(self):
        return self._elem.num_rows()

    def num_cols(self):
        return self._elem.num_cols()

    def _attribute_2d(self, attribute):
        ans = np.zeros((self.num_rows(), self.num_cols()))

        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                ans[row][col] = attribute(self[row, col])

        return ans

    @property
    def x_2d(self):
        return self._attribute_2d(Node.get_x)

    @property
    def y_2d(self):
        return self._attribute_2d(Node.get_y)

    @property
    def z_2d(self):
        return self._attribute_2d(Node.get_z)

    @staticmethod
    def neighbours(node):
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

        print(ans)

        return ans

    def path(self, point1, point2):
        first = self[point1[0], point1[1]]
        last = self[point2[0], point2[1]]

        dist = {self[i, j]: 10 ** 9 for i in range(self.num_rows()) for j in range(self.num_cols())}
        parent = {}
        dist[first] = 0

        li = [Pair(dist[x], x) for x in dist]
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
                    dst = node.distance(node_)

                    if dist[node_] > dist[node] + dst:
                        parent[node_] = node
                        dist[node_] = dist[node] + dst
                        heapq.heappush(li, Pair(dist[node_], node_))

        path = []
        node = last
        while node != first:
            path.append(node)
            node = parent[node]
        path.append(node)

        return path

    def indexes(self, coords):
        y = (self.center[0] - coords[0]) * 3600 / 3 + self.num_rows() / 2
        x = (-self.center[1] + coords[1]) * 3600 / 3 + self.num_cols() / 2

        return int(y), int(x)


class Node:
    def __init__(self, x: int, y: int, value: [float, int],
                 geo_coord: tuple = (None, None), coefficient: tuple = (1, 1),
                 directions: [list, tuple] = (None, None, None, None)):

        self._x = x * coefficient[0]
        self._y = y * coefficient[1]
        self._value = value
        self.n, self.e, self.s, self.w = directions
        self.lat, self.lon = geo_coord

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_z(self):
        return self._value

    def __hash__(self):
        return int(self._x ** 3 + self._y ** 3)

    def distance(self, node):
        x1, y1, z1 = self.get_x(), self.get_y(), self.get_z()
        x2, y2, z2 = node.get_x(), node.get_y(), node.get_z()

        return ((x1 - x2)**2 + (y1 - y2)**2 + 10000 * (z1**4 / 2000**4) * (z1 - z2)**2)**0.5


class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __lt__(self, other):
        return self.a < other.a

    def __gt__(self, other):
        return self.a > other.a
