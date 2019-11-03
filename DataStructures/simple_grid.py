import copy

class SimpleGrid:
    def __init__(self, reader):
        self._reader = reader
        self.reset()
    
    def reset(self):
        # Create lookup collections for fast constant time searches 
        # My solution compromises on memory for speed. 
        self._all_columns = {}  #indexed by x position
        self._all_rows = {} 	#indexed by y position
        self._all_regions = {}  #indexed as 1-9 from left to right, top to bottom. Each region is a 3x3 grid in the grid
        self._grid = self._reader.raw_grid
        self._logically_solvable = False

        for j in range(0, len(self._grid)):
            for i in range(0, len(self._grid[j])):
                curr_val = self._grid[j][i]
                if curr_val!='_':
                    self.__add_to_sets(i,j, curr_val)

    @property 
    def logically_solvable(self):
        return self._logically_solvable
    
    def is_complete(self):
        for y in range(0, len(self._grid)):
            for x in range(0, len(self._grid[y])):
                if self._grid[y][x]=='_':
                    return False

        return True

    def __get_region_number(self, x, y):
        region_y = ((y) //3)+1
        region_x = ((x) //3)+1
        if region_y==0:
            region_number = region_x
        else:
            region_number = region_x+((region_y-1)*3)
        return int(region_number)

    def set_cell_value(self, x, y, value):
        if value=='_':
            curr_val = self._grid[y][x]
            self.__remove_from_sets(x,y, curr_val)
        else:
            self.__add_to_sets(x, y, value)
        self._grid[y][x] = value

    # function to add value to hash tables representing distinct regions, columns and rows
    def __add_to_sets(self, x, y, value):
        region_number = self.__get_region_number(x,y)
        if region_number not in self._all_regions:
            self._all_regions[region_number] = set()

        self._all_regions[region_number].add(value)

        if x not in self._all_columns:
            self._all_columns[x] = set()
        self._all_columns[x].add(value)

        if y not in self._all_rows:
            self._all_rows[y] = set()
        self._all_rows[y].add(value)

    # function remotes value from region, column and row hash tables
    def __remove_from_sets(self, x, y, value):
        region_number = self.__get_region_number(x, y)
        self._all_columns[x].remove(value)
        self._all_rows[y].remove(value)
        self._all_regions[region_number].remove(value)

    # cell entry is valid if no other entry exists in the same row, column and 3x3 region
    # calling set_cell_value will add value to these collections
    def is_cell_valid(self, x, y, value):
        region_number = self.__get_region_number(x,y)
        if value in self._all_rows[y] or value in self._all_columns[x] or value in self._all_regions[region_number]:
            return False
        return True

    # function to return possible values based on region, column and row
    def get_possible_vals(self, x, y, existing_options = set(str(n) for n in range(1,10))):
        # set possible values to all numbers from 1-9 then find the intersection of all sets
        region_number = self.__get_region_number(x,y)
        regional_entries = self._all_regions[region_number]
        row_entries = self._all_rows[y]
        col_entries = self._all_columns[x]
        return existing_options - regional_entries - row_entries - col_entries

    # function to return common values in neighbouring rows/columns
    def get_neighbouring_vals_in_common(self, x, y, possible_vals = set(str(n) for n in range(1,10))):
        region_number = self.__get_region_number(x, y)

        for j in range(y-2, y+3):
            for i in range(x-2, x+3):
                if i==x or j==y:
                    continue
                # bounds checking and checks to ensure cell is not the same
                if i<0 or j<0 or i>=len(self._grid) or j>=len(self._grid) or self.__get_region_number(i, j)!=region_number:
                    continue
                col_vals = self._all_columns[i]
                row_vals = self._all_rows[j]
                possible_vals = possible_vals.intersection(col_vals)
                possible_vals = possible_vals.intersection(row_vals)
        
        return possible_vals

    def get_underlying_grid(self):
        return copy.deepcopy(self._grid)

    # get next position in the grid as if it was being read from left to right, top to bottom
    def get_next_pos(self, x, y):
        x=(x+1)%9
        if x==0:
            y+=1
        return (x,y)
    
    def get_cell_val(self, x, y):
        return (self._grid[y][x])
        
    def size(self):
        return len(self._grid)