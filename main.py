import time

def display_sudoku_grid(grid):
	header = ""
	for x in range(0,len(grid)+2):
		header+="# "
	print (header)

	for row in grid:
		current_line ="# "
		for value in row:
			current_line+=str(value)+" "
		current_line+="#"
		print (current_line)

	footer = ""
	for x in range(0,len(grid)+2):
		footer+="# "
	print (footer)

def get_region_number(x, y):
	region_y = ((y) //3)+1
	region_x = ((x)//3)+1
	if region_y==0:
		region_number = region_x
	else:
		region_number = region_x+((region_y-1)*3)
	return int(region_number)

def add_to_sets(x,y, value):
	region_number = get_region_number(x,y)
	all_regions[region_number].add(value)
	all_columns[x].add(value)
	all_rows[y].add(value)

def remove_from_sets(x, y, value):
	region_number = get_region_number(x, y)
	all_columns[x].remove(value)
	all_rows[y].remove(value)
	all_regions[region_number].remove(value)

def is_cell_valid(x, y, value):
	# cell entry is valid if no other entry exists in the same row, column and 3x3 region
	region_number = get_region_number(x,y)
	if value in all_rows[y] or value in all_columns[x] or value in all_regions[region_number]:
		return False
	return True

def get_next_pos(x, y):
	x=(x+1)%9
	if x==0:
		y+=1
	return (x,y)

def get_empty_cells_on_axis_and_region(x,y, exclude_input_cell, current_grid):
	empty_cells = set()
	region_number = get_region_number(x,y)
	row = current_grid[y]
	for i in range(0,len(row)):
		if row[i]=='_':
			empty_cells.add((i,y))

	for j in range(0, len(current_grid)):
		row = current_grid[j]
		if row[x]=='_':
			empty_cells.add((i,y))

	#get cells from region here
	if exclude_input_cell==True:
		empty_cells.remove((x,y))

	return empty_cells

#function checks if any cascading number of changes from a given position can result in a valid solution
def is_valid_solution(original_grid, x, y, current_grid=[]):
	# terminate where no other cells are remaining
	if x==8 and y==8:
		return True
	next_pos = get_next_pos(x, y)
	# if the value at this position already exists then continue to check the next position
	original_val = original_grid[y][x]
	if original_val!='_':
		return is_valid_solution(original_grid, next_pos[0], next_pos[1], current_grid)

	# otherwise if no value exists at this position, test values 1-9
	# if no value is possible, return False no possible solution 
	for curr_val in range(1, 10):
		# if a value can be entered here, test to see if the solution persists further 
		if is_cell_valid(x, y, curr_val):
			add_to_sets(x, y, curr_val)
			current_grid[y][x] = curr_val
			if is_valid_solution(original_grid, next_pos[0], next_pos[1], current_grid):
				return True
			remove_from_sets(x,y, curr_val)
			current_grid[y][x]='_'

	return False

def solve_by_pen_and_paper(original_grid):
	# Iterate through 1-9 asserting whether they can definitely be placed into a position
	# A number can be used with complete certainty if there is only one remaining space on the axis or block
	# Otherwise a number can only be used with certainity if it cannot be used in any other cell on the x/y axis and the block region
	current_grid = list(original_grid)
	for test_val in range (1,10):
		#get set of all possible coords for the given test value
		#valid_cells = get_all_possible_cells(current_grid, test_val)

		#for any cell which is still valid, check if the test value can be used without any doubts
		for y in range(0,len(current_grid)):
			col_vals = current_grid[y]
			for x in range(0,len(col_vals)):
				if current_grid[y][x]!='_' or not is_cell_valid(x,y, test_val):
					continue

				region_number = get_region_number(x,y)
				#if the row, column or region only has one remaining number then we can deduce that this number is the only valid number left
				if len(all_rows[y])==8 or len(all_columns[x])==8 or len(all_regions[region_number])==8:
					current_grid[y][x] = test_val
					add_to
					add_to_sets(x,y,test_val)
					continue

				valid = True
				row = current_grid[y]
				column = row[x]
				region
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
				if valid==True:
					current_grid[y][x] = test_val
					add_to_sets(x,y,test_val)

	return current_grid
					
def brute_force_search(original_grid):
	# 1) Search through all empty tiles, pick 1 in each check if it conforms to sudoku rules/constraints
	# 2) If any tile doesn't comply add 1, otherwise continue with addition and repeat the process
	# 3) If it is clear no number from 1-9 can be used in that tile then this is no longer a valid grid and requires
	current_grid = list(original_grid)
	is_valid_solution(original_grid, 0, 0, current_grid )
	return current_grid

# Need to read from a file delimited by spaces for each number
sudoku_file = open('sudoku.txt', 'r')
rows = sudoku_file.readlines()
grid = []

# Create lookup collections for fast constant time searches 
# My solution compromises on memory for speed
all_columns = {} #indexed by x position
all_rows = {} 	 #indexed by y position
all_regions = {} #indexed as 1-9 from left to right, top to bottom. Each region is a 3x3 grid in the grid

# Sanitize and display sudoku grid 
for j in range(0, len(rows)):
	curr_row = rows[j]
	sanitised_row = curr_row.replace('\n','')
	values = sanitised_row.split(' ')
	#add to all rows collection
	all_rows[j] = set()
	grid.append(values)

display_sudoku_grid(grid)

# Initilise quick lookup collections
no_remaining_cells = 0
for j in range(0,len(grid)):
	values = grid[j]
	for i in range(0, len(values)):
		curr_value = values[i]
		if curr_value =='_':
			no_remaining_cells+=1
			continue
		curr_value = int(curr_value)
		if not i in all_columns:
			all_columns[i] = set()

		all_columns[i].add(curr_value)
		region_number = get_region_number(i, j)
		
		if region_number not in all_regions:
			all_regions[region_number] = set()

		all_regions[region_number].add(curr_value)
		all_rows[j].add(curr_value)

#deterministic pen and paper method followed by brute force approach
start_time = time.time()
#first_grid = solve_by_pen_and_paper(grid)
#display_sudoku_grid(first_grid)
#isplay_sudoku_grid(grid)
solve_by_pen_and_paper(grid)
#brute_force_search(grid)
display_sudoku_grid(grid)
print("--- %s seconds ---" % (time.time() - start_time))