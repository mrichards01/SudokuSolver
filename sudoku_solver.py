import time

class SudokuSolver:

	def __init__(self, sudoku_file):

		if not isinstance(sudoku_file, str):
			raise TypeEror("sudoku_file arguement must be specified as a string")
		try:
			# Create lookup collections for fast constant time searches 
			# My solution compromises on memory for speed. Arguably the grid array is a duplication of data.
			self._all_columns = {}  #indexed by x position
			self._all_rows = {} 	#indexed by y position
			self._all_regions = {}  #indexed as 1-9 from left to right, top to bottom. Each region is a 3x3 grid in the grid
			sudoku_file = open(sudoku_file, 'r')

			rows = sudoku_file.readlines()
			self._grid = []
			self._original_grid = []
			self._logically_solvable = False
			# Sanitize and display sudoku grid 
			for j in range(0, len(rows)):
				curr_row = rows[j]
				sanitised_row = curr_row.replace('\n','')
				values = sanitised_row.split(' ')
				self._grid.append([])
				self._original_grid.append([])
				for i in range(0, len(values)):
					curr_val = values[i]
					if curr_val!='_':
						self.__add_to_sets(i,j, curr_val)
					self._grid[j].append(curr_val)
					self._original_grid[j].append(curr_val)
		except IOError:
			raise

	def __set_cell_value(self, x, y, value):
		if value=='_':
			curr_val = self._grid[y][x]
			self.__remove_from_sets(x,y, curr_val)
		else:
			self.__add_to_sets(x, y, value)
		self._grid[y][x] = value

	# funnction to add value to hash tables representing distinct regions, columns and rows
	def __add_to_sets(self, x, y, value):
		region_number = self.__get_region_number(x,y)
		if region_number not in self._all_regions:
			self._all_regions[region_number] = set()

		self._all_regions[region_number].add(value)

		if x not in self._all_columns:
			self._all_columns[x] = set()
		self._all_columns[x].add(value)

		if y not in self._all_rows:
			self._all_rows[y] = set()
		self._all_rows[y].add(value)

	# function remotes value from region, column and row hash tables
	def __remove_from_sets(self, x, y, value):
		region_number = self.__get_region_number(x, y)
		self._all_columns[x].remove(value)
		self._all_rows[y].remove(value)
		self._all_regions[region_number].remove(value)

	def __get_region_number(self, x, y):
		region_y = ((y) //3)+1
		region_x = ((x) //3)+1
		if region_y==0:
			region_number = region_x
		else:
			region_number = region_x+((region_y-1)*3)
		return int(region_number)

	def display_sudoku_grid(self):
		max_width = 9
		header = "{0} ".format("# "*(max_width+2))
		print (header)

		for row in self._grid:
			current_line ="{0}{1}{2}".format("# "," ".join(str(x) for x in row)," #")
			print (current_line)

		footer = "{0} ".format("# "*(max_width+2))
		print (footer)

	# cell entry is valid if no other entry exists in the same row, column and 3x3 region
	# calling set_cell_value will add value to these collections
	def __is_cell_valid(self, x, y, value):
		region_number = self.__get_region_number(x,y)
		if value in self._all_rows[y] or value in self._all_columns[x] or value in self._all_regions[region_number]:
			return False
		return True

	# get next position in the grid as if it was being read from left to right, top to bottom
	def __get_next_pos(self, x, y):
		x=(x+1)%9
		if x==0:
			y+=1
		return (x,y)

	# function checks if any cascading number of changes from a given position can result in a valid solution
	def __brute_force(self, x, y):
		# terminate where no other cells are remaining
		if x==0 and y==9:
			return True
		next_pos = self.__get_next_pos(x, y)
		# if a value at this position already exists then continue to check the next position
		original_val = self._original_grid[y][x]
		if original_val!='_':
			return self.__brute_force(next_pos[0], next_pos[1])

		# otherwise if no value exists at this position, test values 1-9
		# if no value is possible, return False no possible solution and backtrack
		for curr_val in range(1, 10):
			# if a value can be entered here, test to see if the solution persists further
			if self.__is_cell_valid(x, y, str(curr_val)):
				self.__set_cell_value(x, y, str(curr_val))
				if self.__brute_force(next_pos[0], next_pos[1]):
					return True
				self.__set_cell_value(x, y,'_')
				
		return False

	@property 
	def logically_solvable(self):
		return self._logically_solvable

	def solve(self):
		# solve by pen and papr, then follow up with backtracking brute force approach
		self._logically_solvable = False # reset boolean to determine if sudoku can be solved without guessing and using only logic
		self.__pen_and_paper_candidate_checks()
		if self.__is_complete():
			self._logically_solvable = True
			return

		self.__brute_force(0,0)

	def __is_complete(self):
		for y in range(0, len(self._grid)):
			for x in range(0, len(self._grid[y])):
				if self._grid[y][x]=='_':
					return False

		return True

	def __pen_and_paper_candidate_checks(self):		
		# use a pen and paper method to find if any numbers are garunteed to be in a cell
		change_found = True
		while change_found:
			change_found = False

			for y in range(0, len(self._grid)):
				for x in range(0, len(self._grid[y])):
					if self._grid[y][x]!='_':
						continue

					# set possible values to all numbers from 1-9 
					possible_vals = set(str(n) for n in range(1,10))
					# remove values given the local region, row and column
					region_number = self.__get_region_number(x,y)
					regional_entries = self._all_regions[region_number]
					row_entries = self._all_rows[y]
					col_entries = self._all_columns[x]
					possible_vals = possible_vals - regional_entries - row_entries - col_entries

					# if only one possible value, update the value of this cell
					if len(possible_vals)==1:
						new_val = str(possible_vals.pop())
						self.__set_cell_value(x,y, new_val)
						change_found = True
						continue

					# check each cell neighbouring this cell horizontally consistently has any of the possible values
					neighbouring_vals = set(possible_vals)
					# #print (neighbouring_vals)
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
