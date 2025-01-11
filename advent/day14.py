import re, collections
from .utils.int_math import inverse_modn, lcm, int_lin_comb_min_solve

Robot = collections.namedtuple("Robot", "pos, vel")

class Parse:
    def __init__(self, rows, debug=False):
#        p=0,4 v=3,-3
        prog = re.compile("p=(.*?),(.*?) v=(.*?),(.*)")
        self._robots = []
        for row in rows:
            m = prog.match(row)
            position = int(m.group(1)), int(m.group(2))
            velocity = int(m.group(3)), int(m.group(4))
            self._robots.append( Robot(pos=position, vel=velocity) )
        if debug:
            self._size = (11, 7)
        else:
            self._size = (101, 103)

    @property
    def robots(self):
        return self._robots
    
    def positions_after_time(self, time=100):
        positions = []
        for robot in self._robots:
            x = robot.pos[0] + time * robot.vel[0]
            y = robot.pos[1] + time * robot.vel[1]
            positions.append( (x % self._size[0], y % self._size[1]))
        return positions
    
    def quadrant_counts(self, positions):
        midx, midy = (self._size[0] - 1 ) // 2, (self._size[1] - 1 ) // 2
        q1 = sum( x < midx and y < midy for (x,y) in positions )
        q2 = sum( x > midx and y < midy for (x,y) in positions )
        q3 = sum( x < midx and y > midy for (x,y) in positions )
        q4 = sum( x > midx and y > midy for (x,y) in positions )
        return [q1, q2, q3, q4]
    
    def safety_factor(self, time=100):
        p = self.positions_after_time(time)
        qc = self.quadrant_counts(p)
        return qc[0] * qc[1] * qc[2] * qc[3]

    def lines_are_horizontal_rows(self, positions, lines):
        search_for = "#" * 20
        rows = self.print(positions)
        return all(search_for in rows[l] for l in lines)

    def print(self, positions):
        out = [ [ "." for _ in range(self._size[0]) ] for _ in range(self._size[1]) ]
        for p in positions:
            out[p[1]][p[0]] = "#"
        return [ "".join(row) for row in out ]
    
    def is_horizontally_symmetric(self, positions):
        grid = [ [ 0 for _ in range(self._size[0]) ] for _ in range(self._size[1]) ]
        for p in positions:
            grid[p[1]][p[0]] += 1
        midx = (self._size[0] - 1 ) // 2
        for row in grid:
            if not all( row[i] == row[self._size[0]-1-i] for i in range(midx) ):
                return False
        return True    

    def is_weakly_horizontally_symmetric(self, positions):
        grid = [ [ 0 for _ in range(self._size[0]) ] for _ in range(self._size[1]) ]
        for p in positions:
            grid[p[1]][p[0]] = 1
        midx = (self._size[0] - 1 ) // 2
        for row in grid:
            if not all( row[i] == row[self._size[0]-1-i] for i in range(midx) ):
                return False
        return True    

    def search_for_horizontally_symmetric(self):
        time = 0
        while True:
            positions = self.positions_after_time(time)
            if self.is_horizontally_symmetric(positions):
                return self.print(positions)
            time += 1

    # 101 and 103 are prime, so Z/pZ is a field, and so the robots will eventually repeat their positions
    # But the pattern (with #) can occur in a smaller period, I guess with different robots occuping the same places.
    def period_of_robot(self, robot):
        x = inverse_modn(robot.vel[0], self._size[0])
        y = inverse_modn(robot.vel[1], self._size[1])
        return lcm(x, y)

    def period_of_all(self):
        period = 1
        for robot in self._robots:
            p = self.period_of_robot(robot)
            period = lcm(period, p)
        return period

# We printed out a load of time steps, and noticed that there was a definite horizontal and vertical pattern at certain times:
# Vertical: 18, 119, 220, 321  so period of 101
# Horizontal: 76, 179, 282, 385  so period of 103
# (Same as size of grid; is that important?)
def print_first_range(robots, number = 10000):
    print(robots.period_of_all())
    with open("temp.txt", "w") as f:
        for time in range(number): #range(0,-100,-1):
            positions = robots.positions_after_time(time)
            f.write(str(time)+"\n")
            for row in robots.print(positions):
                f.write(row+"\n")
            f.write("\n")

def solve_from_manual_data():
    v, vd = 18, 101
    h, hd = 76, 103
    x, y = int_lin_comb_min_solve(vd, hd, h-v)
    return v + x*vd

def main(second_flag):
    with open("input14.txt") as f:
        robots = Parse(f)
    if not second_flag:
        return robots.safety_factor()

    num = solve_from_manual_data()
    assert num == 7492
    return num

    # Or search for a feature we know; but we only know this from the manual investigation,
    # so this doesn't feel any less like cheating than the above!
    time = 0
    while True:
        positions = robots.positions_after_time(time)
        if robots.lines_are_horizontal_rows(positions, [41, 73]):
            return time
        time += 1
