import pytest
import os

import advent.day24 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test24.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert len(p.variables) == 10
    assert p.variables["x03"] == 1
    assert len(p.wiring) == 36
    assert p.wiring[1].v1 == "y02"
    assert p.wiring[2].v2 == "kpj"
    assert p.wiring[3].cmd == "OR"
    assert p.wiring[4].output == "z01"

@pytest.fixture
def in1(eg1):
    return day.Parse(eg1)

def test_solve(in1):
    in1.solve()
    assert in1.variables["fgs"] == 1
    assert in1.variables["tgd"] == 0

def test_value(in1):
    in1.solve()
    assert in1.value() == 2024

def test_layers(in1):
    layers = in1.layers()
    assert len(layers[0]) == 10
    assert len(layers[1]) == 17
    assert len(layers[2]) == 17
    assert len(layers[3]) == 2
    assert len(layers) == 4

@pytest.fixture
def ac1():
    with open(os.path.join("input24.txt")) as f:
        yield day.Parse(f)

def atest_sort_and_output(ac1):
    wires = ac1.sort_and_output()
    with open("temp.txt", "w") as f:
        for w in wires:
            print("{} {} {} -> {}".format(w.v1, w.cmd, w.v2, w.output), file=f)

def atest_correlate_ordered_to_expected(ac1):
    wires = ac1.sort_and_output()
    ac1.correlate_ordered_to_expected(wires)

def atest_swap_and_run(ac1):
    wires = ac1.sort_and_output()
    swaps = ac1.correlate_ordered_to_expected(wires)
    ac1.implement_swaps(swaps)
    assert ac1.run(5, 123) == 128
    assert ac1.run(15, 1223) == 15+1223
