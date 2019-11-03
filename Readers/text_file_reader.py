import copy

class TextFileReader:
    def __init__(self, sudoku_file):
        if not isinstance(sudoku_file, str):
            raise TypeError("sudoku_file argument must be specified as a string")
        self._sudoku_file = sudoku_file
        self._grid = list()
    
    def read_file(self):
        try:
            opened_file = open(self._sudoku_file, 'r')
            rows = opened_file.readlines()
            self._grid = list()
            # Sanitize grid
            for j in range(0, len(rows)):
                curr_row = rows[j]
                sanitised_row = curr_row.replace('\n','')
                values = sanitised_row.split(' ')
                self._grid.append([])
                for i in range(0, len(values)):
                    curr_val = values[i]
                    self._grid[j].append(curr_val)
        except IOError:
            raise

    @property
    def raw_grid(self):
        return copy.deepcopy(self._grid)