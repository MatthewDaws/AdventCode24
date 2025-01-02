import pytest
import os

import advent.utils.disjointset as util

def test_init():
    d = util.DisjointSet("abcd")
    assert d.entries == {"a", "b", "c", "d"}

@pytest.fixture
def ds1():
    d = util.DisjointSet()
    d.add(1)
    d.add(5)
    d.add(7)
    d.add(7)
    return d

def test_adding_containment(ds1):
    d = ds1
    assert d.entries == {5,7,1}
    assert d.as_sets() == { frozenset({x}) for x in [1,5,7] }
    assert d.contains(5)
    assert not d.contains(2)

def test_find(ds1):
    assert ds1.find(1) != ds1.find(7)
    assert ds1.find(1) == ds1.find(1)
    with pytest.raises(KeyError):
        ds1.find(2)

def test_union(ds1):
    d = ds1
    d.union(1,7)
    assert d.find(1) == d.find(7)
    assert d.find(1) != d.find(5)
    with pytest.raises(KeyError):
        d.union(1,2)
    assert d.as_sets() == { frozenset({1,7}), frozenset({5}) }
    d.union(5,7)
    assert d.find(1) == d.find(7)
    assert d.find(1) == d.find(5)
    d.union(1,7)
    assert d.as_sets() == { frozenset({1,5,7}) }
    assert d.find_depth() == 1

def test_larger():
    d = util.DisjointSet(range(100))
    for x in range(1,100):
        d.union(0, x)
    ss = list(d.as_sets())
    assert len(ss) == 1
    assert len(ss[0]) == 100
    assert d.find_depth() == 1
