import pytest
import os

import advent.day8 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test8.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert len(p.locations) == 2
    assert p.locations["A"] == [(5,6), (8,8), (9,9)]
    assert p.rows == 12
    assert p.columns == 12

@pytest.fixture
def in1(eg1):
    yield day.Parse(eg1)

def test_antinotes(in1):
    x = in1.antinodes((5,6), (7,7))
    assert x == [(3,5), (9,8)]

def test_all_antinodes(in1):
    pass

def test_count_all_antinodes(in1):
    assert len(in1.find_all_antinodes()) == 14

def test_count_find_all_line_points(in1):
    assert len(in1.find_all_line_points()) == 34
    