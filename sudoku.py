#! /usr/bin/env python3.3
import sys
import itertools


class MinHeap(object):
    """Priority Queue used to keep track of GridEntry
    objects with lowest number of candidates"""

    def __init__(self):
        self.heap = [None]
        self.heap_size = 0

    @staticmethod
    def parent(index):
        """
        Return heap-index for the parent of node at index

        :index: index of child node
        :returns: index of parent node

        """
        return index // 2

    @staticmethod
    def left_child(index):
        """
        Return heap-index for the left-child of node at index

        :index: index of parent node
        :returns: index of left-child

        """
        return index << 1

    @staticmethod
    def right_child(index):
        """
        Return the heap-index for the right-child of node at index

        :index: index of parent node
        :returns: index of right-child

        """
        return (index << 1) + 1

    def min_heapify(self, i):
        """
        Build a min-heap out of node i and the two min-heaps rooted at
        Left(i) and Right(i)

        :i: index of root node

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
        """
        Build min-heap from input array

        :arr: array to be heapified

        """
        size = len(arr)
        self.heap = [None] + arr
        self.heap_size = size
        self.rebuild_heap()

    def rebuild_heap(self):
        """
        Rebuild min-heap from self.heap.  Used when heap values have mutated
        and heap invariant must be restored throughout heap.

        """
        size = self.heap_size
        for i in range(size // 2, 0, -1):
            self.min_heapify(i)

    def get_min(self):
        """
        Return the node at the top of the heap, but do not remove it.

        :returns: Node with minimum size

        """
        if self.heap_size < 1:
            return None
        else:
            return self.heap[1]

    def extract_min(self):
        """
        Remove and return the node at the top of the heap.

        :returns: Node with minimum size

        """
        if self.heap_size < 1:
            return None
        min_node = self.heap[1]
        self.heap[1] = self.heap[self.heap_size]
        self.heap_size -= 1
        self.min_heapify(1)
        return min_node

    def get_heap(self):
        """
        Return array representation of heap.

        :returns: array representation of heap

        """
        return self.heap[1:]


class GridEntry(object):
    """
    Stores the coordinates, value, and potential candidates for
    sudoku grid cells"""

    def __init__(self, x, y, value):
        """Initializes coordinates, value, and empty candidates set.

        :x: x-coordinate
        :y: y-coordinate
        :value: initial value

        """
        self.x = x
        self.y = y
        self.value = value
        self.candidates = set([])

    def get_x(self):
        """
        Return x-coordinate

        :returns: x-coordinate

        """
        return self.x

    def get_y(self):
        """
        Return y-coordinate

        :returns: y-coordinate

        """
        return self.y

    def get_value(self):
        """
        Return value of cell

        :returns: value

        """
        return self.value

    def get_candidates(self):
        """
        Return set of candidates

        :returns: set of candidates

        """
        return self.candidates

    def set_value(self, val):
        """
        Set cell value

        :val: value to be set

        """
        self.value = val

    def set_candidates(self, cands):
        """
        Set candidates set

        :cands: candidates set

        """
        self.candidates = cands

    def size(self):
        """
        Return length of candidate set for this cell

        :returns: length of candidate set

        """
        return len(self.candidates)

    def has_value(self):
        """
        Check if cell has a value assigned
        :returns: true if cell's value has been set

        """
        return self.value != "_"

    def __lt__(self, entry):
        """
        Override __lt__ method.  Compare cells by length of candidate sets.

        :entry: cell to be compared against
        :returns: true if this cell has a smaller candidate set

        """
        if not isinstance(entry, GridEntry):
            return False
        return len(self.candidates) < len(entry.candidates)

    def __eq__(self, entry):
        """
        Override __eq__ method.  Compare cells by length of candidate sets.

        :entry: cell to be compared against
        :returns: true if this cell has an equal sized candidate set

        """
        if not isinstance(entry, GridEntry):
            return False
        return len(self.candidates) == len(entry.candidates)


def make_grid(filename):
    """
    Build a 2D square array from txt file.  File should be a comma-separated
    list of values representing a sudoku grid.  Blank cells should be
    represented by a "_"

    i.e.

    1,_,3
    2,3,_
    _,_,2

    :filename: name of file storing sudoku grid values
    :returns: 2D square array representing sudoku grid

    """
    arr = [line.strip().split(',') for line in open(filename)]
    rows = len(arr)
    cols = len(arr[0])
    for x in range(rows):
        arr[x] = [GridEntry(x, y, arr[x][y]) for y in range(cols)]
    return arr


def get_row(grid, entry):
    """
    Return list of GridEntry objects located in the row containing 'entry'

    :grid: 2D array representing sudoku grid
    :entry: element of grid array
    :returns: list of GridEntry objects in the same row as 'entry'

    """
    x = entry.get_x()
    return grid[x]


def get_col(grid, entry):
    """
    Return list of GridEntry objects located in the col containing 'entry'

    :grid: 2D array representing sudoku grid
    :entry: element of grid array
    :returns: list of GridEntry objects in the same col as 'entry'

    """
    y = entry.get_y()
    col = [grid[i][y] for i in range(len(grid))]
    return col


def get_box(grid, entry):
    """
    Return list of GridEntry objects located in the box containing 'entry'

    :grid: 2D array representing sudoku grid
    :entry: element of grid array
    :returns: list of GridEntry objects in the same box as 'entry'

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
    """
    Build a set of all the entry values stored in argument list

    :entries: list of GridEntry objects
    :returns: set of values stored in 'entries'

    """
    val_set = set([e.get_value() for e in entries if e.has_value()])
    return val_set


