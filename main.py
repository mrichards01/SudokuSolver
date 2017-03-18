import time
from sudoku_solver import SudokuSolver










# def solve_by_pen_and_paper(original_grid):
# 	# Iterate through 1-9 asserting whether they can definitely be placed into a position
# 	# A number can be used with complete certainty if there is only one remaining space on the axis or block
# 	# Otherwise a number can only be used with certainity if it cannot be used in any other cell on the x/y axis and the block region
# 	current_grid = list(original_grid)
# 	for test_val in range (1,10):
# 		#get set of all possible coords for the given test value
# 		#valid_cells = get_all_possible_cells(current_grid, test_val)

# 		#for any cell which is still valid, check if the test value can be used without any doubts
# 		for y in range(0,len(current_grid)):
# 			col_vals = current_grid[y]
# 			for x in range(0,len(col_vals)):
# 				if current_grid[y][x]!='_' or not is_cell_valid(x,y, test_val):
# 					continue

# 				region_number = get_region_number(x,y)
# 				#if the row, column or region only has one remaining number then we can deduce that this number is the only valid number left
# 				if len(all_rows[y])==8 or len(all_columns[x])==8 or len(all_regions[region_number])==8:
# 					current_grid[y][x] = test_val
# 					add_to
# 					add_to_sets(x,y,test_val)
# 					continue

# 				valid = True
# 				row = current_grid[y]
# 				column = row[x]
# 				for i in row:
# 					if is_cell_valid(x,y,test_val):
# 						valid = False
# 						break

# 				for i in column:
# 					if is_cell_valid(x,y,test_val):
# 						valid = False
# 						break
# 				for i in region:
# 					if is_cell_valid(x,y,test_val):
# 						valid = False
# 						break
# 				if valid==True:
# 					current_grid[y][x] = test_val
# 					add_to_sets(x,y,test_val)

# 	return current_grid
					

# # Initilise quick lookup collections
# no_remaining_cells = 0
# for j in range(0,len(grid)):
# 	values = grid[j]
# 	for i in range(0, len(values)):
# 		curr_value = values[i]
# 		if curr_value =='_':
# 			no_remaining_cells+=1
# 			continue
# 		curr_value = int(curr_value)
# 		if not i in all_columns:
# 			all_columns[i] = set()

# 		all_columns[i].add(curr_value)
# 		region_number = get_region_number(i, j)
		
# 		if region_number not in all_regions:
# 			all_regions[region_number] = set()

# 		all_regions[region_number].add(curr_value)
# 		all_rows[j].add(curr_value)

#deterministic pen and paper method followed by brute force approach
init_start = time.time()
#first_grid = solve_by_pen_and_paper(grid)
#display_sudoku_grid(first_grid)
#isplay_sudoku_grid(grid)
#solve_by_pen_and_paper(grid)
solver = SudokuSolver('sudoku.txt')
init_end = time.time()
init_time = init_start - init_end
solver.display_sudoku_grid()
solve_start = time.time()
solver.backtracking_search()
solve_end = time.time()
solver.display_sudoku_grid()
print ("Total time to solve: ",(init_end-init_end)+(solve_end-solve_start))