#! /usr/bin/env python3.3
import sys
import itertools


class MinHeap(object):
    """Docstring for MinHeap """

    def __init__(self):
        """@todo: to be defined """
        self.heap = [None]
        self.heap_size = 0

    @staticmethod
    def parent(index):
        """@todo: Docstring for parent

        :index: @todo
        :returns: @todo

        """
        return index // 2

    @staticmethod
    def left_child(index):
        """@todo: Docstring for left_child

        :index: @todo
        :returns: @todo

        """
        return index << 1

    @staticmethod
    def right_child(index):
        """@todo: Docstring for right_child

        :index: @todo
        :returns: @todo

        """
        return (index << 1) + 1

    def min_heapify(self, i):
        """@todo: Docstring for min_heapify

        :i: @todo
        :returns: @todo

        """
        l = MinHeap.left_child(i)
        r = MinHeap.right_child(i)
        min_i = i

        if (l <= self.heap_size) and (self.heap[l] < self.heap[i]):
            min_i = l
        if (r <= self.heap_size) and (self.heap[r] < self.heap[min_i]):
            min_i = r
        if min_i != i:
            self.heap[i], self.heap[min_i] = self.heap[min_i], self.heap[i]
            self.min_heapify(min_i)

    def build_min_heap(self, arr):
        """@todo: Docstring for build_min_heap

        :arr: @todo
        :returns: @todo

        """
        size = len(arr)
        self.heap = [None] + arr
        self.heap_size = size
        for i in range(size // 2, 0, -1):
            self.min_heapify(i)

    def get_min(self):
        if self.heap_size < 1:
            return None
        else:
            return self.heap[1]

    def extract_min(self):
        if self.heap_size < 1:
            return None
        min_node = self.heap[1]
        self.heap[1] = self.heap[self.heap_size]
        self.heap_size -= 1
        self.min_heapify(1)
        return min_node


class GridEntry(object):
    """Docstring for GridEntry """

    def __init__(self, x, y, value):
        """@todo: to be defined

        :x: @todo
        :y: @todo
        :value: @todo

        """
        self.x = x
        self.y = y
        self.value = value
        self.candidates = []

    def get_x(self):
        """@todo: Docstring for get_x
        :returns: @todo

        """
        return self.x

    def get_y(self):
        """@todo: Docstring for get_y
        :returns: @todo

        """
        return self.y

    def get_value(self):
        """@todo: Docstring for get_value
        :returns: @todo

        """
        return self.value

    def get_candidates(self):
        """@todo: Docstring for get_candidates
        :returns: @todo

        """
        return self.candidates

    def set_value(self, val):
        """@todo: Docstring for set_value.

        :val: @todo
        :returns: @todo

        """
        self.value = val

    def set_candidates(self, cands):
        """@todo: Docstring for set_candidates.

        :cands: @todo
        :returns: @todo

        """
        self.candidates = cands

    def size(self):
        """@todo: Docstring for size
        :returns: @todo

        """
        return len(self.candidates)

    def has_value(self):
        """@todo: Docstring for has_value.
        :returns: @todo

        """
        return self.value != "_"

    def __lt__(self, entry):
        """@todo: Docstring for __lt__

        :entry: @todo
        :returns: @todo

        """
        if not isinstance(entry, GridEntry):
            return False
        return len(self.candidates) < len(entry.candidates)

    def __eq__(self, entry):
        """@todo: Docstring for __eq__

        :entry: @todo
        :returns: @todo

        """
        if not isinstance(entry, GridEntry):
            return False
        return len(self.candidates) == len(entry.candidates)


def make_grid(filename):
    """@todo: Docstring for make_grid

    :filename: @todo
    :returns: @todo

    """
    arr = [line.strip().split(',') for line in open(filename)]
    rows = len(arr)
    cols = len(arr[0])
    for x in range(rows):
        arr[x] = [GridEntry(x, y, arr[x][y]) for y in range(cols)]
    return arr


def get_row(grid, entry):
    """@todo: Docstring for get_row

    :grid: @todo
    :entry: @todo
    :returns: @todo

    """
    x = entry.get_x()
    return grid[x]


def get_col(grid, entry):
    """@todo: Docstring for get_col

    :grid: @todo
    :entry: @todo
    :returns: @todo

    """
    y = entry.get_y()
    col = [grid[i][y] for i in range(len(grid))]
    return col


def get_box(grid, entry):
    """@todo: Docstring for get_box

    :grid: @todo
    :entry: @todo
    :returns: @todo

    """
    x = entry.get_x()
    y = entry.get_y()
    box_x = (x // 3) * 3
    box_y = (y // 3) * 3
    xs = range(box_x, box_x + 3)
    ys = range(box_y, box_y + 3)
    box = [grid[i][j] for i in xs for j in ys]
    return box


def make_value_set(entries):
    """@todo: Docstring for make_value_set.

    :entries: @todo
    :returns: @todo

    """
    val_set = set([e.get_value() for e in entries if e.has_value()])
    return val_set


def filter_initial_values(flatgrid):
    """@todo: Docstring for filter_initial_candidates.

    :flatgrid: @todo
    :returns: @todo

    """
    filtered = filter(lambda e: not e.has_value(), flatgrid)
    return filtered


def initialize_candidates(grid):
    """@todo: Docstring for update_candidates

    :grid: @todo
    :returns: @todo

    """
    flat_grid = list(itertools.chain.from_iterable(grid))
    filtered = filter_initial_values(flat_grid)
    for entry in filtered:
        row_set = make_value_set(get_row(grid, entry))
        col_set = make_value_set(get_col(grid, entry))
        box_set = make_value_set(get_box(grid, entry))
        val_set = row_set.union(col_set.union(box_set))
        all_vals = set(map(str, range(1, len(grid) + 1)))
        candidates = all_vals.difference(val_set)
        entry.set_candidates(candidates)
    return filtered


def propagate_singletons(grid, heap):
    """@todo: Docstring for propagate_singletons.

    :grid: @todo
    :heap: @todo
    :returns: @todo

    """
    while heap.get_min() and heap.get_min().size() == 1:
        singleton = heap.extract_min()
        val = singleton.get_candidates().pop()
        singleton.set_value(val)

def update_grid_entry(grid, entry):
    """@todo: Docstring for update_grid_entry.

    :grid: @todo
    :entry: @todo
    :returns: @todo

    """
    row = get_row(grid, entry)
    col = get_col(grid, entry)
    box = get_box(grid, entry)

def solve_sudoku(filename):
    """@todo: Docstring for solve_sudoku

    :filename: @todo
    :returns: @todo

    """
    sudoku_grid = make_grid(filename)
    filtered_grid = initialize_candidates(sudoku_grid)
    heap = MinHeap()
    heap.build_min_heap(filtered_grid)
    propagate_singletons(sudoku_grid, heap)

if __name__ == "__main__":
    print("Main")
    sudoku_file = sys.argv[1]
    solve_sudoku(sudoku_file)
