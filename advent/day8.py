import itertools, math

class Parse:
    def __init__(self, rows):
        self._grid = []
        self._frequencies = set()
        for row in rows:
            self._grid.append(row.strip())
            for c in self._grid[-1]:
                if c != ".":
                    self._frequencies.add(c)
        self._locations = dict()
        for c in self._frequencies:
            self._locations[c] = []
        for r, row in enumerate(self._grid):
            for c, entry in enumerate(row):
                if entry != ".":
                    self._locations[entry].append( (r,c) )
        
    @property
    def locations(self):
        return self._locations
    
    @property
    def rows(self):
        return len(self._grid)
    
    @property
    def columns(self):
        return len(self._grid[0])

    @staticmethod
    def antinodes(a, b):
        dr, dc = b[0] - a[0], b[1] - a[1]
        r1, c1 = a[0] - dr, a[1] - dc
        r2, c2 = b[0] + dr, b[1] + dc
        return [(r1,c1), (r2,c2)]
    
    def all_antinodes(self, frequency):
        out = set()
        for a,b in itertools.combinations(self._locations[frequency], 2):
            for (r,c) in self.antinodes(a, b):
                if r>=0 and c>=0 and r<self.rows and c<self.columns:
                    out.add((r,c))
        return out
    
    def find_all_antinodes(self):
        antinodes = set()
        for freq in self._locations:
            antinodes |= self.all_antinodes(freq)
        return antinodes
    
    def _line_based_at(self, start, delta):
        r, c = start
        while r>=0 and c>=0 and r<self.rows and c<self.columns:
            yield r, c
            r += delta[0]
            c += delta[1]

    def lines_from(self, a, b):
        dr, dc = b[0] - a[0], b[1] - a[1]
        g = math.gcd(dr, dc)
        dr = dr // g
        dc = dc // g
        yield from self._line_based_at(a, (dr, dc))
        yield from self._line_based_at(a, (-dr, -dc))

    def find_all_line_points(self):
        points = set()
        for frequency in self._locations:
            for a,b in itertools.combinations(self._locations[frequency], 2):
                points.update(self.lines_from(a, b))
        return points
        

    # In the 2nd case, for every pair we look at the line (1-t)x1 + tx2 for any t, and look at all intersections
    # with the grid: i.e. the integer lattice.
    

def main(second_flag):
    with open("input8.txt") as f:
        grid = Parse(f)
    if not second_flag:
        return len(grid.find_all_antinodes())
    return len(grid.find_all_line_points())
