import pytest
import os

import advent.day19 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test19.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert len(p.towels) == 8
    assert p.towels[0] == "r"
    assert p.towels[2] == "b"
    assert len(p.designs) == 8

@pytest.fixture
def in1(eg1):
    return day.Parse(eg1)

def test_count_ways2(in1):
    for d, n in zip(in1.designs, [2,1,4,6,0,1,2,0]):
        assert in1.count_ways2(d) == n

def test_number_designs_possible2(in1):
    assert in1.number_designs_possible2() == 6
