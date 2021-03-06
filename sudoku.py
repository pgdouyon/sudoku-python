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
        """ Return heap-index for the parent of node at index. """
        return index // 2

    @staticmethod
    def left_child(index):
        """ Return heap-index for the left-child of node at index. """
        return index << 1

    @staticmethod
    def right_child(index):
        """ Return the heap-index for the right-child of node at index. """
        return (index << 1) + 1

    def min_heapify(self, i):
        """
        Build a min-heap rooted at node i using the two min-heaps rooted at
        Left(i) and Right(i).

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
        """ Build min-heap from input array. """

        size = len(arr)
        self.heap = [None] + arr
        self.heap_size = size
        self.rebuild_heap()

    def rebuild_heap(self):
        """
        Rebuild min-heap from self.heap.

        Used when heap values have mutated
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
        """ Remove and return the node at the top of the heap. """
        if self.heap_size < 1:
            return None
        min_node = self.heap[1]
        self.heap[1] = self.heap[self.heap_size]
        self.heap_size -= 1
        self.min_heapify(1)
        return min_node

    def get_heap(self):
        """ Return array representation of heap. """
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
        """ Return x-coordinate """
        return self.x

    def get_y(self):
        """ Return y-coordinate """
        return self.y

    def get_value(self):
        """ Return value of cell """
        return self.value

    def get_candidates(self):
        """ Return set of candidates """
        return self.candidates

    def set_value(self, val):
        """ Set cell value """
        self.value = val

    def set_candidates(self, cands):
        """ Set candidates """
        self.candidates = cands

    def size(self):
        """ Return length of candidate set for this cell """
        return len(self.candidates)

    def has_value(self):
        """ Return true if cell has a value assigned """
        return self.value != "_"

    def clone(self):
        """ Return copy of this GridEntry object """
        clone = GridEntry(self.x, self.y, self.value)
        clone.set_candidates(self.candidates.copy())
        return clone

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
    Build a 2D square array from txt file.

    File should be a comma-separated list of values representing a sudoku
    grid.  Blank cells should be represented by a "_"

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
    xpose = transpose(grid)
    col = xpose[y]
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


def transpose(grid):
    """
    Return a transpose of the grid
    :grid: 2D array representing sudoku grid

    """
    xpose = [list(l) for l in zip(*grid)]
    return xpose


def make_value_set(entries):
    """
    Build a set of all the entry values stored in argument list

    :entries: list of GridEntry objects
    :returns: set of values stored in 'entries'

    """
    val_set = set([e.get_value() for e in entries if e.has_value()])
    return val_set


def get_unsolved_cells(flatgrid):
    """
    Extract cells without an initial value from the 1D input array

    :flatgrid: 1D array of a flattend 2D sudoku grid
    :returns: list of GridEntry objects with unknown/unset values

    """
    filtered = [e for e in flatgrid if not e.has_value()]
    return filtered


def update_candidates(grid, entries):
    """
    Recalculates possible candidates for each GridEntry object in entries.

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


def propagate_singletons(grid, heap):
    """
    Sets the value of all cells with only one candidate.

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


def propagate_singletons_recursive(grid, heap):
    """
    Reduces grid by recursively propagating singletons and rebuilding the heap

    Uses propagate singleton to reduce all singletons currently on the heap,
    then updates the candidate sets for all cells on the heap and loops if
    there are new singletons to reduce.

    :grid: 2D sudoku grid
    :heap: heap containing unsolved cells

    """
    while heap.get_min() and heap.get_min().size() == 1:
        propagate_singletons(grid, heap)
        update_candidates(grid, heap.get_heap())
        heap.rebuild_heap()


def clone_grid(grid):
    """ Copy each entry to a new 2D array """
    grid_copy = []
    for row in grid:
        row_copy = [e.clone() for e in row]
        grid_copy.append(row_copy)
    return grid_copy


def clone_state(grid):
    """ Return cloned grid and a new heap of its unsolved cells """
    grid_copy = clone_grid(grid)
    flatgrid = list(itertools.chain.from_iterable(grid_copy))
    unsolved_cells = get_unsolved_cells(flatgrid)
    heap_copy = MinHeap()
    heap_copy.build_min_heap(unsolved_cells)
    return (grid_copy, heap_copy)


