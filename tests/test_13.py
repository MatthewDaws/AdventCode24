import pytest
import os

import advent.day13 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test13.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert len(p.machines) == 4
    assert p.machines[0].A == (94,34)
    assert p.machines[0].B == (22,67)
    assert p.machines[0].prize == (8400,5400)

@pytest.fixture
def in1(eg1):
    return day.Parse(eg1)

def test_solve(in1):
    soln, kernel = in1.solve(in1.machines[0])
    assert soln == (80, 40)
    assert kernel is None
    assert in1.solve(in1.machines[1]) == (None, None)
    soln, kernel = in1.solve(in1.machines[2])
    assert soln == (38, 86)
    assert kernel is None
    assert in1.solve(in1.machines[3]) == (None, None)

def test_minimal_cost(in1):
    assert in1.minimal_cost() == 480

@pytest.fixture
def in2(in1):
    in1.adjust_units()
    return in1

def test_2nd_case(in2):
    assert in2.solve(in2.machines[0]) == (None, None)
    assert in2.solve(in2.machines[2]) == (None, None)
    soln, kernel = in2.solve(in2.machines[1])
    assert soln is not None
    assert kernel is None
    soln, kernel = in2.solve(in2.machines[3])
    assert soln is not None
    assert kernel is None
