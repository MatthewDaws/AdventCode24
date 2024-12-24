import pytest
import os

import advent.day2 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test2.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert len(p) == 6
    assert p[1] == [1,2,7,8,9]

@pytest.fixture
def reports1(eg1):
    yield day.Parse(eg1)

def test_safe(reports1):
    assert reports1.safe(0)
    assert not reports1.safe(1)
    assert not reports1.safe(2)
    assert not reports1.safe(3)
    assert not reports1.safe(4)
    assert reports1.safe(5)

def test_count_safe(reports1):
    assert reports1.count_safe() == 2

def test_find_bad_levels(reports1):
    assert reports1.find_bad_levels(0) == []
    assert reports1.find_bad_levels(1) == [1]
    assert reports1.find_bad_levels(2) == [2]
    assert reports1.find_bad_levels(3) == [1]
    assert reports1.find_bad_levels(4) == [2]
    assert reports1.find_bad_levels(5) == []

def test_brute_force_check_single_removal(reports1):
    assert reports1.brute_force_check_single_removal(0)
    assert not reports1.brute_force_check_single_removal(1)
    assert not reports1.brute_force_check_single_removal(2)
    assert reports1.brute_force_check_single_removal(3)
    assert reports1.brute_force_check_single_removal(4)
    assert reports1.brute_force_check_single_removal(5)

def test_single_removal(reports1):
    assert reports1.check_single_removal(0)
    assert not reports1.check_single_removal(1)
    assert not reports1.check_single_removal(2)
    assert reports1.check_single_removal(3)
    assert reports1.check_single_removal(4)
    assert reports1.check_single_removal(5)
