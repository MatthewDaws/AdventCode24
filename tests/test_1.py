import pytest
import os

import advent.day1 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test1.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert p[0] == (1,3)
    assert p[2] == (3,3)

@pytest.fixture
def locs1(eg1):
    yield day.Parse(eg1)

def test_distance(locs1):
    assert locs1.distance == 11

def test_locate(locs1):
    assert locs1.locate_in_right(3) == 0
    assert locs1.locate_in_right(4) == 3
    assert locs1.locate_in_right(2) == -1

def test_counts(locs1):
    assert locs1.count_in_right(3) == 3
    assert locs1.count_in_right(2) == 0
    assert locs1.count_in_right(9) == 1

def test_similarity_score(locs1):
    assert locs1.similarity_score() == 31
    