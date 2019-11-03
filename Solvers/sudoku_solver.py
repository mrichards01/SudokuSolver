import time

class SudokuSolver:

	def __init__(self, sudoku_file):



	def __pen_and_paper_candidate_checks(self):		
		# use a pen and paper method to find if any numbers are garanteed to be in a cell
		change_found = True
		while change_found:
			change_found = False

			for y in range(0, len(self._grid)):
				for x in range(0, len(self._grid[y])):
					if self._grid[y][x]!='_':
						continue

					possible_vals = self._grid.get_possible_vals()

					# if only one possible value, update the value of this cell
					if len(possible_vals)==1:
						new_val = str(possible_vals.pop())
						self._grid.set_cell_value(x,y, new_val)
						change_found = True
						continue

##THIS IS DUPLICATION (THESE TWO FOR LOOPS)
					# check each cell neighbouring this cell horizontally consistently has any of the possible values
					neighbouring_vals = set(possible_vals)
					for i in range(x-2, x+3):
						# bounds checking and checks to see if the cell is the same
						if x==i or i<0 or self.__get_region_number(i, y)!=region_number:
							continue
						neighbouring_col = self._all_columns[i]
						neighbouring_vals = neighbouring_vals.intersection(neighbouring_col)

					# check each cell neighbouring this cell vertically
					for j in range(y-2, y+3):
						if y==j or j<0 or self.__get_region_number(x, j)!=region_number:
							continue
						neighbouring_row = self._all_rows[j]
						neighbouring_vals = neighbouring_vals.intersection(neighbouring_row)

					if len(neighbouring_vals)==1:
						new_deduced_val = str(neighbouring_vals.pop())
						self.__set_cell_value(x,y, new_deduced_val)
						change_found = True

		# set these new numbers as static as if they were the original grid. These entries do not require further guessign
		self._original_grid = list(self._grid)
