from structures.linked_array_data_structure import *
import numpy as np


class Lattice:
    def __init__(self, step: int, array2d: np.ndarray):
        self.step = step
        self._elem = Array2D(*array2d.shape)
        self._construct(array2d)
        self._bind()

    def _construct(self, array2d):
        for row in range(self._elem.num_rows()):
            for col in range(self._elem.num_cols()):

                self._elem[row, col] = Node(array2d[row, col])

    def _bind(self):
        for row in range(self._elem.num_rows()):
            for col in range(self._elem.num_cols()):
                curr_node = self._elem[row, col]

                if row != 0:
                    curr_node.n = self._elem[row-1, col]
                    self._elem[row+1, col].s = curr_node

                if col != self._elem.num_cols():
                    curr_node.e = self._elem[row, col+1]
                    self._elem[row, col-1].w = curr_node

                if row != self._elem.num_rows():
                    curr_node.s = self._elem[row+1, col]
                    self._elem[row-1, col].n = curr_node

                if col != 0:
                    curr_node.w = self._elem[row, col-1]
                    self._elem[row, col+1].e = curr_node


class Node:
    def __init__(self, value: object, directions: [list, tuple] = (None, None, None, None)):
        self.value = value
        self.n, self.e, self.s, self.w = directions
