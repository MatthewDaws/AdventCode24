from collections import namedtuple, defaultdict

class adv:
    def __init__(self, parent, data):
        self._parent = parent
        self._num = 2 ** parent.combo(data)

    def __call__(self):
        self._parent.A = self._parent.A // self._num
    

class bxl:
    def __init__(self, parent, data):
        self._parent = parent
        self._num = data

    def __call__(self):
        self._parent.B = self._parent.B ^ self._num
    

class bst:
    def __init__(self, parent, data):
        self._parent = parent
        self._num = parent.combo(data)

    def __call__(self):
        self._parent.B = self._num % 8


class jnz:
    def __init__(self, parent, data):
        self._parent = parent
        self._num = data

    def __call__(self):
        if self._parent.A != 0:
            self._parent.jump(self._num)


class bxc:
    def __init__(self, parent, data):
        self._parent = parent

    def __call__(self):
        self._parent.B = self._parent.B ^ self._parent.C


class out:
    def __init__(self, parent, data):
        self._parent = parent
        self._num = parent.combo(data) % 8

    def __call__(self):
        self._parent.output(self._num)


class bdv:
    def __init__(self, parent, data):
        self._parent = parent
        self._num = 2 ** parent.combo(data)

    def __call__(self):
        self._parent.B = self._parent.A // self._num


class cdv:
    def __init__(self, parent, data):
        self._parent = parent
        self._num = 2 ** parent.combo(data)

    def __call__(self):
        self._parent.C = self._parent.A // self._num


class Parse:
    def __init__(self, rows):
        for row in rows:
            if row.startswith("Register "):
                assert row[10] == ":"
                value = int(row.strip()[12:])
                if row[9] == "A":
                    self._A = value
                elif row[9] == "B":
                    self._B = value
                elif row[9] == "C":
                    self._C = value
                else:
                    raise ValueError()
                continue
            if row.strip() == "":
                continue
            assert row.startswith("Program: ")
            self._program = [int(x) for x in row[9:].strip().split(",")]
            # self._program = list(zip(self._program[::2], self._program[1::2]))

    @property
    def program(self):
        return self._program

    @property
    def A(self):
        return self._A

    @A.setter
    def A(self, v):
        self._A = v

    @property
    def B(self):
        return self._B

    @B.setter
    def B(self, v):
        self._B = v

    @property
    def C(self):
        return self._C
    
    @C.setter
    def C(self, v):
        self._C = v

    def combo(self, data):
        if data <= 3:
            return data
        if data == 4:
            return self._A
        if data == 5:
            return self._B
        if data == 6:
            return self._C
        raise ValueError()
    
    def jump(self, location):
        self._jumped = 1
        self._pointer = location
    
    def output(self, value):
        self._output.append(value)
    
    cmd_to_code = {0:adv, 1:bxl, 2:bst, 3:jnz, 4:bxc, 5:out, 6:bdv, 7:cdv}

    def run_single(self, code, data):
        cmd_class = self.cmd_to_code[code]
        cmd = cmd_class(self, data)
        self._jumped = 0
        cmd()

    def run(self):
        self._output = []
        self._pointer = 0
        while self._pointer < len(self._program):
            code = self._program[self._pointer]
            data = self._program[self._pointer + 1]
            self.run_single(code, data)
            if self._jumped == 0:
                self._pointer += 2

    @property
    def result(self):
        return self._output
    

def build_lookup(machine):
    lookup = []
    for a in range(1023):
        machine.A = a
        machine.run()
        lookup.append( machine.result[0] )
    return lookup

def solve_part_two(machine):
    # What input A makes the machine write out its own code?
    # - The only thing which changes A is dividing by 8 each loop.  So to get 16 loops,
    #   we know 8**16 > A >= 8**15.  I.e. very large.
    # - The programme (see tests) is:
    #    * B = A % 8  i.e. least 3-bit word of A
    #    * B = B XOR 1  i.e. flip lowest bit
    #    * C = A // (2**B)
    #    * B = B XOR 5  i.e. reset lowest bit, flip highest bit
    #    * B = B XOR C
    #    * Write out B % 8
    #    * Remove lowest word of A, loop
    # - What gets written out is ((lowest word of A) XOR 4) XOR (lowest 3 bits of C)
    # - And C=A//(2**B) means we look at the 3 bits of A shifted by B, where here B=(A%8) XOR 1
    # - So the output of one loop depends only on the 10 least bits of A
    # - And there is no memory.
    lookup = build_lookup(machine)
    assert lookup[221] == 4
    # This lookup tells us what the lower 10 bits must be.  So we could try to find a coherent way
    # to piece these together.
    # Entry = namedtuple("Entry", ["output", "higherbits"])
    # reverse_lookup = defaultdict(list)
    # for k,v in enumerate(lookup):
    #     key = Entry(v, k//8)
    #     reverse_lookup[key].append(k)
    Partial = namedtuple("Partial", ["A", "depth"])
    to_search = [ Partial(k, 1) for k,v in enumerate(lookup) if v == machine.program[0] ]
    solutions = []
    while len(to_search) > 0:
        partial = to_search.pop()
        higher_bits = partial.A >> (3*partial.depth)
        if partial.depth == len(machine.program):
            if higher_bits == 0:
                solutions.append(partial.A)
            continue
        target = machine.program[partial.depth]
        for k,v in enumerate(lookup):
            if v == target and (k & 127) == higher_bits:
                A = ( k << (3*partial.depth) ) | partial.A
                to_search.append( Partial(A, partial.depth+1) )
    return min(solutions)


def main(second_flag):
    with open("input17.txt") as f:
        machine = Parse(f)
    if not second_flag:
        machine.run()
        return (",".join(str(x) for x in machine.result), None) #  Slightly silly convention
    A = solve_part_two(machine)
    machine.A = A
    machine.run()
    assert machine.result == machine.program
    # 164282363637693 too high
    return A