def dfs(grid, heap):
    """
    Solve grid by checking each candidate for the entry at the top of the heap

    Clones the grid/heap and randomly chooses a candidate for the GridEntry
    atop the heap.  Recursively checks if that choice is a part of the correct
    solution and if not then the recursion backs up and chooses a different
    candidate.  The original heap/grid is cloned to avoid corrupting its values
    if the original choice was incorrect.

    :returns: puzzle solution or false if none exists for the given input state

    """
    while heap.get_min() and heap.get_min().size() != 0:
        val = heap.get_min().get_candidates().pop()
        grid_copy, heap_copy = clone_state(grid)

        singleton = heap_copy.extract_min()
        singleton.set_value(val)
        update_candidates(grid_copy, heap_copy.get_heap())
        heap_copy.rebuild_heap()
        propagate_singletons_recursive(grid_copy, heap_copy)

        if not heap_copy.get_min():
            if validate_sudoku(grid_copy):
                return grid_copy
        elif heap_copy.get_min().size() > 1:
            solution = dfs(grid_copy, heap_copy)
            if solution:
                return solution

    return False


def init_sudoku(filename):
    """
    Generates sudoku grid from input file and initializes candidate values.

    Builds the 2D grid and populates the set of candidates for each unsolved
    cell with its initial value.

    :filename: input file containing sudoku puzzle
    :returns: 2D sudoku grid and list of unsolved cells

    """
    sudoku = make_grid(filename)
    flat_grid = list(itertools.chain.from_iterable(sudoku))
    unsolved_cells = get_unsolved_cells(flat_grid)
    update_candidates(sudoku, unsolved_cells)

    return (sudoku, unsolved_cells)


def solve_sudoku(filename):
    """
    Solve sudoku puzzle sourced from input file.

    Builds the 2D grid representation of sudoku puzzle and solves it via a
    combination of singleton propagation (using a priority queue) and
    depth-first search if necessary.

    :filename: file containing sudoku grid

    """
    sudoku, unsolved_cells = init_sudoku(filename)
    heap = MinHeap()
    heap.build_min_heap(unsolved_cells)

    propagate_singletons_recursive(sudoku, heap)
    if heap.get_min():
        sudoku = dfs(sudoku, heap)

    print_sudoku(sudoku)

    if validate_sudoku(sudoku):
        print("Solution validated!")
    else:
        print("FAILED - Invalid solution")


def print_sudoku(grid):
    for row in grid:
        s = ""
        for entry in row:
            s = s + entry.get_value() + ","
        print(s)


def check_rows(grid):
    """ Checks all rows to see if the have the numbers 1-9 """
    for row in grid:
        val_set = make_value_set(row)
        expected = set(map(str, range(1, len(row) + 1)))
        if val_set != expected:
            return False
    return True


def check_cols(grid):
    """ Checks all cols to see if the have the numbers 1-9 """
    xpose = transpose(grid)
    for col in xpose:
        val_set = make_value_set(col)
        expected = set(map(str, range(1, len(col) + 1)))
        if val_set != expected:
            return False
    return True


def check_boxs(grid):
    """ Checks all boxes to see if the have the numbers 1-9 """
    for box_num in range(len(grid)):
        rows = 3 * (box_num // 3)
        cols = 3 * (box_num % 3)
        xs = range(rows, rows + 3)
        ys = range(cols, cols + 3)
        box = [grid[x][y] for x in xs for y in ys]
        val_set = make_value_set(box)
        expected = set(map(str, range(1, len(box) + 1)))
        if val_set != expected:
            return False
    return True


def validate_sudoku(grid):
    """ Validates that all rows, cols, and boxes contain only numbers 1-9 """
    rows = check_rows(grid)
    cols = check_cols(grid)
    boxs = check_boxs(grid)
    return rows and cols and boxs


if __name__ == "__main__":
    print("Main")
    sudoku_file = sys.argv[1]
    solve_sudoku(sudoku_file)
