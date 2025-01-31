import pytest
import os

import advent.day21 as day

@pytest.fixture
def eg1():
    with open(os.path.join("tests", "test21.txt")) as f:
        yield f

def test_parse(eg1):
    p = day.Parse(eg1)
    assert p.codes[0] == "029A"
    assert len(p.codes) == 5

@pytest.fixture
def in1(eg1):
    return day.Parse(eg1)

def test_numeric_part_code(in1):
    assert in1.numeric_part_code("029A") == 29

def test_optimal_routes_numeric_pad(in1):
    rs = in1.optimal_routes_numeric_pad("029A")
    assert set(rs) == {"<A^A>^^AvvvA", "<A^A^^>AvvvA"}
    rs = in1.optimal_routes_numeric_pad("596A")
    assert set(rs) == {"<^^A^>AvAvvA", "<^^A>^AvAvvA", "^^<A^>AvAvvA", "^^<A>^AvAvvA"}

def test_optimal_routes_keypad(in1):
    assert in1.optimal_routes_keypad("<") == ["v<<A"]
    def to_nice_form(code):
        chs = in1.optimal_routes_keypad(code)
        return set(x.replace("A", "A ") for x in chs)
    assert to_nice_form("<vA") == {"v<<A >A ^>A ", "v<<A >A >^A "}
    assert to_nice_form("v<A") == {"v<A <A >>^A ", "<vA <A >>^A "}
    assert to_nice_form("<A") == {"v<<A >>^A "}
    assert to_nice_form(">A") == {"vA ^A "}
    assert to_nice_form("vA") == {"v<A >^A ", "v<A ^>A ", "<vA >^A ", "<vA ^>A "}

def test_build_lookup(in1):
    lookup = in1.build_lookup()
    assert lookup[0]["<A"] == (8, "v<<A>>^A")
    assert lookup[1]["<vA"] == (21, "v<<A>A^>A") # Dodgy test; could end ">^A"

def test_shortest_implementation_keypad(in1):
    in1.build_lookup()
    # <vA<AA>>^AvAA<^A>A  <v<A>>^AvA^A  <vA>^A<v<A>^A>AAvA^A  <v<A>A>^AAAvA<^A>A
    # v<<A>>^A            <A>A          vA<^AA>A              <vAAA>^A
    # <A                  ^A            >^^A                  vvvA
    assert in1.shortest_implementation_keypad("<A") == 18
    assert in1.shortest_implementation_keypad("^A") == 12
    assert in1.shortest_implementation_keypad(">^^A") == 20
    assert in1.shortest_implementation_keypad("vvvA") == 18

def test_shortest_path_from_lookup(in1):
    in1.build_lookup()
    assert in1.shortest_path_from_lookup("029A") == 68
    assert in1.shortest_path_from_lookup("980A") == 60

def test_complexity_from_lookup(in1):
    in1.build_lookup()
    assert in1.complexity_from_lookup() == 126384

def test_convert_string_to_commands(in1):
    x = in1.optimal_routes_numeric_pad("379A")[1]
    assert in1.convert_string_to_commands(x) == ["^A", "<<^^A", ">>A", "vvvA"]
    assert in1.convert_string_to_commands("<A^^AA") == ["<A", "^^A", "A"]
