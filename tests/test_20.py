import pytest
import os

import advent.day20 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test20.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert p.start == (3,1)
    assert p.end == (7,5)

@pytest.fixture
def in1(eg1):
    return day.Parse(eg1)

def test_find_path(in1):
    assert len(in1.find_path()) == 85

def test_find_cheats(in1):
    it = in1.find_cheats()
    assert next(it) == ((3,1), (3,3), 4)

def test_group_cheats(in1):
    groups = in1.group_cheats()
    assert groups[2] == 14
    assert groups[12] == 3
    assert sum(groups.values()) == 44

def test_count_cheats_at_least(in1):
    assert in1.count_cheats_at_least(20) == 5
    assert in1.count_cheats_at_least(21) == 4
    assert in1.count_cheats_at_least(2) == 44

def test_count_cheats_at_least_longer_cheats(in1):
    assert in1.count_cheats_at_least(76, 20) == 3
    assert in1.count_cheats_at_least(75, 20) == 3
    assert in1.count_cheats_at_least(74, 20) == 7
    assert in1.count_cheats_at_least(73, 20) == 7
    assert in1.count_cheats_at_least(72, 20) == 29
    assert in1.count_cheats_at_least(71, 20) == 29
