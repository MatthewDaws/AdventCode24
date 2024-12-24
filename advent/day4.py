class Parse:
    def __init__(self, rows):
        self._grid = []
        for row in rows:
            self._grid.append(row.strip())
        
    @property
    def rows(self):
        return len(self._grid)
    
    @property
    def cols(self):
        return len(self._grid[0])
    
    def get(self, row, col):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return None
        return self._grid[row][col]

    def xmas_count(self):
        return sum(self.contains_xmas(row, col)
                    for row in range(self.rows)
                    for col in range(self.cols) )

    def contains_xmas(self, row, col):
        return sum(self.contains_xmas_in_dir(row, col, dr, dc)
                for dc in [-1,0,1] for dr in [-1,0,1] )

    def contains_xmas_in_dir(self, row, col, dr, dc):
        if dr==0 and dc==0:
            return False
        for n, s in enumerate("XMAS"):
            r = row + n*dr
            c = col + n*dc
            if s != self.get(r,c):
                return False
        return True
    
    def has_x_mas(self, row, col):
        if row<=0 or row>=self.rows-1 or col<=0 or col>=self.rows-1:
            return False
        if self.get(row, col) != "A":
            return False
        s = self.get(row-1,col-1) +  self.get(row+1,col+1)
        if s != "MS" and s != "SM":
            return False
        s = self.get(row-1,col+1) +  self.get(row+1,col-1)
        return s == "MS" or s == "SM"

    def count_x_mas(self):
        return sum(self.has_x_mas(row, col)
                   for row in range(1, self.rows)
                   for col in range(1, self.cols) )


def main(second_flag):
    with open("input4.txt") as f:
        grid = Parse(f)
    if not second_flag:
        return grid.xmas_count()
    return grid.count_x_mas()
