import pytest
import os

import advent.day4 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test4.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert p.rows == 10
    assert p.cols == 10
    assert p.get(1,2) == "A"

@pytest.fixture
def in1(eg1):
    yield day.Parse(eg1)

def test_contains_xmas_dir(in1):
    assert not in1.contains_xmas_in_dir(0,4,0,0)
    assert in1.contains_xmas_in_dir(0,4,1,1)

def test_count(in1):
    assert in1.xmas_count() == 18

def test_has_x_mas(in1):
    assert not in1.has_x_mas(0,0)
    assert in1.has_x_mas(1,2)

def test_count_x_mas(in1):
    assert in1.count_x_mas() == 9
    