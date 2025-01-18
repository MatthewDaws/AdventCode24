import pytest
import os

import advent.day18 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test18.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1, True)
    assert len(p.places) == 25

@pytest.fixture
def in1(eg1):
    return day.Parse(eg1, True)

def test_grid(in1):
    g = in1.build_grid(12)
    assert "".join(g[1]) == "..#..#."

def test_graph(in1):
    grid = in1.build_grid(12)
    graph = in1.build_graph(grid)
    assert graph.neighbours_of((0,0)) == [(1,0), (0,1)]
    assert graph.neighbours_of((1,1)) == [(0,1), (1,0), (1,2)]

def test_shortest_path(in1):
    assert in1.shortest_path(12) == 22

def test_find_first_no_path(in1):
    assert in1.find_first_no_path(12) == (6,1)

def test_find_first_no_path2(in1):
    assert in1.find_first_no_path2(12) == (6,1)

def test_find_all_paths(in1):
    grid = in1.build_grid(12)
    all_paths = in1.find_all_paths(grid)
    assert len(all_paths) == 40

def test_find_first_no_path3(in1):
    assert in1.find_first_no_path3(12) == (6,1)
