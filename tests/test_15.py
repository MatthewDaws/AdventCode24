import pytest
import os

import advent.day15 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test15.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert p.rows == 10
    assert p.columns == 10
    assert p.at(2,3) == "."
    assert p.at(0,0) == "#"
    assert len(p.instructions) == 70*10

@pytest.fixture
def in1(eg1):
    return day.Parse(eg1)

def test_robot_location(in1):
    assert in1.robot_location() == (4,4)

def test_move(in1):
    assert in1.move(in1._grid, (2,3), (-1,0)) == None
    assert in1.move(in1._grid, (1,1), (0,1)) == in1._grid
    g = in1.move(in1._grid, (1,2), (0,1))
    assert "".join(g[1]) == "#...O.O.O#"
    g = in1.move(in1._grid, (2,3), (1,0))
    assert "".join(g[r][3] for r in range(3,7)) == ".OO."
    assert in1.move(in1._grid, (1,1), (0,-1)) == None

@pytest.fixture
def in2():
    with open(os.path.join("tests", "test15a.txt")) as f:
        yield day.Parse(f)

def test_grid_without_robot(in2):
    g, p = in2.grid_without_robot()
    assert p == (2,2)
    rows = ["".join(r) for r in g]
    assert rows[0] == "########"
    assert rows[1] == "#..O.O.#"
    assert rows[2] == "##..O..#"
    assert rows[3] == "#...O..#"

def test_run_step(in2):
    g, p = in2.grid_without_robot()
    g1, p1 = in2.run_step(g, p, "<")
    assert g1 == g
    assert p1 == p

def test_run(in2):
    grid = in2.run()
    rows = ["".join(r) for r in grid]
    assert rows[0] == "########"
    assert rows[1] == "#....OO#"
    assert rows[2] == "##.....#"
    assert rows[3] == "#.....O#"
    assert rows[4] == "#.#O...#"
    assert rows[5] == "#...O..#"
    assert rows[6] == "#...O..#"
    assert rows[7] == "########"

def test_GPS_score(in2):
    grid = in2.run()
    assert in2.GPS_score(grid) == 2028

def test_GPS_score1(in1):
    grid = in1.run()
    assert in1.GPS_score(grid) == 10092

def test_double_map(in1):
    in1.double()
    assert in1._grid[3] == "##..[][]....[]..[]##"
    assert in1.robot_location() == (4,8)

def test_grid_to_placements(in1):
    in1.double()
    assert in1.grid_to_placements(in1._grid)[:4] == [(1,6), (1,12), (1,16), (2,14)]

def test_doubled_move_new(in1):
    in1.double()
    assert in1.doubled_move_new(in1._grid, (1,8), (0,-1)) == {(1,6)}
    assert in1.doubled_move_new(in1._grid, (1,9), (0,-1)) == set()
    assert in1.doubled_move_new(in1._grid, (1,2), (0,-1)) == None
    assert in1.doubled_move_new(in1._grid, (5,6), (-1,0)) == {(4,6), (3,6)}

@pytest.fixture
def in3():
    with open(os.path.join("tests", "test15b.txt")) as f:
        p = day.Parse(f)
        p.double()
        yield p

def test_run_step_doubled(in3):
    grid, pos = in3.grid_without_robot()
    assert pos == (3,10)
    in3.set(grid, pos, ".")
    grid, pos = in3.run_step_doubled(grid, pos, "<")
    assert pos == (3,9)
    assert "".join(grid[3]) == "##...[][]...##"
    
def test_double_run3(in3):
    grid = in3.double_run()
    assert "".join(grid[0]) == "##############"
    assert "".join(grid[1]) == "##...[].##..##"
    assert "".join(grid[2]) == "##.....[]...##"
    assert "".join(grid[3]) == "##....[]....##"
    assert "".join(grid[4]) == "##..........##"
    assert "".join(grid[5]) == "##..........##"
    assert "".join(grid[6]) == "##############"

def test_double_run(in1):
    in1.double()
    grid = in1.double_run()
    assert in1.GPS_score(grid) == 9021
