import time
from sudoku_solver import SudokuSolver

while True:

	filename = input("Enter the filename for the Sudoku file (default: sudoku.txt): ")
	if filename.strip()=='':
		filename = "sudoku.txt"
	try:
		solve_start = time.time()
		solver = SudokuSolver(filename)
		solver.display_sudoku_grid()
		solver.solve()
		solve_end = time.time()
		solve_time = solve_end - solve_start
		solver.display_sudoku_grid()

		# display solve time (including display output)
		print ("Total time to solve (seconds): ",solve_time)
		print ("Can be solved logically (without guessing): ", solver.logically_solvable)
	except IOError:
		print ("Could not find file specified.")