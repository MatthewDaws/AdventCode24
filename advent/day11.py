from collections import defaultdict

class Parse:
    def __init__(self, rows):
        row = next(rows)
        self._nums = [int(x) for x in row.strip().split(" ")]

    def reset(self):
        self._counts = defaultdict(int)
        for x in self._nums:
            self._counts[x] += 1
        
    @property
    def counts(self):
        return self._counts

    @staticmethod
    def blink_number(n):
        if n == 0:
            return 1, None
        x = str(n)
        if len(x) % 2 == 0:
            mid = len(x) // 2
            a, b = x[:mid], x[mid:]
            return int(a), int(b)
        return n*2024, None

    def blink(self):
        new_counts = defaultdict(int)
        for n, count in self._counts.items():
            n1, n2 = self.blink_number(n)
            new_counts[n1] += count
            if n2 is not None:
                new_counts[n2] += count
        self._counts = new_counts

    def solve(self, iterations):
        self.reset()
        for _ in range(iterations):
            self.blink()
        return sum(self.counts.values())
    

def main(second_flag):
    with open("input11.txt") as f:
        nums = Parse(f)
    if not second_flag:
        return nums.solve(25)
    return nums.solve(75)
