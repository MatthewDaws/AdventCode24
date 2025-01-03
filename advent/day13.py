import re, collections

from sympy import N

Machine = collections.namedtuple("Machine", "A, B, prize")

class Parse:
    def __init__(self, rows):
        # Button A: X+94, Y+34
        # Button B: X+22, Y+67
        # Prize: X=8400, Y=5400
        self._prog1 = re.compile("Button (.): X\+(\d+), Y\+(\d+)")
        self._prog2 = re.compile("Prize: X=(\d+), Y=(\d+)")
        self._machines = []
        while True:
            Anum, Ax, Ay = self._parse_button(next(rows))
            Bnum, Bx, By = self._parse_button(next(rows))
            Px, Py = self._parse_prize(next(rows))
            self._machines.append( Machine(A=(Ax,Ay), B=(Bx,By), prize=(Px,Py)) )
            try:
                next(rows)
            except StopIteration:
                break

    def _parse_button(self, row):
        m = self._prog1.match(row)
        return m.group(1), int(m.group(2)), int(m.group(3))
    
    def _parse_prize(self, row):
        m = self._prog2.match(row)
        return int(m.group(1)), int(m.group(2))

    @property
    def machines(self):
        return self._machines
    
    @staticmethod
    def solve(machine):
        matrix = [[machine.A[0], machine.B[0]], [machine.A[1], machine.B[1]]]
        determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        if determinant != 0:
            x = matrix[1][1] * machine.prize[0] - matrix[0][1] * machine.prize[1]
            y = -matrix[1][0] * machine.prize[0] + matrix[0][0] * machine.prize[1]
            if x % determinant != 0 or y % determinant != 0:
                return None, None
            return (x//determinant, y//determinant), None
        image = [matrix[0][0], matrix[1][0]]
        if image[0] == 0 and image[1] == 0:
            image = [matrix[0][1], matrix[1][1]]
            if image[0] == 0 and image[1] == 0:
                return None, None
        # Does there exists `s` with `s * image == machine.prize` ?
        if image[0] != 0 and image[1] != 0:
            # machine.prize[0] / image[0] == machine.prize[1] / image[1]
            if machine.prize[0] * image[1] != machine.prize[1] * image[0]:
                return None, None
        raise NotImplementedError()
    
    def minimal_cost(self):
        cost = 0
        for m in self.machines:
            soln, kernal = self.solve(m)
            if soln is not None:
                cost += 3*soln[0] + soln[1]
        return cost
    
    def adjust_units(self):
        new_machines = []
        for m in self._machines:
            new_machines.append(Machine(A=m.A, B=m.B, prize=(10000000000000+m.prize[0], 10000000000000+m.prize[1])))
        self._machines = new_machines


def main(second_flag):
    with open("input13.txt") as f:
        machines = Parse(f)
    if not second_flag:
        return machines.minimal_cost()
    machines.adjust_units()
    return machines.minimal_cost()
