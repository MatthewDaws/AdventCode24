from collections import defaultdict

class Parse:
    def __init__(self, rows):
        self._grid = []
        for r, row in enumerate(rows):
            self._grid.append(row.strip())
            c = row.find("S")
            if c != -1:
                self._start = (r,c)
            c = row.find("E")
            if c != -1:
                self._end = (r,c)

    @property
    def grid(self):
        return self._grid
    
    @property
    def start(self):
        return self._start
    
    @property
    def end(self):
        return self._end
    
    def find_path(self):
        deltas = [(1,0), (-1,0), (0,1), (0,-1)]
        path = [self._start]
        while True:
            for dr,dc in deltas:
                rr, cc = dr + path[-1][0], dc + path[-1][1]
                if self._grid[rr][cc] == "." and (len(path)==1 or path[-2]!=(rr,cc)):
                    path.append((rr,cc))
                if self._grid[rr][cc] == "E":
                    path.append((rr,cc))
                    return path

    def find_cheats(self):
        path = self.find_path()
        for index, src in enumerate(path):
            for i, tar in enumerate(path[index+3:]):
                if abs(src[0]-tar[0]) + abs(src[1]-tar[1]) == 2:
                    yield src, tar, i+1

    def group_cheats(self):
        time_saved = defaultdict(int)
        for s,t, saved in self.find_cheats():
            time_saved[saved] += 1
        return time_saved
    
    def count_cheats_at_least(self, lowbound, max_cheat_time=2):
        path = self.find_path()
        count = 0
        for index, src in enumerate(path):
            for i, tar in enumerate(path[index+lowbound+2:]):
                distance = abs(src[0]-tar[0]) + abs(src[1]-tar[1])
                if distance <= max_cheat_time and i >= distance-2:
                    count += 1
        return count
    

def main(second_flag):
    with open("input20.txt") as f:
        map = Parse(f)
    if not second_flag:
        return map.count_cheats_at_least(100)
    return map.count_cheats_at_least(100, 20)
