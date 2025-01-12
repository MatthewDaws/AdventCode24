from sympy import N
from .utils import graphs

class Parse:
    def __init__(self, rows):
        self._grid = [ row.strip() for row in rows ]
        self._process()
        self._build_graph_2()

    def _process(self):
        self._grid = [ list(r) for r in self._grid ]
        for r, row in enumerate(self._grid):
            for c, entry in enumerate(row):
                if entry == "E":
                    self.end = (r,c)
                if entry == "S":
                    self.start = (r,c)
        self._grid[self.end[0]][self.end[1]] = "."
        self._grid[self.start[0]][self.start[1]] = "."

    def _build_graph(self):
        """Builds a graph in a naive way: vertices and point/direction pairs, and at each vertex we either move in the
        given direction, or rotate.  This ends up being too slow."""
        next_orientation_from = {(1,0):(0,1), (0,1):(-1,0), (-1,0):(0,-1), (0,-1):(1,0)}
        self.graph = graphs.WeightedGraph()
        for r, row in enumerate(self._grid):
            for c, entry in enumerate(row):
                if entry == ".":
                    for d in next_orientation_from.keys():
                        self.graph.add_vertex( (r,c,d) )
                    for d1, d2 in next_orientation_from.items():
                        self.graph.add_directed_edge( (r,c,d1), (r,c,d2), 1000 )
                        self.graph.add_directed_edge( (r,c,d2), (r,c,d1), 1000 )
                    for d in next_orientation_from.keys():
                        rr, cc = r + d[0], c + d[1]
                        if self._grid[rr][cc] == ".":
                            self.graph.add_directed_edge( (r,c,d), (rr,cc,d), 1 )

    rotation_cost = { (1,0) : {(1,0):0, (0,1):1000, (0,-1):1000, (-1,0):2000},
                     (-1,0) : {(1,0):2000, (0,1):1000, (0,-1):1000, (-1,0):0},
                     (0,1) : {(1,0):1000, (0,1):0, (0,-1):2000, (-1,0):1000},
                     (0,-1) : {(1,0):1000, (0,1):2000, (0,-1):0, (-1,0):1000} }

    def _build_graph_2(self):
        """Builds a smaller graph: at a given position, it's only worth rotating if we can then move, so build this
        into the graph."""
        self.graph = graphs.WeightedGraph()
        for r, row in enumerate(self._grid):
            for c, entry in enumerate(row):
                if entry == ".":
                    for d in self.rotation_cost.keys():
                        self.graph.add_vertex( (r,c,d) )
                    for d in self.rotation_cost.keys():
                        rr, cc = r + d[0], c + d[1]
                        if self._grid[rr][cc] == ".":
                            for dd in self.rotation_cost.keys():
                                self.graph.add_directed_edge( (r,c,dd), (rr,cc,d), 1 + self.rotation_cost[dd][d] )                    

    def shortest_path(self):
        v = (*self.start, (0,1))
        distances, p = graphs.shortest_path(self.graph, v)
        choices = [ distances[*self.end,d] for d in [(1,0), (0,1), (-1,0), (0,1)] ]
        choices = [ d for d in choices if d is not None ]
        return min(choices)
    
    @staticmethod
    def trace_routes(starts, preds):
        to_visit = set(starts)
        vertices_seen = set()
        while len(to_visit) > 0:
            vertex = to_visit.pop()
            vertices_seen.add(vertex)
            if preds[vertex] == None:
                continue
            for v in preds[vertex]:
                if v not in vertices_seen:
                    to_visit.add(v)
        return set(v[:2] for v in vertices_seen)

    def shortest_paths(self):
        v = (*self.start, (0,1))
        distances, preds = graphs.shortest_paths_all(self.graph, v)
        routes = dict()
        for d in [(1,0), (0,1), (-1,0), (0,1)]:
            dist = distances[*self.end,d]
            if dist is not None:
                routes[(*self.end,d)] = dist
        min_distance = min(routes.values())
        routes = {k:v for k,v in routes.items() if v==min_distance}
        return routes, preds

    def all_paths_count_locations(self):
        all_locations = self.trace_routes(*self.shortest_paths())
        return len(all_locations)
    

def main(second_flag):
    with open("input16.txt") as f:
        maze = Parse(f)
    if not second_flag:
        return maze.shortest_path()
    return maze.all_paths_count_locations()
