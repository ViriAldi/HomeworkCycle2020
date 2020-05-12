import ctypes


class Array:
    def __init__(self, size):
        if size <= 0:
            raise ValueError

        self._size = size
        py_array_type = ctypes.py_object * size
        self._elements = py_array_type()
        self.clear(None)

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        if index < 0 or index >= self._size:
            raise IndexError

        return self._elements[index]

    def __setitem__(self, index, value):
        if index < 0 or index >= self._size:
            raise IndexError

        self._elements[index] = value

    def clear(self, value):
        for i in range(len(self)):
            self._elements[i] = value

    def __iter__(self):
        return _ArrayIterator(self._elements)


class _ArrayIterator:
    def __init__(self, the_array):
        self._array_ref = the_array
        self._cur_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._cur_index < len(self._array_ref):
            entry = self._array_ref[self._cur_index]
            self._cur_index += 1
            return entry
        else:
            raise StopIteration


class Array2D:
    def __init__(self, num_rows, num_cols):
        self.rows = Array(num_rows)

        for i in range(num_rows):
            self.rows[i] = Array(num_cols)

    def num_rows(self):
        return len(self.rows)

    def num_cols(self):
        return len(self.rows[0])

    def clear(self, value):
        for row in self.rows:
            row.clear(value)

    def __getitem__(self, index_tuple):
        if len(index_tuple) != 2:
            raise ValueError

        row = index_tuple[0]
        col = index_tuple[1]
        if (not 0 <= row < self.num_rows()) or (not 0 <= col < self.num_cols()):
            raise IndexError

        array_1d = self.rows[row]
        return array_1d[col]

    def __setitem__(self, index_tuple, value):
        if len(index_tuple) != 2:
            raise ValueError

        row = index_tuple[0]
        col = index_tuple[1]
        if (not 0 <= row < self.num_rows()) or (not 0 <= col < self.num_cols()):
            raise IndexError

        array_1d = self.rows[row]
        array_1d[col] = value

    def __iter__(self):
        return _ArrayIterator(self.rows)
