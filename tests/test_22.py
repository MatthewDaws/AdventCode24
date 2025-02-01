import pytest
import os

import advent.day22 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test22.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert len(p.secrets) == 4
    assert p.secrets[2] == 100

@pytest.fixture
def in1(eg1):
    return day.Parse(eg1)

def test_next_secret():
    assert day.Parse.next_secret(123) == 15887950
    expected = [15887950, 16495136, 527345, 704524, 1553684, 12683156, 11100544, 12249484, 7753432, 5908254]
    s = 123
    for e in expected:
        s = day.Parse.next_secret(s)
        assert s == e

def test_sum_iterations(in1):
    assert in1.sum_iterations() == 37327623

def test_prices_changes():
    p = day.Parse.prices_changes(123, 10)
    assert p[0] == (0, -3)
    assert p[1] == (6, 6)
    assert p[8] == (2, -2)

def test_to_quads():
    p = day.Parse.prices_changes(123, 10)
    quads, values = day.Parse.to_quads(p)
    assert quads[0] == (-3,6,-1,-1)
    assert values[0] == 4
    assert quads[2] == (-1,-1,0,2)
    assert values[2] == 6

def test_quad_values_to_initial_pattern_lookup():
    p = day.Parse.prices_changes(123, 10)
    quads, values = day.Parse.to_quads(p)
    lookup = day.Parse.quad_values_to_initial_pattern_lookup(quads, values)
    assert lookup[(-1,-1,0,2)] == 6

@pytest.fixture
def in2():
    with open(os.path.join("tests", "test22a.txt")) as f:
        yield day.Parse(f)

def test_compute_lookups(in2):
    ls = in2.compute_lookups()
    instruction = (-2,1,-1,3)
    assert in2.bananas_from(instruction, ls) == 23

def test_best_instruction(in2):
    assert in2.best_instruction() == 23
    