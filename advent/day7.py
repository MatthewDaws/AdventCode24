import re, itertools, math

class Parse:
    def __init__(self, rows):
        start_prog = re.compile("(\\d+)\:")
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
    
    @staticmethod
    def concat(i,j):
        m = 10 ** (1 + math.floor(math.log10(j)))
        return i*m + j

    def solution_concat_fast(self, row):
        target, parts = row[0], row[1]
        length = len(parts) - 1
        ops = [0] * length
        def inc(i):
            while True:
                if i<0:
                    raise StopIteration()
                ops[i] += 1
                if ops[i] <= 2:
                    break
                ops[i] = 0
                i -= 1
        try:
            while True:
                value = parts[0]
                flag = False
                for i, op in enumerate(ops):
                    val = parts[i+1]
                    if op == 0:
                        value += val
                    elif op == 1:
                        value *= val
                    else:
                        value = self.concat(value, val)
                    if value > target:
                        inc(i)
                        flag = True
                        break
                if flag:
                    continue
                if value == target:
                    strops = []
                    for op in ops:
                        if op == 0: strops.append("+")
                        elif op == 1: strops.append("*")
                        else: strops.append("|")
                    return "".join(strops)
                inc(length-1)
        except StopIteration:
            return None
        
    def sum_can_solve_fast(self):
        count = 0
        for row in self._data:
            if self.solution_concat_fast(row) is not None:
                count += row[0]
        return count

    
def main(second_flag):
    with open("input7.txt") as f:
        sums = Parse(f)
    if not second_flag:
        return sums.sum_can_solve()
    # Only a bit faster, sadly
    return sums.sum_can_solve_fast()
    #return sums.sum_can_solve(True)
