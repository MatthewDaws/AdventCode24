import pytest
import os

import advent.day16 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test16.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert p.end == (1,13)
    assert p.start == (13,1)

@pytest.fixture
def in1(eg1):
    return day.Parse(eg1)

def test_graph(in1):
    assert set( in1.graph.weighted_neighbours_of((1,1,(-1,0))) ) == {
        ((1,2,(0,1)), 1001), ((2,1,(1,0)), 2001) }

def test_shortest_path(in1):
    assert in1.shortest_path() == 7036

@pytest.fixture
def in2():
    with open(os.path.join("tests", "test16a.txt")) as f:
        yield day.Parse(f)

def test_shortest_path2(in2):
    assert in2.shortest_path() == 11048

def test_shortest_paths(in2):
    r, p = in2.shortest_paths()
    assert r == {(1,15,(-1,0)) : 11048}
    assert p[(1,15,(-1,0))] == {(2,15,(-1,0))}

def test_trace_routes(in2):
    r, p = in2.shortest_paths()
    all_locations = in2.trace_routes([(1,15,(-1,0))], p)
    assert len(all_locations) == 64

def test_all_paths_count_locations(in1):
    assert in1.all_paths_count_locations() == 45
    