def filter_initial_values(flatgrid):
    """
    Remove GridEntry objects that already have a value set.
    The list returned from this method will be used to
    populate the min-heap with all unknown cells whose
    values still need to be determined.

    :flatgrid: 1D array of a flattend 2D sudoku grid
    :returns: list of GridEntry objects with unknown/unset values

    """
    filtered = [e for e in flatgrid if not e.has_value()]
    return filtered


def update_candidates(grid, entries):
    """
    Recalculates possible candidates for each GridEntry object in entries.
    Used after grid values have been updated.

    :grid: 2D sudoku grid
    :entries: 1D array of flattened 2D sudoku grid

    """
    for entry in entries:
        row_set = make_value_set(get_row(grid, entry))
        col_set = make_value_set(get_col(grid, entry))
        box_set = make_value_set(get_box(grid, entry))
        val_set = row_set.union(col_set.union(box_set))
        all_nums = set(map(str, range(1, len(grid) + 1)))
        candidates = all_nums.difference(val_set)
        entry.set_candidates(candidates)


def initialize_candidates(grid):
    """
    Populate GridEntry objects with unknown values with a set of all
    possible candidate values.

    :grid: 2D sudoku grid
    :returns: 1D list of unknown GridEntry objects with candidates updated

    """
    flat_grid = list(itertools.chain.from_iterable(grid))
    filtered = filter_initial_values(flat_grid)
    update_candidates(grid, filtered)
    return filtered


def propagate_all_singletons(grid, heap):
    """
    Recursively checks the top element of the heap.  If it is a singleton,
    meaning it has only one candidate value, then that value must be the value
    of the cell.  That value is set and the entry is removed from the heap
    since its value has been determined.

    Updates the candidates of all objects remaining in the heap and rebuilds
    the heap when all known singletons have been removed.

    :grid: 2D sudoku grid
    :heap: min-heap of unknown GridEntry objects

    """
    while heap.get_min() and heap.get_min().size() == 1:
        singleton = heap.extract_min()
        val = singleton.get_candidates().pop()
        singleton.set_value(val)
    update_candidates(grid, heap.get_heap())
    heap.rebuild_heap()


def solve_sudoku(filename):
    """
    Builds the 2D grid representation of sudoku puzzle and solves it via a
    combination of singleton propagation and depth-first search.

    :filename: file containing sudoku grid

    """
    sudoku_grid = make_grid(filename)
    filtered_grid = initialize_candidates(sudoku_grid)
    heap = MinHeap()
    heap.build_min_heap(filtered_grid)

    while heap.get_min() and heap.get_min().size() == 1:
        propagate_all_singletons(sudoku_grid, heap)


def print_sudoku(grid):
    for row in grid:
        s = ""
        for entry in row:
            s = s + entry.get_value() + ","
        print(s)

if __name__ == "__main__":
    print("Main")
    sudoku_file = sys.argv[1]
    solve_sudoku(sudoku_file)
