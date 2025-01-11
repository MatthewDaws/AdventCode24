import pytest
import os

import advent.day14 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test14.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1, True)
    assert len(p.robots) == 12
    assert p.robots[0].pos == (0,4)
    assert p.robots[1].vel == (-1,-3)

@pytest.fixture
def in1(eg1):
    return day.Parse(eg1, True)

def test_positions_after_time(in1):
    p = in1.positions_after_time()
    assert sum( r[0]==6 and r[1]==0 for r in p ) == 2

def test_quadrant_counts(in1):
    p = in1.positions_after_time()
    assert in1.quadrant_counts(p) == [1,3,4,1]

def test_safety_factor(in1):
    assert in1.safety_factor() == 12

def test_print(in1):
    out = in1.print(in1.positions_after_time(0))
    assert out[0] == "#.##......."
    out = in1.print(in1.positions_after_time(100))
    assert out[6] == ".#....#...."

def test_is_h_symmetric(in1):
    pos = [(0,0), (10,0)]
    assert in1.is_horizontally_symmetric(pos)
    pos = [(0,0), (10,0), (5,4)]
    assert in1.is_horizontally_symmetric(pos)
    pos = [(0,0), (10,0), (2,4)]
    assert not in1.is_horizontally_symmetric(pos)

    pos = [(0,0), (10,0), (10,0)]
    assert not in1.is_horizontally_symmetric(pos)
    assert in1.is_weakly_horizontally_symmetric(pos)

def test_period_of_robot(in1):
    in1.period_of_robot(in1.robots[0]) == 20
    assert in1.period_of_all() == 420
