class BaseSolver:
    def solve(self, grid):
        self._grid = grid
        self._original_grid = grid.get_underlying_grid()
        return self.__brute_force(0, 0)
        
    # Function checks if any cascading number of changes from a given position
    # Can result in a valid solution
    def __brute_force(self, x, y):
        # terminate where no other cells are remaining
        if x==0 and y==9:
            return True
        next_pos = self._grid.get_next_pos(x, y)
        # if a value at this position already exists then continue to check the next position
        original_val = self._grid.get_cell_val(x, y)
        if original_val!='_':
            return self.__brute_force(next_pos[0], next_pos[1])

        # otherwise if no value exists at this position, test values 1-9
        # if no value is possible, return False no possible solution and backtrack
        for curr_val in range(1, 10):
            # if a value can be entered here, test to see if the solution persists further
            if self._grid.is_cell_valid(x, y, str(curr_val)):
                self._grid.set_cell_value(x, y, str(curr_val))
                if self.__brute_force(next_pos[0], next_pos[1]):
                    return True
                self._grid.set_cell_value(x, y,'_')
                
        return False
