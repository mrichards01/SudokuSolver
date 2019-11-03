import time
from Readers import text_file_reader
from DataStructures import simple_grid
from Solvers import base_solver
from Solvers import pen_and_paper_solver
from Displays import console_display

while True:

    filename = input("Enter the filename for the Sudoku file (default: sudoku.txt): ")
    if filename.strip()=='':
        filename = "sudoku.txt"
    try:
        reader = text_file_reader.TextFileReader(filename)
        reader.read_file()

        grid = simple_grid.SimpleGrid(reader)
        
        screen = console_display.ConsoleDisplay()

        print ("Brute Force method")
        screen.display(grid.get_underlying_grid())
        basic_solver = base_solver.BaseSolver()
        basic_solver.solve(grid)
        screen.display(grid.get_underlying_grid())

        print ("Without Guessing")
        advanced_solver = pen_and_paper_solver.PenAndPaperSolver()
        grid.reset()
        screen.display(grid.get_underlying_grid())
        advanced_solver.solve(grid)
        screen.display(grid.get_underlying_grid())
        print ("Can be solved logically (without guessing): ", advanced_solver.logically_solvable)

    except IOError:
        print ("Could not find file specified.")