import itertools

class Parse:
    def __init__(self, rows):
        self._locks = []
        self._keys = []

        def read_rows(rows):
            grid = []
            for row in rows:
                row = row.strip()
                if len(row) == 0:
                    return grid
                grid.append(row)
            return grid

        def parse(grid):
            heights = []
            for col in range(len(grid[0])):
                heights.append( sum(row[col]=="#" for row in grid) )
            return heights
        
        while True:
            grid = read_rows(rows)
            if len(grid) == 0:
                break
            if all(c=="#" for c in grid[0]):
                self._locks.append( parse(grid[1:]) )
            else:
                self._keys.append( parse(grid[:-1]) )

    @property
    def keys(self):
        return self._keys
    
    @property
    def locks(self):
        return self._locks
    
    @staticmethod
    def overlap(lock, key):
        return any(x+y>5 for x,y in zip(lock, key))
    
    def fit_count(self):
        return sum( not self.overlap(lock, key)
            for lock, key in itertools.product(self._locks, self._keys) )

    
def main(second_flag):
    with open("input25.txt") as f:
        lockskeys = Parse(f)
    if not second_flag:
        return lockskeys.fit_count()
