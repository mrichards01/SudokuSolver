#Problem: How might you solve a Sodoku problem algorithmically? How may you compute an optimal solution
#utility function to display board
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
	region_number = get_region_number(x,y)
	if value in all_rows[y] or value in all_columns[x] or value in all_regions[region_number]:
		return False
	return True
	# cell entry is valid if no other entry exists in the same row, column and 3x3 region

def get_next_pos(x, y):
	x=(x+1)%9
	if x==0:
		y+=1
	return (x,y)

#function checks if any cascading number of changes from a given position can result in a valid solution
def is_valid_solution(original_grid, x, y, no_remaining_cells, current_grid=[]):
	# terminate where no other cells are remaining
	if no_remaining_cells == 0:
		return True
	next_pos = get_next_pos(x, y)
	# if the value at this position already exists then continue to check the next position
	original_val = original_grid[y][x]
	if original_val!='_':
		return is_valid_solution(original_grid, next_pos[0], next_pos[1], no_remaining_cells, current_grid)
	no_remaining_cells-=1

	# otherwise if no value exists at this position, test values 1-9
	# if no value is possible, return False no possible solution 
	for curr_val in range(1, 10):
		# if a value can be entered here, test to see if the solution persists further 
		if is_cell_valid(x, y, curr_val):
			add_to_sets(x, y, curr_val)
			current_grid[y][x] = curr_val
			if is_valid_solution(original_grid, next_pos[0], next_pos[1], no_remaining_cells, current_grid):
				return True
			remove_from_sets(x,y, curr_val)
			current_grid[y][x]='_'

	return False

def brute_force_search(original_grid, no_remaining_cells):
	# 1) Search through all empty tiles, pick 1 in each check if it conforms to sudoku rules/constraints
	# 2) If any tile doesn't comply add 1, otherwise continue with addition and repeat the process
	# 3) If it is clear no number from 1-9 can be used in that tile then this is no longer a valid grid and requires
	current_grid = list(original_grid)
	is_valid_solution(original_grid, 0, 0, no_remaining_cells, current_grid )
	return current_grid

# need to read from a file delimited by spaces for each number
sudoku_file = open('sudoku.txt', 'r')
rows = sudoku_file.readlines()
grid = []

# create lookup collections for fast constant time searches
all_columns = {} #indexed by x position
all_rows = {} # indexed by y position
all_regions = {} #indexed as 1-9 from left to right, top to bottom. Each region is a 3x3 grid in the grid

#sanitize and display 
for j in range(0, len(rows)):
	curr_row = rows[j]
	sanitised_row = curr_row.replace('\n','')
	values = sanitised_row.split(' ')
	#add to all rows collection
	all_rows[j] = set()
	grid.append(values)

display_sudoku_grid(grid)

#initilise quick lookup collections
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

display_sudoku_grid(brute_force_search(grid, no_remaining_cells))