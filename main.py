import time
from sudoku_solver import SudokuSolver

					
#deterministic pen and paper method followed by brute force approach
init_start = time.time()
#first_grid = solve_by_pen_and_paper(grid)
#isplay_sudoku_grid(grid)
#solve_by_pen_and_paper(grid)
solver = SudokuSolver('sudoku.txt')
init_end = time.time()
init_time = init_start - init_end
solver.display_sudoku_grid()
solve_start = time.time()
solver.solve()
#solver.brute_force(0,0)
solve_end = time.time()
solver.display_sudoku_grid()
print ("Total time to solve: ",(init_end-init_end)+(solve_end-solve_start))