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

# need to read from a file delimited by spaces for each number

sudoku_file = open('sudoku.txt', 'r')
rows = sudoku_file.readlines()
grid = []

#sanitize and display 
for curr_row in rows:
	curr_row.replace('\n','')
	curr_row.replace('\r','')
	print curr_row
	values = curr_row.split(' ')
	grid.append(values)

display_board(grid)

#my_naive_implementation(grid)


#def my_naive_implementation(grid):

