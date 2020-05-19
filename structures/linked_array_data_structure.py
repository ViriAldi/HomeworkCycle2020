import ctypes


class Array:
    """
    Class that represents low-level array data structure
    """
    def __init__(self, size):
        """
        Initializes an array with size
        :param size: int
        """
        if size <= 0:
            raise ValueError

        self._size = size
        py_array_type = ctypes.py_object * size
        self._elements = py_array_type()
        self.clear(None)

    def __len__(self):
        """
        Returns the size of array
        :return: int
        """
        return self._size

    def __getitem__(self, index):
        """
        Returns an item by index
        :param index: int
        :return: object
        """
        if index < 0 or index >= self._size:
            raise IndexError

        return self._elements[index]

    def __setitem__(self, index, value):
        """
        Sets the item by index
        :param index: int
        :param value: object
        :return:
        """
        if index < 0 or index >= self._size:
            raise IndexError

        self._elements[index] = value

    def clear(self, value):
        """
        Fills the array with value
        :param value: object
        :return:
        """
        for i in range(len(self)):
            self._elements[i] = value

    def __iter__(self):
        """
        Returns the iterator for array
        :return: iterator
        """
        return _ArrayIterator(self._elements)


class _ArrayIterator:
    """
    Iterator of 2D array
    """
    def __init__(self, the_array):
        """
        Initializes an iterator with parent array
        :param the_array: Array
        """
        self._array_ref = the_array
        self._cur_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        """
        Returns nex element or raises StopIteration exception
        :return:
        """
        if self._cur_index < len(self._array_ref):
            entry = self._array_ref[self._cur_index]
            self._cur_index += 1
            return entry
        else:
            raise StopIteration


class Array2D:
    """
    Class that represents 2D Array data structure
    """
    def __init__(self, num_rows, num_cols):
        """
        Initializes the 2d array with rows (arrays
        :param num_rows: int
        :param num_cols: int
        """
        self.rows = Array(num_rows)

        for i in range(num_rows):
            self.rows[i] = Array(num_cols)

    def num_rows(self):
        """
        Returns the number of rows
        :return: int
        """
        return len(self.rows)

    def num_cols(self):
        """
        Returns the number of columns
        :return: int
        """
        return len(self.rows[0])

    def clear(self, value):
        """
        Fills the array with value
        :param value: object
        :return:
        """
        for row in self.rows:
            row.clear(value)

    def __getitem__(self, index_tuple):
        """
        Returns the item by position
        :param index_tuple: position (int, int)
        :return:
        """
        if len(index_tuple) != 2:
            raise ValueError

        row = index_tuple[0]
        col = index_tuple[1]
        if (not 0 <= row < self.num_rows()) or (not 0 <= col < self.num_cols()):
            raise IndexError

        array_1d = self.rows[row]
        return array_1d[col]

    def __setitem__(self, index_tuple, value):
        """
        Sets the item by position
        :param index_tuple: position (int, int)
        :param value: object
        :return:
        """
        if len(index_tuple) != 2:
            raise ValueError

        row = index_tuple[0]
        col = index_tuple[1]
        if (not 0 <= row < self.num_rows()) or (not 0 <= col < self.num_cols()):
            raise IndexError

        array_1d = self.rows[row]
        array_1d[col] = value

    def __iter__(self):
        """
        Returns the array iterator for rows
        :return: iterator
        """
        return _ArrayIterator(self.rows)
