import pytest
import os

import advent.day17 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test17.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert p.A == 729
    assert p.B == 0
    assert p.C == 0
    assert len(p.program) == 6
    assert p.program[0] == 0

@pytest.fixture
def in1(eg1):
    return day.Parse(eg1)

def test_cmds(in1):
    in1.C = 9
    in1.run_single(2, 6)
    assert in1.B == 1
    assert in1._jumped == 0

    in1.B = 29
    in1.run_single(1, 7)
    assert in1.B == 26
    assert in1._jumped == 0

    in1.B = 2024
    in1.C = 43690
    in1.run_single(4, 0)
    assert in1.B == 44354
    assert in1._jumped == 0

    in1.A = 10
    in1._output = []
    in1.run_single(5, 0)
    in1.run_single(5, 1)
    in1.run_single(5, 4)
    assert in1.result == [0,1,2]

def test_small_prog(in1):
    in1.A = 2024
    in1._program = [0,1,5,4,3,0]
    in1.run()
    assert in1.result == [4,2,5,6,7,7,7,7,3,1,0]
    assert in1.A == 0

def test_run(in1):
    in1.run()
    assert in1.result == [4,6,3,5,6,3,5,2,1,0]
    assert ",".join(str(x) for x in in1.result) == "4,6,3,5,6,3,5,2,1,0"

def test_prog(in1):
    in1.A = 64854237
    in1.B = None
    in1.run_single(2,4)
    assert in1.B == 5 # 64854237 % 8  (= A % 8)
    in1.run_single(1,1)
    assert in1.B == 4 # 5 ^ 1   (= B^1)
    in1.run_single(7,5)
    assert in1.C == 4053389 # 64854237 // 16  (= A // 2^B)
    in1.run_single(1,5)
    assert in1.B == 1 # 4 ^ 5  (= B^5)
    in1.run_single(4,0)
    assert in1.B == 4053388 # B^C = 4053389 ^ 1   (= B^C)
    in1._output = []
    in1.run_single(5,5)
    assert in1.result[-1] == 4  # output  B % 8
    in1.run_single(0,3)
    assert in1.A == 8106779  # A // 8
    in1.run_single(3,0)
    assert in1._jumped == 1

@pytest.fixture
def in2():
    with open(os.path.join("tests", "test17a.txt")) as f:
        yield day.Parse(f)

def test_run2(in2):
    in2.A = 117440
    in2.run()
    assert in2.result == [0,3,5,4,3,0]
