import pytest
import os

import advent.day11 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test11.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    p.reset()
    assert p.counts == {125:1, 17:1}

@pytest.fixture
def in1(eg1):
    p = day.Parse(eg1)
    p.reset()
    return p

def test_blink_number(in1):
    assert in1.blink_number(0) == (1, None)
    assert in1.blink_number(125) == (253000, None)
    assert in1.blink_number(17) == (1, 7)

def test_blink(in1):
    in1.blink()
    assert in1.counts == {253000:1, 1:1, 7:1}

def test_blink_counts(in1):
    for _ in range(6):
        in1.blink()
    assert sum(in1.counts.values()) == 22

def test_solve(in1):
    assert in1.solve(6) == 22
    assert in1.solve(25) == 55312
    