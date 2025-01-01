import pytest
import os

import advent.day9 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test9.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert len(p.disk) == 42
    assert p.disk[0] == 0
    assert p.disk[2] is None
    assert p.disk[-1] == 9
    assert p.file_positions[:4] == [(0,2), (5,3), (11,1), (15,3)]
    assert p.gap_positions[:4] == [(2,3), (8,3), (12,3), (18,1)]

@pytest.fixture
def in1(eg1):
    yield day.Parse(eg1)

def test_defrag(in1):
    d = in1.defrag()
    assert len(d) == 28
    assert d[0] == 0
    assert d[2] == 9
    assert d[-1] == 6

def test_checksum(in1):
    assert in1.checksum() == 1928

def test_find_gap(in1):
    gaps = [(2,4), (10,5), (20, 2)]
    assert in1.find_gap(gaps, 6, 100) is None
    assert in1.find_gap(gaps, 2, 1) is None
    assert in1.find_gap(gaps, 1, 100) == 2
    assert gaps[0] == (3,3)
    assert in1.find_gap(gaps, 5, 100) == 10
    assert len(gaps) == 2
    assert gaps[1] == (20,2)

def test_defrag_files(in1):
    f = in1.defrag_files()
    assert f[0] == (0,2)
    assert f[9] == (2,2)

def test_files_checksum(in1):
    assert in1.files_checksum() == 2858
    