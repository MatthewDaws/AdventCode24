import pytest
import os

import advent.day23 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test23.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    ns = set(p.network.neighbours_of("aq"))
    assert "cg" in ns
    assert "yn" in ns

@pytest.fixture
def in1(eg1):
    return day.Parse(eg1)

def test_find_triangles_with_t(in1):
    triples = in1.find_triangles_with_t()
    assert len(triples) == 7

def test_find_maximum_clique(in1):
    clique = in1.find_maximum_clique()
    assert clique == {"co","de","ka","ta"}

def test_password(in1):
    assert in1.password() == "co,de,ka,ta"
    