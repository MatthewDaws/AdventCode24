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

def test_concat(in1):
    assert in1.concat(5, 6) == 56
    assert in1.concat(3, 45) == 345
    assert in1.concat(123, 4567) == 1234567

def test_solution_with_concat_fast(in1):
    assert in1.solution_concat_fast(in1.data[0]) == "*"
    assert in1.solution_concat_fast(in1.data[2]) is None
    assert in1.solution_concat_fast(in1.data[8]) == "+*+"
    assert in1.solution_concat_fast(in1.data[3]) == "|"

def test_sum_can_solve_with_concat_fast(in1):
    assert in1.sum_can_solve_fast() == 11387



def atest():
    import random, time
    values = []
    for _ in range(2):
        values.append( [random.randint(1,1000000) for _ in range(1000000)] )
    for _ in range(5):
        st = time.monotonic()
        out = [int(str(i)+str(j))  for i,j in zip(values[0], values[1])]
        en = time.monotonic()
        print(en-st)
    for _ in range(5):
        st = time.monotonic()
        out1 = [concat(i,j) for i,j in zip(values[0], values[1])]
        en = time.monotonic()
        print(en-st)
    assert out == out1
    assert False
