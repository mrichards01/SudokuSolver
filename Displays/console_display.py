# Simple Console Display
class ConsoleDisplay:
    def display(self, grid):
        if not isinstance(grid, list):
            raise TypeError("grid specified must be a list")
        max_width = len(grid)
        header = "{0} ".format("# "*(max_width+2))
        print (header)

        for row in grid:
            current_line ="{0}{1}{2}".format("# "," ".join(str(x) for x in row)," #")
            print (current_line)

        footer = "{0} ".format("# "*(max_width+2))
        print (footer)