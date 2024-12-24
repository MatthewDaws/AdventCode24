import re

class Parse:
    def __init__(self, rows):
        self._prog = re.compile("\((\d+)\,(\d+)\)")
        self._rows = []
        for row in rows:
            self._rows.append(row.strip())
    
    @property
    def rows(self):
        return self._rows

    @staticmethod
    def _find_cmd(row, index):
        cmds = ["mul", "don't()", "do()"]
        finds = [row.find(c,index) for c in cmds]
        if all(f==-1 for f in finds):
            return -1, None
        minimal = min(f for f in finds if f!=-1)
        return minimal, cmds[finds.index(minimal)]

    def find_muls(self, row, use_commands = False, initial_blocked = False):
        blocked = initial_blocked
        muls = []
        index = 0
        while True:
            index, cmd = self._find_cmd(row, index)
            #index = row.find("mul", index)
            if cmd == "don't()":
                blocked = True
                index += 1
                continue
            if cmd == "do()":
                blocked = False
                index += 1
                continue
            if index == -1:
                if use_commands:
                    return muls, blocked
                return muls
            index += 3
            m = self._prog.match(row[index:])
            if m and not (blocked and use_commands):
                muls.append((int(m.group(1)), int(m.group(2)) ))
    
    def sum_all_muls(self, row, use_commands = False, initial_blocked=False):
        if use_commands:
            muls, blocked = self.find_muls(row, use_commands, initial_blocked)
            return sum(a*b for a,b in muls), blocked
        return sum(a*b for a,b in self.find_muls(row, use_commands, initial_blocked))
    
    def sum_all(self, use_commands = False):
        if use_commands:
            count = 0
            blocked = False
            for row in self._rows:
                c, blocked = self.sum_all_muls(row, True, blocked)
                count += c
            return count
        return sum(self.sum_all_muls(r, use_commands) for r in self._rows)
    

def main(second_flag):
    with open("input3.txt") as f:
        rows = Parse(f)
    if not second_flag:
        return rows.sum_all()
    return rows.sum_all(use_commands = True)
