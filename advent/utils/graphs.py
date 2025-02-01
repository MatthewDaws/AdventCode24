class BaseGraph:
    """Just defines an interface for various algorithms"""
    def __init__(self):
        pass

    @property
    def vertices(self):
        pass

    def neighbours_of(self, vertex):
        pass

    def weighted_neighbours_of(self, vertex):
        """Return a list of pairs (neighbour, length_of_edge)"""
        raise NotImplementedError()


class Graph(BaseGraph):
    def __init__(self):
        self._vertices = []
        self._neighbourhoods = dict()

    def add_vertex(self, v):
        if v in self._neighbourhoods:
            raise ValueError(f"Already has vertex '{v}'")
        self._vertices.append(v)
        self._neighbourhoods[v] = []

    def add_directed_edge(self, start, end):
        self._neighbourhoods[start].append(end)

    @property
    def vertices(self):
        return self._vertices
    
    def neighbours_of(self, vertex):
        return self._neighbourhoods[vertex]
    

class WeightedGraph(Graph):
    def __init__(self):
        super().__init__()
        self._weights = dict()

    def add_vertex(self, v):
        super().add_vertex(v)
        self._weights[v] = []

    def add_directed_edge(self, start, end, weight):
        super().add_directed_edge(start, end)
        self._weights[start].append(weight)

    def weighted_neighbours_of(self, vertex):
        return zip(self._neighbourhoods[vertex], self._weights[vertex])

    def __str__(self):
        out = []
        for v in self.vertices:
            line = f"{v}: "
            for u,l in self.weighted_neighbours_of(v):
                line = line + f" ({u},{l})"
            out.append(line)
        return "\n".join(out)
    
def _select_smallest_unvisited(unvisited, shortest_distances):
    minimum = None
    for v in unvisited:
        cd = shortest_distances[v]
        if minimum is None or (cd is not None and cd < minimum):
            minimum = shortest_distances[v]
            vertex = v
    return vertex, minimum


def shortest_path(graph, start):
    """Uses Dijkstra'a algorithm.  `graph` should be a weighted graph."""
    unvisited = {start}
    visited = set()
    shortest_distances = { v : None for v in graph.vertices }
    predecessors = dict(shortest_distances)
    shortest_distances[start] = 0
    while len(unvisited) > 0:
        to_visit, distance = _select_smallest_unvisited(unvisited, shortest_distances)
        if distance is None: # Graph disconnected; trying to find distances to another component
            break
        unvisited.remove(to_visit)
        visited.add(to_visit)
        for u, d in graph.weighted_neighbours_of(to_visit):
            curdist = shortest_distances[u]
            if curdist is None or distance + d < curdist:
                shortest_distances[u] = distance + d
                predecessors[u] = to_visit
                if u not in visited:
                    unvisited.add(u)
    return shortest_distances, predecessors

def shortest_paths_all(graph, start):
    """Uses Dijkstra'a algorithm.  `graph` should be a weighted graph."""
    unvisited = {start}
    visited = set()
    shortest_distances = { v : None for v in graph.vertices }
    predecessors = dict(shortest_distances)
    shortest_distances[start] = 0
    while len(unvisited) > 0:
        to_visit, distance = _select_smallest_unvisited(unvisited, shortest_distances)
        if distance is None: # Graph disconnected; trying to find distances to another component
            break
        unvisited.remove(to_visit)
        visited.add(to_visit)
        for u, d in graph.weighted_neighbours_of(to_visit):
            curdist = shortest_distances[u]
            if curdist == distance + d:
                predecessors[u].add(to_visit)
            if curdist is None or distance + d < curdist:
                shortest_distances[u] = distance + d
                predecessors[u] = {to_visit}
                if u not in visited:
                    unvisited.add(u)
    return shortest_distances, predecessors

def BronKerbosch(graph):
    """Yields all maximal cliques in graph (which is assumed undirected)"""
    tasks = [ (set(), set(graph.vertices), set()) ]
    while len(tasks) > 0:
        clique, options, ignore = tasks.pop()
        if len(options) == 0:
            if len(ignore) == 0:
                yield clique
            continue
        while len(options) > 0:
            v = options.pop()
            ns = set(graph.neighbours_of(v))
            tasks.append((clique | {v}, options & ns, ignore & ns))
            ignore.add(v)