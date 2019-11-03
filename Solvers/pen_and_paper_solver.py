from . import base_solver

class PenAndPaperSolver(base_solver.BaseSolver):
    def solve(self, grid):
      self._grid = grid

      # try to solve by using only pen and paper (without guessing or trial and error)
      self._logically_solvable = False
      self.__pen_and_paper_candidate_checks()
      if self._grid.is_complete():
        self._logically_solvable = True
        
    @property
    def logically_solvable(self):
      return self._logically_solvable

    def __pen_and_paper_candidate_checks(self):
      # use a pen and paper method to find if any numbers are garanteed to be in a cell
      change_found = True
      while change_found:
        change_found = False

        for y in range(0, self._grid.size()):
          for x in range(0, self._grid.size()):
            if self._grid.get_cell_val(x, y)!='_':
              continue
            
            # remove values given the local region, row and column
            possible_vals = self._grid.get_possible_vals(x, y)
            # if only one possible value, update the value of this cell
            if len(possible_vals)==1:
              new_val = str(possible_vals.pop())
              self._grid.set_cell_value(x,y, new_val)
              change_found = True
              continue

            # check all columns and rows other than the current one. 
            # Where all of the values are common between and only one value is left remaining it must go here
            neighbouring_vals = self._grid.get_neighbouring_vals_in_common(x, y, set(possible_vals))

            if len(neighbouring_vals)==1:
              new_deduced_val = str(neighbouring_vals.pop())
              self._grid.set_cell_value(x,y, new_deduced_val)
              change_found = True