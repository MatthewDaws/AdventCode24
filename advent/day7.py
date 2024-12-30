import re, itertools

class Parse:
    def __init__(self, rows):
        start_prog = re.compile("(\d+)\:")
        self._data = []
        for row in rows:
            m = start_prog.match(row)
            target = int(m.group(1))
            parts = row[len(m.group(1))+1:].strip()
            self._data.append((target, [int(_) for _ in parts.split()]))

    @property
    def data(self):
        return self._data
        
    def sum_can_solve(self, use_concat = False):
        count = 0
        for row in self._data:
            if self.solution(row, use_concat) is not None:
                count += row[0]
        return count

    def solution(self, row, use_concat = False):
        target = row[0]
        parts = row[1]
        if use_concat:
            options = "*+|"
        else:
            options = "*+"
        for ops in itertools.product(options, repeat=len(parts)-1):
            value = parts[0]
            for op, val in zip(ops, parts[1:]):
                if op == "+":
                    value += val
                elif op == "*":
                    value *= val
                else:
                    value = int(str(value)+str(val))
                if value > target:
                    break # Could improve by not looking at any further part of this "ops tree", but I'd have to roll my own `itertools.product` to do that
            if value == target:
                return "".join(ops)
        return None

    
def main(second_flag):
    with open("input7.txt") as f:
        sums = Parse(f)
    if not second_flag:
        return sums.sum_can_solve()
    return sums.sum_can_solve(True)
