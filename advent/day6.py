from enum import Enum

class Dir(Enum):
    UP = (-1,0)
    DOWN = (1,0)
    LEFT = (0,-1)
    RIGHT = (0,1)

class Parse:
    _rot_dict = {Dir.UP:Dir.RIGHT, Dir.RIGHT:Dir.DOWN, Dir.DOWN: Dir.LEFT, Dir.LEFT:Dir.UP}

    def __init__(self, rows):
        self._grid = []
        for r, row in enumerate(rows):
            grid_row = []
            for c, entry in enumerate(row.strip()):
                if entry == "^":
                    self._location = (r,c)
                    self._direction = Dir.UP
                    self._init = (r,c)
                    entry = "."
                if entry == "#":
                    grid_row.append(False)
                else:
                    grid_row.append(True)
            self._grid.append(grid_row)

    @property
    def location(self):
        return self._location
    
    @property
    def grid(self):
        return self._grid

    @property
    def direction(self):
        return self._direction
    
    @property
    def rows(self):
        return len(self._grid)
    
    @property
    def columns(self):
        return len(self._grid[0])
    
    def rotate(self):
        self._direction = self._rot_dict[self._direction]

    def move(self):
        while True:
            dr, dc = self._direction.value
            new_r = self._location[0] + dr
            new_c = self._location[1] + dc
            if new_r < 0 or new_c < 0 or new_r >= self.rows or new_c >= self.columns:
                return None
            if not self._grid[new_r][new_c]:
                self.rotate()
                continue
            self._location = (new_r, new_c)
            return self._location
        
    def visits_until_leave(self):
        count = 1
        while self.move() is not None:
            count += 1
        return count
    
    def find_path_until_leave(self):
        places = set()
        places.add(self.location)
        while self.move() is not None:
            places.add(self.location)
        return places

    def distinct_visits_until_leave(self):
        return len(self.find_path_until_leave())
    
    def reset(self):
        self._location = self._init
        self._direction = Dir.UP

    def does_repeat(self, block):
        self.reset()
        r, c = block
        if block == self.location or self._grid[r][c] == False:
            raise ValueError()
        self._grid[r][c] = False
        try:
            places = set()
            places.add((self.location, self.direction))
            while self.move() is not None:
                pair = (self.location, self.direction)
                if pair in places:
                    return True
                places.add(pair)
            return False
        finally:
            self._grid[r][c] = True

    def count_blocking_points(self):
        count = 0
        for r in range(self.rows):
            for c in range(self.columns):
                if (r,c) == self._init or not self.grid[r][c]:
                    continue
                if self.does_repeat((r,c)):
                    count += 1
        return count

    def count_blocking_points(self):
        self.reset()
        places = self.find_path_until_leave()
        choices = []
        for (r,c) in places:
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    rr, cc = r+dr, c+dc
                    if rr < 0 or cc < 0 or rr >= self.rows or cc >= self.columns:
                        continue
                    choices.append((rr,cc))
        choices = set(choices)
        # This is still too large.  A potential blocking point must interrupt the "usual" path; this might reduce to options a little?
        # Or look at "squares": to have a loop you need 4 blocks in a square!

        count = 0
        for r, c in choices:
            if (r,c) == self._init or not self.grid[r][c]:
                continue
            if self.does_repeat((r,c)):
                count += 1
        return count


def main(second_flag):
    with open("input6.txt") as f:
        grid = Parse(f)
    if not second_flag:
        return grid.distinct_visits_until_leave()
    return grid.count_blocking_points()
