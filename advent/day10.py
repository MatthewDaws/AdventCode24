from collections import namedtuple

class DGraph:
    def __init__(self):
        self._neighbours = dict()

    @property
    def vertices(self):
        return self._neighbours.keys()
    
    def neighbours_of(self, vertex):
        return self._neighbours[vertex]
    
    def add_edge(self, source, target):
        if source not in self._neighbours:
            self._neighbours[source] = list()
        self._neighbours[source].append(target)


class Parse:
    def __init__(self, rows):
        self._grid = []
        for row in rows:
            self._grid.append( [int(c) for c in row.strip()] )

    @property
    def grid(self):
        return self._grid
    
    @property
    def rows(self):
        return len(self._grid)
    
    @property
    def columns(self):
        return len(self._grid[0])
    
    def trail_heads(self):
        for r, row in enumerate(self._grid):
            for c, entry in enumerate(row):
                if entry == 0:
                    yield (r,c)

    def is_top(self, loc):
        return self._grid[loc[0]][loc[1]] == 9

    def steps_up(self, loc):
        deltas = [(-1,0), (0,-1), (0,1), (1,0)]
        r, c = loc
        current = self._grid[r][c]
        steps = set()
        for (dr, dc) in deltas:
            rr, cc = r+dr, c+dc
            if rr>=0 and cc>=0 and rr<self.rows and cc<self.columns and self._grid[rr][cc] == current + 1:
                steps.add((rr,cc))
        return steps
    
    def brute_force_from(self, loc):
        tops_attainable = set()
        to_visit = [loc]
        while len(to_visit) > 0:
            loc = to_visit.pop()
            for new_loc in self.steps_up(loc):
                if self.is_top(new_loc):
                    tops_attainable.add(new_loc)
                else:
                    to_visit.append(new_loc)
        return tops_attainable

    def brute_force(self):
        return sum(len(self.brute_force_from(loc)) for loc in self.trail_heads())

    def count_paths_from(self, loc):
        counts = [[0]*self.columns for _ in range(self.rows)]
        tops_attainable = set()
        to_visit = [loc]
        while len(to_visit) > 0:
            loc = to_visit.pop()
            counts[loc[0]][loc[1]] += 1
            for new_loc in self.steps_up(loc):
                if self.is_top(new_loc):
                    tops_attainable.add(new_loc)
                    counts[new_loc[0]][new_loc[1]] += 1
                else:
                    to_visit.append(new_loc)
        return { (r,c) : counts[r][c] for (r,c) in tops_attainable }
    
    def sum_ratings(self):
        return sum( sum(self.count_paths_from(l).values()) for l in self.trail_heads() )


def main(second_flag):
    with open("input10.txt") as f:
        terrain = Parse(f)
    if not second_flag:
        return terrain.brute_force()
    return terrain.sum_ratings()
