import pytest
import os

import advent.day25 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test25.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert p.keys == [[5,0,2,1,3], [4,3,4,0,2], [3,0,2,0,1]]
    assert p.locks == [[0,5,3,4,3], [1,2,0,5,3]]

@pytest.fixture
def in1(eg1):
    return day.Parse(eg1)

def test_overlap(in1):
    assert in1.overlap(in1.locks[0], in1.keys[0])
    assert in1.overlap(in1.locks[0], in1.keys[1])
    assert not in1.overlap(in1.locks[0], in1.keys[2])

def test_fit_count(in1):
    assert in1.fit_count() == 3
    