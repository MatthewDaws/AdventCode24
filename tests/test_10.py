import pytest
import os

import advent.day10 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test10.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert p.rows == 8
    assert p.columns == 8
    assert p.grid[1][2] == 1

@pytest.fixture
def in1(eg1):
    yield day.Parse(eg1)

def test_trail_heads(in1):
    assert list(in1.trail_heads())[:3] == [(0,2), (0,4), (2,4)]

def test_steps_up(in1):
    assert in1.steps_up((0,2)) == { (0,3), (1,2) }
    assert in1.steps_up((2,0)) == { (3,0) }

def test_brute_force_from(in1):
    assert len(in1.brute_force_from((0,2))) == 5

def test_brute_force(in1):
    assert in1.brute_force() == 36

def test_count_paths_from(in1):
    d = in1.count_paths_from((0,2))
    assert sum(d.values()) == 20
    assert sum(in1.count_paths_from((0,4)).values()) ==24    
    assert sum(in1.count_paths_from((2,4)).values()) == 10

def test_sum_ratings(in1):
    assert in1.sum_ratings() == 81
    