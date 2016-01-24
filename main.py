#problem: Given any sudoku grid, how may you compute a solution (optimally)

#utility function to display board
def display_board(grid):
	header = ""
	for x in range(0,11):
		header+="# "
	print header

	for row in grid:
		current_line ="# "
		for value in row:
			current_line+=value+" "
		current_line+="#"
		print current_line

	footer = ""
	for x in range(0,11):
		footer+="# "
	print footer


def my_naive_implementation(grid):
	# 1) Search through all empty tiles, pick 1 in each check if it conforms to sudoku rules/constraints
	# 2) If  any tile doesn't comply add 1, otherwise continue with addition and repeat the process
	# 3) If it is clear no number from 1-9 can be used in that tile then this is no longer a valid grid and requires

	
#use tree based method with backtracking if a branch is seen to have failed
def backtracing_method(grid):
	return

# need to read from a file delimited by spaces for each number

sudoku_file = open('sudoku.txt', 'r')
rows = sudoku_file.readlines()
grid = []

#sanitize and display 
for curr_row in rows:
	sanitized_row = curr_row.replace('\n','')
	values = sanitized_row.split(' ')
	grid.append(values)

display_board(grid)
my_naive_implementation(grid)

