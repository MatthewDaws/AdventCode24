import stat
import advent.utils.graphs as graphs

class Parse:
    def __init__(self, rows, debug=False):
        self._places = []
        for row in rows:
            x,y = row.strip().split(",")
            self._places.append( (int(x), int(y)) )
        if debug:
            self._size = 7
        else:
            self._size = 71


    @property
    def places(self):
        return self._places
    
    def build_grid(self, steps=1024):
        self._grid = [["." for _ in range(self._size)] for _ in range(self._size)]
        for i in range(steps):
            x, y = self._places[i]
            self._grid[y][x] = "#"
        return self._grid
    
    @staticmethod
    def build_graph(grid):
        size = len(grid)
        g = graphs.WeightedGraph()
        for y in range(size):
            for x in range(size):
                g.add_vertex((x,y))
        deltas = [(-1,0), (1,0), (0,-1), (0,1)]
        for y in range(size):
            for x in range(size):
                if grid[y][x] != ".":
                    continue
                for dx, dy in deltas:
                    xx, yy = x+dx, y+dy
                    if xx >= 0 and yy >= 0 and xx < size and yy < size and grid[yy][xx] == ".":
                        g.add_directed_edge((x,y), (xx,yy), 1)
        return g                        
    
    def shortest_path(self, steps=1024):
        grid = self.build_grid(steps)
        graph = self.build_graph(grid)
        distances, preds = graphs.shortest_path(graph, (0,0))
        return distances[ (self._size-1, self._size-1) ]

    @staticmethod
    def connected_component(grid):
        deltas = [(-1,0), (1,0), (0,-1), (0,1)]
        size = len(grid)
        cc = [[e=="#" for e in r] for r in grid]
        to_visit = [(0,0)]
        while len(to_visit) > 0:
            (x,y) = to_visit.pop()
            if cc[y][x]:
                continue
            for dx, dy in deltas:
                xx, yy = x+dx, y+dy
                if xx >= 0 and yy >= 0 and xx < size and yy < size and not cc[yy][xx]:
                    to_visit.append((xx,yy))
            cc[y][x] = True
        return cc[-1][-1]

    def find_first_no_path(self, start_steps = 1024):
        extra = 1
        grid = self.build_grid(start_steps)
        while True:
            x, y = self._places[start_steps + extra - 1]
            grid[y][x] = "#"
            graph = self.build_graph(grid)
            distances, preds = graphs.shortest_path(graph, (0,0))
            d = distances[ (self._size-1, self._size-1) ]
            #d = self.shortest_path(start_steps + extra)
            if d is None:
                return self._places[start_steps + extra - 1]
            extra += 1

    def find_first_no_path2(self, start_steps = 1024):
        extra = 1
        grid = self.build_grid(start_steps)
        while True:
            x, y = self._places[start_steps + extra - 1]
            grid[y][x] = "#"
            if not self.connected_component(grid):
                return self._places[start_steps + extra - 1]
            extra += 1

    @staticmethod
    def find_all_paths(grid):
        deltas = [(-1,0), (1,0), (0,-1), (0,1)]
        size = len(grid)
        partial_paths = [ (set(), (0,0)) ]
        paths = []
        while len(partial_paths) > 0:
            pp, end_pt = partial_paths.pop()
            if end_pt == (size-1, size-1):
                newpp = set(pp)
                newpp.add(end_pt)
                paths.append(newpp)
                continue
            for dx, dy in deltas:
                xx, yy = end_pt[0]+dx, end_pt[1]+dy
                if xx >= 0 and yy >= 0 and xx < size and yy < size and grid[yy][xx] == "." and (xx,yy) not in pp:
                    newpp = set(pp)
                    newpp.add(end_pt)
                    partial_paths.append( (newpp, (xx,yy)) )
        return paths

    def find_first_no_path3(self, start_steps = 1024):
        grid = self.build_grid(start_steps)
        all_paths = self.find_all_paths(grid)
        extra = 0
        while True:
            pt = self._places[start_steps + extra]
            all_paths = [path for path in all_paths if pt not in path]
            if len(all_paths) == 0:
                return pt
            extra += 1


def main(second_flag):
    with open("input18.txt") as f:
        places = Parse(f)
    if not second_flag:
        return places.shortest_path()
    #return places.find_first_no_path3(), None
    return places.find_first_no_path2(), None
    #return places.find_first_no_path(), None
