from structures.linked_array_data_structure import *
import numpy as np


class Lattice:
    def __init__(self, step: int, array2d: np.ndarray):
        self.step = step
        self._elem = Array2D(*array2d.shape)
        self._construct(array2d)
        self._bind()

    def _construct(self, array2d):
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):

                self._elem[row, col] = Node(x=row, y=col,
                                            value=array2d[row, col],
                                            coefficient=self.step)

    def _bind(self):
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                curr_node = self[row, col]

                if row != 0:
                    curr_node.n = self[row-1, col]
                    self[row+1, col].s = curr_node

                if col != self.num_cols():
                    curr_node.e = self[row, col+1]
                    self[row, col-1].w = curr_node

                if row != self.num_rows():
                    curr_node.s = self[row+1, col]
                    self[row-1, col].n = curr_node

                if col != 0:
                    curr_node.w = self[row, col-1]
                    self[row, col+1].e = curr_node

    def __getitem__(self, item):
        return self._elem.__getitem__(item)

    def __setitem__(self, key, value):
        self._elem.__setitem__(key, value)

    def num_rows(self):
        return self._elem.num_rows()

    def num_cols(self):
        return self._elem.num_cols()


class Node:
    def __init__(self, x: int, y: int,
                 value: object, coefficient: int = 1,
                 directions: [list, tuple] = (None, None, None, None)):

        self.x = x * coefficient
        self.y = y * coefficient
        self.value = value
        self.n, self.e, self.s, self.w = directions
