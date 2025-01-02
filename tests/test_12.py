import pytest
import os

import advent.day12 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test12.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert p.rows == 10
    assert p.columns == 10
    assert p.entry(0,0) == "R"
    assert p.entry(3,5) == "C"

@pytest.fixture
def in1(eg1):
    return day.Parse(eg1)

def test_neighbours(in1):
    assert list(in1.neighbours(0,0)) == [(1,0,"R"), (0,1,"R")]

def test_find_plots(in1):
    p = in1.find_plots()
    assert p.find((0,0)) == p.find((1,1))
    assert p.find((0,0)) != p.find((2,0))
    for ss in p.as_sets():
        if (7,0) in ss:
            assert set(ss) == {(7,0),(8,0),(9,0),(9,1),(9,2)}

def test_perimeter(in1):
    assert in1.perimeter({(0,0)}) == 4
    assert in1.perimeter({(0,0),(1,0),(0,1)}) == 8

def test_price(in1):
    assert in1.price() == 1930

def test_sides(in1):
    p = in1.find_plots()
    for ss in p.as_sets():
        if (7,0) in ss:
            assert in1.sides(ss) == 6

def test_discount_price(in1):
    assert in1.discount_price() == 1206

@pytest.fixture
def in2():
    return day.Parse(["EEEEE", "EXXXX", "EEEEE", "EXXXX", "EEEEE"])

def test_discount_price2(in2):
    assert in2.discount_price() == 236

@pytest.fixture
def in3():
    with open(os.path.join("tests", "test12a.txt")) as f:
        yield day.Parse(f)

def test_discount_price3(in3):
    assert len(in3.find_plots().as_sets()) == 3
    # 16 + 16 + 28*12
    assert in3.discount_price() == 368
