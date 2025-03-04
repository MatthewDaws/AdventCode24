from flask import cli
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

def test_BronKerbosch():
    g = util.Graph()
    for v in range(1, 7):
        g.add_vertex(v)
    def uedge(u, v):
        g.add_directed_edge(u, v)
        g.add_directed_edge(v, u)
    for e in [(1,2), (1,5), (2,3), (2,5), (3,4), (4,5), (4,6)]:
        uedge(*e)

    cliques = list(util.BronKerbosch(g))
    assert [x for x in cliques if len(x) == 3] == [{1,2,5}]
    assert len([x for x in cliques if len(x)==2]) == 4
    assert [x for x in cliques if len(x) > 3 or len(x) < 2] == []

def test_Integer_Priority_Queue():
    q = util.Integer_Priority_Queue()
    assert q.is_empty
    q.add("a", 5)
    assert q.pop() == ("a", 5)
    assert q.is_empty
    q.add("a", 5)
    q.add("b", 10)
    q.add("c", 5)
    e,w = q.pop()
    assert e in "ac"
    assert w == 5
    e,w = q.pop()
    assert e in "ac"
    assert w == 5
    e,w = q.pop()
    assert e == "b"
    assert w == 10
    assert q.is_empty
    q.add("a", 5)
    q.add("b", 10)
    q.add("c", 7)
    q.add("b", 3)
    q.add("c", 4)
    assert q.pop() == ("b",3)
    assert q.pop() == ("c", 4)
    assert q.pop() == ("a", 5)
    assert q.is_empty

def test_shortest_path_unweighted_graph(graph1):
    # 0-1, 0-2, 1-3, 2-3
    dists, prev = util.shortest_path_unweighted(graph1, 0)
    assert dists == {0:0, 1:1, 2:1, 3:2}
    assert prev[1] == 0
    assert prev[2] == 0
    assert prev[3] in {1,2}
