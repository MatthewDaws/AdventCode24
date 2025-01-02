from .utils.disjointset import DisjointSet

class Parse:
    def __init__(self, rows):
        self._grid = [row.strip() for row in rows]

    @property
    def grid(self):
        return self._grid
    
    @property
    def rows(self):
        return len(self._grid)
    
    @property
    def columns(self):
        return len(self._grid[0])

    def entry(self, r, c):
        return self._grid[r][c]
    
    def neighbours(self, r, c):
        for (rr,cc) in self.all_neighbours(r,c):
            if rr<0 or cc<0 or rr>=self.rows or cc>=self.columns:
                continue
            yield rr, cc, self.entry(rr,cc)

    def find_plots(self):
        plots = DisjointSet()
        for r in range(self.rows):
            for c in range(self.columns):
                plots.add((r,c))
        for r in range(self.rows):
            for c in range(self.columns):
                entry = self.entry(r,c)
                for (rr,cc,ee) in self.neighbours(r,c):
                    if entry == ee:
                        plots.union((r,c), (rr,cc))
        return plots
    
    def all_neighbours(self, r, c):
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            yield (r+dr, c+dc)

    def perimeter(self, plot):
        perimeter = 0
        for (r,c) in plot:
            for (rr,cc) in self.all_neighbours(r,c):
                if (rr,cc) not in plot:
                    perimeter += 1
        return perimeter

    def price(self):
        plots = self.find_plots()
        return sum( len(plot) * self.perimeter(plot) for plot in plots.as_sets() )

    @staticmethod
    def contiguous_sides(e1, e2, edges):
        loc1, loc2 = e1[:2], e2[:2]
        dir1, dir2 = e1[2], e2[2]
        if dir1 != dir2:
            return False
        if dir1 == (1,0):
            if loc2 != (loc1[0]+1, loc1[1]):
                return False
            for r, c, direction in edges:
                if direction == (0,1) and ( (r,c) == loc2 or (r,c+1) == loc2 ):
                    return False
            return True
        else:
            if loc2 != (loc1[0], loc1[1]+1):
                return False
            for r, c, direction in edges:
                if direction == (1,0) and ( (r,c) == loc2 or (r+1,c) == loc2 ):
                    return False
            return True

    def sides(self, plot):
        edges = set()
        for (r,c) in plot:
            if (r-1,c) not in plot:
                edges.add((r,c,(0,1)))
            if (r+1,c) not in plot:
                edges.add((r+1,c,(0,1)))
            if (r,c-1) not in plot:
                edges.add((r,c,(1,0)))
            if (r,c+1) not in plot:
                edges.add((r,c+1,(1,0)))
        sides = DisjointSet(edges)
        for e1 in edges:
            for e2 in edges:
                if self.contiguous_sides(e1, e2, edges):
                    sides.union(e1, e2)
        return len(sides.as_sets())

    def discount_price(self):
        plots = self.find_plots()
        return sum( len(plot) * self.sides(plot) for plot in plots.as_sets() )


def main(second_flag):
    with open("input12.txt") as f:
        garden = Parse(f)
    if not second_flag:
        return garden.price()
    # 852368 too low!
    return garden.discount_price()
