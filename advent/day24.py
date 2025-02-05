"""
For the 2nd part, I think we build an adder in this way:

- a XOR b   is a+b mod 2
- a AND b   is the carry of a+b
- If we have a carry from a previous addition, then the next bit is
   (a XOR b) XOR carry
- the new carry is (a AND b) OR ((a XOR b) AND carry)

So the general pattern is

xi XOR yi  ->  t1
xi AND yi  ->  t2
t1 XOR ci  ->  zi
t1 AND ci  ->  t3
t2 OR t3   ->  c(i+1)

The start and end special cases are

x0 XOR y0  ->  z0
x0 AND y0  ->  c1

c(n+1)  ==  z(n+1)

With n=44 we have 2 + 5 * 44 = 222 which is what we find.
"""

import random
import re
from collections import namedtuple

Wire = namedtuple("Wire", ["v1", "cmd", "v2", "output"])

class Parse:
    def __init__(self, rows):
        self._variables = dict()
        for row in rows:
            if row.strip() == "":
                break
            v = row[:3]
            assert row[3:5] == ": "
            self._variables[v] = int(row[5])
        cmds_prog = re.compile("(.*)\\s(.*)\\s(.*) -> (.*)")
        self._wiring = []
        for row in rows:
            m = cmds_prog.match(row.strip())
            self._wiring.append(Wire(m.group(1), m.group(2), m.group(3), m.group(4)))

    @property
    def variables(self):
        return self._variables
    
    @property
    def wiring(self):
        return self._wiring

    def solve(self):
        wiring = self._wiring
        while len(wiring) > 0:
            unsolved_wires = []
            for wire in wiring:
                if wire.v1 in self._variables and wire.v2 in self._variables:
                    if wire.output in self._variables:
                        print(wire)
                        print(self._variables[wire.output])
                        raise AssertionError()
                    v1 = self._variables[wire.v1]
                    v2 = self._variables[wire.v2]
                    if wire.cmd == "OR":
                        self._variables[wire.output] = v1 | v2
                    elif wire.cmd == "AND":
                        self._variables[wire.output] = v1 & v2
                    elif wire.cmd == "XOR":
                        self._variables[wire.output] = v1 ^ v2
                    else:
                        raise NotImplementedError() 
                else:
                    unsolved_wires.append(wire)
            wiring = unsolved_wires

    def value(self):
        value = 0
        pow2 = 1
        index = 0
        while True:
            v = "z{:02}".format(index)
            if v in self._variables:
                value += pow2 * self._variables[v]
            else:
                return value
            pow2 += pow2
            index += 1

    def layers(self):
        """Sort the logic gates into the order we solve them in: for trying to understand the 2nd part."""
        layers = []
        seen = set( self._variables.keys() )
        layers.append( set(seen) )
        wiring = self._wiring
        while len(wiring) > 0:
            unsolved_wires = []
            next_layer = set()
            for wire in wiring:
                if wire.v1 in seen and wire.v2 in seen:
                    next_layer.add(wire.output)
                    seen.add(wire.output)
                else:
                    unsolved_wires.append(wire)
            layers.append(next_layer)
            wiring = unsolved_wires
        return layers
    
    def sort_and_output(self):
        """Try to put `xi XOR yi`, and `xi AND yi`, in order, putting as many other logic gates
        as we can in between.  Alphabetically sorts the inputs."""
        seen_variables = set()
        wires_left = list(self._wiring)
        index = 0
        ordered_wires = []

        def add_wire(wire):
            v1, v2 = wire.v1, wire.v2
            seen_variables.add(v1)
            seen_variables.add(v2)
            seen_variables.add(wire.output)
            if v1 > v2:
                v1, v2 = v2, v1
            ordered_wires.append( Wire(v1, wire.cmd, v2, wire.output) )
        def push_wires():
            left_wires = list(wires_left)
            i = 0
            while i < len(left_wires):
                wire = left_wires[i]
                if wire.v1 in seen_variables and wire.v2 in seen_variables:
                    add_wire(wire)
                    del left_wires[i]
                    i = 0
                else:
                    i += 1
            return left_wires
        def add_next_xiyi():
            left_wires = []
            seek = {"x{:02}".format(index), "y{:02}".format(index)}
            found = []
            for wire in wires_left:
                if {wire.v1, wire.v2} == seek:
                    found.append(wire)
                else:
                    left_wires.append(wire)
            for w in found:
                add_wire(w)
            return left_wires

        while len(wires_left) > 0:
            wires_left = add_next_xiyi()
            wires_left = push_wires()
            index += 1
        return ordered_wires
    
    @staticmethod
    def _chunk(ordered_wires, index):
        start, end = None, None
        for i, wire in enumerate(ordered_wires):
            try:
                xy = int(wire.v1[1:])
                if xy == index and start is None:
                    start = i
                if xy == index + 1:
                    end = i
                    break
            except ValueError:
                pass
        return set(ordered_wires[start:end])

    @staticmethod
    def _find_remove_xy_cmd(chunk, cmd):
        for wire in chunk:
            if wire.cmd == cmd and wire.v1[0] == "x" and wire.v2[0] == "y":
                chunk.remove(wire)
                return wire
        raise AssertionError()

    @staticmethod
    def _find_remove_cmd(chunk, cmd):
        for wire in chunk:
            if wire.cmd == cmd:
                chunk.remove(wire)
                return wire
        raise AssertionError()
    
    @staticmethod
    def _vars(cps, key):
        return {cps[key].v1, cps[key].v2}

    @staticmethod
    def _replace(cps, expected, to_put):
        for key, wire in cps.items():
            if wire.output == expected:
                cps[key] = Wire(*wire[:3], to_put)
                break

    def correlate_ordered_to_expected(self, ordered_wires):
        # x0 XOR y0  ->  z0
        # x0 AND y0  ->  c0
        swaps = []
        assert ordered_wires[0] == Wire("x00", "XOR", "y00", "z00")
        assert ordered_wires[1][:3] == ("x00", "AND", "y00")
        c = ordered_wires[1].output
        # xi XOR yi  ->  ri
        # xi AND yi  ->  si
        # ri XOR c[i-1]  ->  zi
        # ri AND c[i-1]  ->  ti
        # si OR ti   ->  ci
        for index in range(1, 45):
            chunk = self._chunk(ordered_wires, index)
            assert len(chunk) == 5
            cps = { "xy_xor" : self._find_remove_xy_cmd(chunk, "XOR"),
                   "xy_and" : self._find_remove_xy_cmd(chunk, "AND") }
            assert set( w.cmd for w in chunk ) == {"XOR", "AND", "OR"}
            cps["xor_wire"] = self._find_remove_cmd(chunk, "XOR")
            cps["and_wire"] = self._find_remove_cmd(chunk, "AND")
            cps["or_wire"] = self._find_remove_cmd(chunk, "OR")
            expected = "z{:02}".format(index)
            if cps["xor_wire"].output != expected:
                #print("xor wrong:", index)
                swaps.append((expected, cps["xor_wire"].output))
                self._replace(cps, expected, cps["xor_wire"].output)
                cps["xor_wire"]= Wire(*cps["xor_wire"][:3], expected)
            assert self._vars(cps, "xor_wire") == self._vars(cps, "and_wire")
            # Assumption (which holds here) is that only one of these can be wrong
            assert c in self._vars(cps,"xor_wire")
            if cps["xy_xor"].output not in self._vars(cps,"xor_wire"):
                #print("xy xor output wrong", index)
                xy_xor_correct_output = set( self._vars(cps,"xor_wire") )
                xy_xor_correct_output.remove(c)
                xy_xor_correct_output = xy_xor_correct_output.pop()
                swaps.append((xy_xor_correct_output, cps["xy_xor"].output))
                self._replace(cps, xy_xor_correct_output, cps["xy_xor"].output)
                cps["xy_xor"] = Wire(*cps["xy_xor"][:3], xy_xor_correct_output)
            assert self._vars(cps,"or_wire") == {cps["xy_and"].output, cps["and_wire"].output}
            c = cps["or_wire"].output
        return swaps
    
    def implement_swaps(self, swaps):
        for v1, v2 in swaps:
            for index in range(len(self._wiring)):
                wire = self._wiring[index]
                if wire.output == v1:
                    self._wiring[index] = Wire(*wire[:3], v2)
                if wire.output == v2:
                    self._wiring[index] = Wire(*wire[:3], v1)

    def run(self, x, y):
        self._variables = dict()
        for i in range(45):
            self._variables["x{:02}".format(i)] = x % 2
            self._variables["y{:02}".format(i)] = y % 2
            x = x // 2
            y = y // 2
        self.solve()
        return self.value()
    

def main(second_flag):
    with open("input24.txt") as f:
        wires = Parse(f)
    if not second_flag:
        wires.solve()
        return wires.value()
    ordered_wires = wires.sort_and_output()
    swaps = wires.correlate_ordered_to_expected(ordered_wires)
    wires.implement_swaps(swaps)
    # for x in range(2**45):
    #     for y in range(2**45):
    #         assert wires.run(x,y) == x+y
    for _ in range(100):
        x = random.randrange(0, 2**45)
        y = random.randrange(0, 2**45)
        assert wires.run(x,y) == x+y
    all_swaps = []
    for v1, v2 in swaps:
        all_swaps.append(v1)
        all_swaps.append(v2)
    all_swaps.sort()
    return ",".join(all_swaps), None
