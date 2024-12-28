import pytest
import os

import advent.day5 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test5.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert len(p.books) == 6
    assert len(p.rules) == 21
    assert p.rules[1] == (97, 13)
    assert p.books[2] == [75,29,13]
    assert p.rules_dict[97] == {13, 61, 47,29, 53,75}

@pytest.fixture
def in1(eg1):
    yield day.Parse(eg1)

def test_is_ordered(in1):
    assert in1.is_ordered(in1.books[0])
    assert in1.is_ordered(in1.books[1])
    assert in1.is_ordered(in1.books[2])
    assert not in1.is_ordered(in1.books[3])
    assert not in1.is_ordered(in1.books[4])
    assert not in1.is_ordered(in1.books[5])

def test_sum_middles_of_ordered(in1):
    assert in1.sum_middles_of_ordered() == 143

def test_Page(in1):
    a = in1.Page(47, in1)
    b = in1.Page(53, in1)
    assert a < b
    assert not b < a
    c = in1.Page(29, in1)
    assert b < c
    assert not c < b

def test_reorder(in1):
    pages = in1.reorder(in1.books[3])
    assert pages == [97,75,47,61,53]
    pages = in1.reorder(in1.books[4])
    assert pages == [61,29,13]
    pages = in1.reorder(in1.books[5])
    assert pages == [97,75,47,29,13]

def test_sum_reordered(in1):
    assert in1.sum_middles_needed_reordering() == 123
    