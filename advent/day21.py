"""
Found this one really hard; the 2nd part at least.

A typical solution (to the 1st case, 2 levels deep) is as follows:

`
v<<A >>^A vA ^A    v<A <A A >>^A A vA ^<A >A A vA ^A    v<A ^>A A <A >A    v<A <A >>^A A A <A v>A ^A 
<A        >A       v<<A          A >^A       A >A       vA      A ^A       v<A         A A ^>A 
^A                 <<^^A                                >>A                vvvA 
379A
`

We add spaces for clarity.  Some observations:

- A "repeated move" like `<<^^A` is always better than `<^<^A` because any repeated move can be executed by a chain of `A` button presses, which clearly cannot be improved upon.
- This gives the possible choices in the numerical keypad: choices like `<<^^A` or `^^<<A`.  We look at all of these.
- Any move ends in an `A`, at all levels (the spaces in the example above show this), and in this way the problem splits into subproblems

We now look at these "subproblem":

- Within such a subproblem, it's not clear to me if we have an "optimal substructure" problem: if we have the best (shortest) solution of depth 5, say, is the depth 4 sub-problem also optimal?
- It's clear it's not worth taking a "silly" route, like `v<^A` instead of `<A`, as the shortest string will be a substring.
- Thus in the keypad, the only choices are in the right-hand "square", choices between `<vA` and `v<A`, and so forth.

An example of why this choice matters:

`
<vA <A A >>^A vA ^A <A v>A ^A
v<<A          >A    ^>A
<vA

<vA <A A >>^A vA ^A vA <^A >A
v<<A          >A    >^A
<vA

<vA <A >>^A v<<A >>^A vA A <^A >A
v<A         <A        >>^A
v<A

v<<A >A >^A v<<A >>^A vA A <^A A
<vA         <A        >>^A
v<A
`

Notice that in the top row the choices don't matter.

There is an `optimal substructure' here.  A "command" is a (optimal) sequence of keypad directions
ending in "A".  If we know the shortest way to get every command at a certain depth, then to find
the shortest way to execute a command at the next depth, we look at all choices at the depth above,
and use the lookup to find which of these choices is optimal.  We can build up this lookup table
recursively, and then use the depth we need to search over all optimal movements in the numeric
keypad.

The problem seems hard (to me) because the 1st part doesn't expose that these choies really matter.
This meant I spent too long trying to reason out the optimal moves, instead of seeing the dynamic
programming solution.
"""

from collections import defaultdict

