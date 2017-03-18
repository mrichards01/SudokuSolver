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

			# Sanitize and display sudoku grid 
			for j in range(0, len(rows)):
				curr_row = rows[j]
				sanitised_row = curr_row.replace('\n','')
				values = sanitised_row.split(' ')
				for i in range(len(values)):
					curr_val = values[i]
					if curr_val!='_':
						self.add_to_sets(i, j, int(curr_val))
				self._grid.append(values)
		except IOError:
			raise 
		
	def add_to_sets(self, x, y, value):
		region_number = self.get_region_number(x,y)
		if region_number not in self._all_regions:
			self._all_regions[region_number] = set()

		self._all_regions[region_number].add(value)

		if x not in self._all_columns:
			self._all_columns[x] = set()
		self._all_columns[x].add(value)

		if y not in self._all_rows:
			self._all_rows[y] = set()
		self._all_rows[y].add(value)

	def remove_from_sets(self, x, y, value):
		region_number = self.get_region_number(x, y)
		self._all_columns[x].remove(value)
		self._all_rows[y].remove(value)
		self._all_regions[region_number].remove(value)

	def get_region_number(self, x, y):
		region_y = ((y) //3)+1
		region_x = ((x) //3)+1
		if region_y==0:
			region_number = region_x
		else:
			region_number = region_x+((region_y-1)*3)
		return int(region_number)

	def get_empty_cells_on_axis_and_region(self, x, y, exclude_input_cell):
		empty_cells = set()
		region_number = self.get_region_number(x,y)
		row = self._grid[y]
		for i in range(0,len(row)):
			if row[i]=='_':
				empty_cells.add((i,y))

		for j in range(0, len(self._grid)):
			row = self._grid[j]
			if row[x]=='_':
				empty_cells.add((i,y))
		region_start_x = (region_number*3)-3
		region_start_y = region_number
		# get cells from region here
		if exclude_input_cell==True:
			empty_cells.remove((x,y))

		return empty_cells

	def display_sudoku_grid(self):
		max_width = 9
		header = "{0} ".format("# "*(max_width+2))
		print (header)

		for row in self._grid:
			#print (" ".join(row))
			current_line ="{0}{1}{2}".format("# "," ".join(row)," #")
			print (current_line)

		footer = "{0} ".format("# "*(max_width+2))
		print (footer)

	def is_cell_valid(self, x, y, value):
		# cell entry is valid if no other entry exists in the same row, column and 3x3 region
		region_number = self.get_region_number(x,y)
		if value in self._all_rows[y] or value in self._all_columns[x] or value in self._all_regions[region_number]:
			return False
		return True

	def get_next_pos(self, x, y):
		x=(x+1)%9
		if x==0:
			y+=1
		return (x,y)

	# function checks if any cascading number of changes from a given position can result in a valid solution
	def is_valid_solution(self, original_grid, x, y):
		# terminate where no other cells are remaining
		if x==0 and y==9:
			return True
		next_pos = self.get_next_pos(x, y)
		# if a value at this position already exists then continue to check the next position
		original_val = original_grid[y][x]
		if original_val!='_':
			return self.is_valid_solution(original_grid, next_pos[0], next_pos[1])

		# otherwise if no value exists at this position, test values 1-9
		# if no value is possible, return False no possible solution 
		for curr_val in range(1, 10):
			# if a value can be entered here, test to see if the solution persists further 
			if self.is_cell_valid(x, y, curr_val):
				self.add_to_sets(x, y, curr_val)
				self._grid[y][x] = str(curr_val)
				if self.is_valid_solution(original_grid, next_pos[0], next_pos[1]):
					return True
				# otherwise, back-track by removingfrom sets and resetting figure in the cell
				self.remove_from_sets(x,y, curr_val)
				self._grid[y][x]='_'

		return False

	def backtracking_search(self):
		# 1) Search through all empty tiles, pick 1 in each check if it conforms to sudoku rules/constraints
		# 2) If any tile doesn't comply add 1, otherwise continue with addition and repeat the process
		# 3) If it is clear no number from 1-9 can be used in that tile then this is no longer a valid grid and requires
		original_grid = list(self._grid)
		#self.solve_by_pen_and_paper()
		self.is_valid_solution(original_grid, 0, 0)

	# mark-up each cell with numbers 1-9
	# iterate through numbers 1-9 while the last pass successfully added a number or this is the first pass
	# if a cell is not valid for a number remove that number from the mark-up set and do this for all cells
	# mark-up cells again when moving onto the next number

	def solve_by_pen_and_paper(self):
		current_grid = list(self._grid)
		solution_found = False # flag to denote if a valid number was found
		# repeat entering numbers until no more definite numbers can be found
		while solution_found:
			solution_found = False
			for test_val in range (1,10):
				#get set of all possible coords for the given test value
				#valid_cells = get_all_possible_cells(current_grid, test_val)

				#for any cell which is still valid, check if the test value can be used without any doubts
				for y in range(0,len(current_grid)):
					col_vals = current_grid[y]
					for x in range(0,len(col_vals)):
						if current_grid[y][x]!='_' or not is_cell_valid(x, y, test_val):
							continue

						region_number = get_region_number(x,y)
						#if the row, column or region only has one remaining number then we can deduce that this number is the only valid number left
						if len(all_rows[y])==8 or len(all_columns[x])==8 or len(all_regions[region_number])==8:
							add_to_sets(x,y,test_val)
							current_grid[y][x] = test_val
							solution_found = True
							continue

						# assume this number is 100% valid until other valid cells are fund in the same row, column or 3x3 region
						row = current_grid[y]
						column = row[x]
						region = all_regions[region_number]
						valid = True
						for i in row:
							if is_cell_valid(x,y,test_val):
								valid = False
								break

						for i in column:
							if is_cell_valid(x,y,test_val):
								valid = False
								break

						for i in region:
							if is_cell_valid(x,y,test_val):
								valid = False
								break

						if valid!=True:
							add_to_sets(x,y,test_val)
							current_grid[y][x] = test_val
							solution_found = True

		return current_grid