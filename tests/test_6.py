import pytest
import os

import advent.day6 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test6.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert p.location == (6,4)
    assert p.grid[1][2] == True
    assert p.grid[3][2] == False
    assert p.direction == day.Dir.UP
    assert p.direction.value == (-1,0)
    assert p.rows == 10
    assert p.columns == 10

@pytest.fixture
def in1(eg1):
    yield day.Parse(eg1)

def test_rotate(in1):
    assert in1.direction.value == (-1,0)
    in1.rotate()
    assert in1.direction.value == (0,1)
    in1.rotate()
    assert in1.direction.value == (1,0)
    in1.rotate()
    assert in1.direction.value == (0,-1)
    in1.rotate()
    assert in1.direction.value == (-1,0)

def test_move(in1):
    assert in1.location == (6,4)
    assert in1.move() == (5,4)
    assert in1.move() == (4,4)
    assert in1.move() == (3,4)
    assert in1.move() == (2,4)
    assert in1.move() == (1,4)
    assert in1.move() == (1,5)

def test_visits_until_leave(in1):
    assert in1.visits_until_leave() == 45

def test_distinct_visits_until_leave(in1):
    assert in1.distinct_visits_until_leave() == 41

def test_does_repeat(in1):
    with pytest.raises(ValueError):
        in1.does_repeat((0,4))
    with pytest.raises(ValueError):
        in1.does_repeat(in1.location)
    assert in1.does_repeat((6,3))
    assert in1.grid[6][3]
    assert not in1.does_repeat((0,0))
    assert in1.grid[0][0]

def test_count_blocking_points(in1):
    assert in1.count_blocking_points() == 6
    