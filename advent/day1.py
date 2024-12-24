import bisect

class Parse:
    def __init__(self, rows):
        self._cols = [[],[]]
        for row in rows:
            a,b = [int(x) for x in row.strip().split()]
            self._cols[0].append(a)
            self._cols[1].append(b)
        self._cols[0].sort()
        self._cols[1].sort()

    def __getitem__(self, row):
        return self._cols[0][row], self._cols[1][row]
        
    @property
    def distance(self):
        return sum(abs(a-b) for a,b in zip(self._cols[0], self._cols[1]))

    @property
    def left_list(self):
        return self._cols[0]

    def locate_in_right(self, value):
        i = bisect.bisect_left(self._cols[1], value)
        if i != len(self._cols[1]) and self._cols[1][i] == value:
            return i
        return -1

    def count_in_right(self, value):
        start = self.locate_in_right(value)
        if start == -1:
            return 0
        count = 0
        while start < len(self._cols[1]) and self._cols[1][start] == value:
            count += 1
            start += 1
        return count

    def similarity_score(self):
        return sum(value * self.count_in_right(value) for value in self.left_list)
    

def main(second_flag):
    with open("input1.txt") as f:
        locs = Parse(f)
    if not second_flag:
        return locs.distance
    return locs.similarity_score()
