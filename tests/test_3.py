import pytest
import os

import advent.day3 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test3.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert len(p.rows) == 1

@pytest.fixture
def in1(eg1):
    yield day.Parse(eg1)

def test_find_muls(in1):
    assert in1.find_muls("ashamul(3,73)afgs") == [(3,73)]
    assert in1.find_muls(in1.rows[0]) == [(2,4), (5,5), (11,8), (8,5)]

def test_sum_all(in1):
    assert in1.sum_all() == 161

@pytest.fixture
def eg2():
    with open(os.path.join("tests", "test3a.txt")) as f:
        yield f

@pytest.fixture
def in2(eg2):
    yield day.Parse(eg2)

def test_find_muls2(in2):
    assert in2.find_muls(in2.rows[0]) == [(2,4), (5,5), (11,8), (8,5)]
    assert in2.find_muls(in2.rows[0], True) == ([(2,4), (8,5)], False)
    assert in2.sum_all(True) == 48
