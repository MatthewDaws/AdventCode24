import pytest

import advent.utils.graphs as util

@pytest.fixture
def graph1():
    g = util.Graph()
    for i in range(4):
        g.add_vertex(i)
    g.add_directed_edge(0,1)
    g.add_directed_edge(0,2)
    g.add_directed_edge(1,3)
    g.add_directed_edge(2,3)
    return g

def test_Graph(graph1):
    assert graph1.vertices == [0,1,2,3]
    assert graph1.neighbours_of(0) == [1,2]
    assert graph1.neighbours_of(1) == [3]
    assert graph1.neighbours_of(2) == [3]
    assert graph1.neighbours_of(3) == []

    with pytest.raises(ValueError):
        graph1.add_vertex(2)
    with pytest.raises(KeyError):
        graph1.neighbours_of(5)

def test_Weighted_Graph():
    g = util.WeightedGraph()
    for i in range(4):
        g.add_vertex(i)
    g.add_directed_edge(0,1,5)
    g.add_directed_edge(0,2,3)

    assert g.neighbours_of(0) == [1, 2]
    assert list(g.weighted_neighbours_of(0)) == [(1,5), (2,3)]

@pytest.fixture
def wiki_eg():
    # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#/media/File:Dijkstra_Animation.gif
    g = util.WeightedGraph()
    for i in range(1, 7):
        g.add_vertex(i)
    for u,v,w in [(1,2,7), (1,3,9), (1,6,14), (2,3,10), (2,4,15), (3,4,11), (3,6,2), (4,5,6), (5,6,9)]:
        g.add_directed_edge(u,v,w)
        g.add_directed_edge(v,u,w)
    return g

def test_shortest_path(wiki_eg):
    d, p = util.shortest_path(wiki_eg, 1)
    assert d == {1:0, 2:7, 3:9, 4:20, 5:20, 6:11}
    assert p == {1:None, 2:1, 3:1, 4:3, 5:6, 6:3}

def test_shortest_paths_all(wiki_eg):
    d, p = util.shortest_paths_all(wiki_eg, 1)
    assert d == {1:0, 2:7, 3:9, 4:20, 5:20, 6:11}
    assert p == {1:None, 2:{1}, 3:{1}, 4:{3}, 5:{6}, 6:{3}}
