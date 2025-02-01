import advent.utils.graphs as graphs
import itertools

class Parse:
    def __init__(self, rows):
        self._network = graphs.Graph()
        def add_vertex(v):
            if v not in self._network.vertices:
                self._network.add_vertex(v)
        for row in rows:
            v1 = row[:2]
            assert row[2] == "-"
            v2 = row[3:5]
            add_vertex(v1)
            add_vertex(v2)
            self._network.add_directed_edge(v1, v2)
            self._network.add_directed_edge(v2, v1)
    
    @property
    def network(self):
        return self._network

    def find_triangles_with_t(self):
        triangles = set()
        for v1 in self._network.vertices:
            if v1[0] != "t":
                continue
            for v2, v3 in itertools.combinations(self._network.neighbours_of(v1), 2):
                if v3 in self._network.neighbours_of(v2):
                    triangles.add( frozenset((v1,v2,v3)) )
        return triangles
    
    def find_maximum_clique(self):
        clique, size = None, None
        for c in graphs.BronKerbosch(self._network):
            if clique is None or len(c) > size:
                size = len(c)
                clique = c
        return clique
    
    def password(self):
        clique = self.find_maximum_clique()
        clique = list(clique)
        clique.sort()
        return ",".join(clique)
    

def main(second_flag):
    with open("input23.txt") as f:
        network = Parse(f)
    if not second_flag:
        triples = network.find_triangles_with_t()
        return len(triples)
    return network.password(), None