class Parse:
    def __init__(self, rows):
        self._codes = [row.strip() for row in rows]
    
    @property
    def codes(self):
        return self._codes
    
    def numeric_part_code(self, code):
        return int(code[:-1])
    
    @staticmethod
    def _vertical(current, target):
        if current < target:
            return "v" * (target - current)
        if current > target:
            return "^" * (current - target)
        return ""
    
    @staticmethod
    def _horizontal(current, target):
        if current < target:
            return ">" * (target - current)
        if current > target:
            return "<" * (current - target)
        return ""

    _numeric_pad = {"7":(0,0), "8":(0,1), "9":(0,2), "4":(1,0), "5":(1,1), "6":(1,2), "1":(2,0), "2":(2,1), "3":(2,2), "0":(3,1), "A":(3,2)}

    @staticmethod
    def optimal_routes_numeric_pad(code):
        current = Parse._numeric_pad["A"]
        routes = [""]
        for entry in code:
            target = Parse._numeric_pad[entry]
            if current[0] == 3 and target[1] == 0:
                # Can't go horizontal first
                toadd = [0]
            elif target[0] == 3 and current[1] == 0:
                # Can't go vertical first
                toadd = [1]
            else:
                toadd = [0, 1]
            r0 = Parse._vertical(current[0], target[0]) + Parse._horizontal(current[1], target[1])
            r1 = Parse._horizontal(current[1], target[1]) + Parse._vertical(current[0], target[0])
            if r0 == r1:
                toadd = [0]
            new_routes = []
            for route in routes:
                if 0 in toadd:
                    new_routes.append(route + r0 + "A")
                if 1 in toadd:
                    new_routes.append(route + r1 + "A")
            routes = new_routes
            current = target
        return routes

    def build_lookup(self, depth=2):
        """The top, 0, row doesn't matter.  If we know the shortest implementation of each move
        at level n, we can compute those at level n+1 by checking all against this lookup."""
        possible_keypad_locations = [(0,1), (0,2), (1,0), (1,1), (1,2)]
        possible_keypad_moves = set()
        for c in possible_keypad_locations:
            for t in possible_keypad_locations:
                s = Parse.keypad_route_from_to(c,t)
                if type(s) == str:
                    possible_keypad_moves.add(s)
                else:
                    possible_keypad_moves.update(s)
        
        self._lookup = dict()
        self._lookup[0] = dict()
        for code in possible_keypad_moves:
            possibles = Parse.optimal_routes_keypad(code)
            option = possibles[0]
            self._lookup[0][code] = (len(option), option)
            #Parse.convert_string_to_commands

        for level in range(1, depth):
            self._lookup[level] = dict()
            for code in possible_keypad_moves:
                possibles = Parse.optimal_routes_keypad(code)
                min_length, best = None, None
                for option in possibles:
                    length = sum( self._lookup[level-1][c][0] for c in Parse.convert_string_to_commands(option) )
                    if min_length is None or length < min_length:
                        min_length = length
                        best = option
                self._lookup[level][code] = (min_length, best)
        return self._lookup

    def shortest_implementation_keypad(self, initial_code, depth=2):
        """`initial_code` should be a single code ending in `A` coming from the numeric codes"""
        return min(
            sum( self._lookup[depth-2][c][0] for c in Parse.convert_string_to_commands(option) )
            for option in Parse.optimal_routes_keypad(initial_code)
            )
    
    def shortest_path_from_lookup(self, numeric_code, depth=2):
        return min(
           self.shortest_implementation_keypad(initial_code, depth)
           for initial_code in Parse.optimal_routes_numeric_pad(numeric_code)
        )
    

    def complexity_from_lookup(self, depth=2):
        return sum( self.shortest_path_from_lookup(code, depth) * self.numeric_part_code(code) for code in self._codes)

    _keypad = { "^":(0,1), "A":(0,2), "<":(1,0), "v":(1,1), ">":(1,2) }
    
    @staticmethod
    def keypad_route_from_to(current, target):
        if target == (1,0):
            return "v" * (1-current[0]) + "<" * current[1] + "A"
        elif current == (1,0):
            return ">" * target[1] + "^" * (1-target[0]) + "A"
        else:
            if target[0] == current[0]:
                if target[1] < current[1]:
                    return "<" * (current[1]-target[1]) + "A"
                else:
                    return ">" * (target[1]-current[1]) + "A"
            elif target[1] == current[1]:
                if target[0] < current[0]:
                    return "^A"
                elif target[0] > current[0]:
                    return "vA"
                else:
                    return "A"
            else:
                if target[0] < current[0]:
                    r1 = "^"
                else:
                    r1 = "v"
                if target[1] < current[1]:
                    r2 = "<"
                else:
                    r2 = ">"
                return [r1+r2+"A", r2+r1+"A"]
    
    @staticmethod
    def optimal_routes_keypad(code):
        current = Parse._keypad["A"]
        routes = [""]
        for entry in code:
            target = Parse._keypad[entry]
            r = Parse.keypad_route_from_to(current, target)
            if type(r) == str:
                new_routes = [x + r for x in routes]
            else:
                new_routes = []
                r1, r2 = r
                for x in routes:
                    new_routes.append(x+r1)
                    new_routes.append(x+r2)
            routes = new_routes
            current = target
        return routes
    
    @staticmethod
    def convert_string_to_commands(code):
        return [x+"A" for x in code.split("A")][:-1]


def main(second_flag):
    with open("input21.txt") as f:
        codes = Parse(f)
    if not second_flag:
        codes.build_lookup()
        return codes.complexity_from_lookup()
    codes.build_lookup(25)
    return codes.complexity_from_lookup(25)
