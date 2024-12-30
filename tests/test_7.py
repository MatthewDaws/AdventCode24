import pytest
import os

import advent.day7 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test7.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert p.data[0][0] == 190
    assert p.data[0][1] == [10,19]
    assert p.data[5] == (161011, [16, 10, 13])
    assert len(p.data) == 9

@pytest.fixture
def in1(eg1):
    yield day.Parse(eg1)

def test_solution(in1):
    assert in1.solution(in1.data[0]) == "*"
    assert in1.solution(in1.data[2]) is None
    assert in1.solution(in1.data[8]) == "+*+"

def test_sum_can_solve(in1):
    assert in1.sum_can_solve() == 3749

def test_solution_with_concat(in1):
    assert in1.solution(in1.data[0], True) == "*"
    assert in1.solution(in1.data[2], True) is None
    assert in1.solution(in1.data[8], True) == "+*+"
    assert in1.solution(in1.data[3], True) == "|"

def test_sum_can_solve_with_concat(in1):
    assert in1.sum_can_solve(True) == 11387
