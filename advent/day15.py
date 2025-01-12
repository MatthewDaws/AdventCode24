import enum

from regex import D

class Parse:
    def __init__(self, rows):
        self._grid = []
        self._instructions = ""
        self._dir_dict = {"^":(-1,0), "v":(1,0), "<":(0,-1), ">":(0,1)}
        parsed_map = False
        for row in rows:
            row = row.strip()
            if parsed_map:
                self._instructions += row
            else:
                if len(row) == 0:
                    parsed_map = True
                    continue
                self._grid.append(row.strip())
        
    def at(self, row, col):
        return self._grid[row][col]
    
    @property
    def rows(self):
        return len(self._grid)
    
    @property
    def columns(self):
        return len(self._grid[0])
    
    @property
    def instructions(self):
        return self._instructions

    def robot_location(self):
        for r, row in enumerate(self._grid):
            for c, entry in enumerate(row):
                if entry == "@":
                    return r,c
        raise ValueError()
    
    @staticmethod
    def access(grid, pos):
        return grid[pos[0]][pos[1]]

    @staticmethod
    def set(grid, pos, entry):
        grid[pos[0]][pos[1]] = entry

    @staticmethod
    def move(grid, position, direction):
        start_pos = position[0] + direction[0], position[1] + direction[1]
        if Parse.access(grid, start_pos) == "#":
            return None
        end_pos = start_pos
        while Parse.access(grid, end_pos) == "O":
            end_pos = end_pos[0] + direction[0], end_pos[1] + direction[1]
        if end_pos == start_pos:
            return grid
        if Parse.access(grid, end_pos) == "#":
            return None
        new_grid = [ list(row) for row in grid ]
        Parse.set(new_grid, start_pos, ".")
        Parse.set(new_grid, end_pos, "O")
        return new_grid
    
    def run_step(self, grid, pos, cmd):
        direction = self._dir_dict[cmd]
        g = self.move(grid, pos, direction)
        if g is not None:
            grid = g
            pos = pos[0] + direction[0], pos[1] + direction[1]
        return grid, pos

    def grid_without_robot(self):
        pos = self.robot_location()
        grid = [list(row) for row in self._grid]
        grid[pos[0]][pos[1]] = "."
        return grid, pos
    
    def run(self):
        grid, pos = self.grid_without_robot()
        self.set(grid, pos, ".")
        for cmd in self._instructions:
            grid, pos = self.run_step(grid, pos, cmd)
        return grid

    @staticmethod
    def GPS_score(grid):
        score = 0
        for r, row in enumerate(grid):
            for c, entry in enumerate(row):
                if entry in "O[":
                    score += 100*r + c
        return score

    def double(self):
        double_map = {"#":"##", ".":"..", "@":"@.", "O":"[]"}
        self._grid = [
            "".join(double_map[c] for c in row)
            for row in self._grid ]
        
    @staticmethod
    def grid_to_placements(grid):
        boxes = []
        for r, row in enumerate(grid):
            for c, entry in enumerate(row):
                if entry == "[":
                    boxes.append((r,c))
        return boxes
    
    @staticmethod
    def intersects_box(position, box_pos):
        if position == box_pos:
            return True
        box_pos_right = (box_pos[0], box_pos[1]+1)
        return position == box_pos_right

    @staticmethod
    def doubled_move_new(grid, position, direction):
        need_to_occupy_places = [(position[0] + direction[0], position[1] + direction[1])]
        unmoved_boxes = set(Parse.grid_to_placements(grid))
        moved_boxes = set()
        while len(need_to_occupy_places) > 0:
            new_occupy_places = []
            for p in need_to_occupy_places:
                if Parse.access(grid, p) == "#":
                    return None
                intersected_boxes = []
                for b in unmoved_boxes:
                    if Parse.intersects_box(p, b):
                        new_occupy_places.append(b)
                        new_occupy_places.append((b[0], b[1]+1))
                        intersected_boxes.append(b)
                for b in intersected_boxes:
                    unmoved_boxes.remove(b)
                    moved_boxes.add(b)
            need_to_occupy_places = [(p[0] + direction[0], p[1] + direction[1]) for p in new_occupy_places]
        return moved_boxes        

    def run_step_doubled(self, grid, pos, cmd):
        direction = self._dir_dict[cmd]
        moved_boxes = self.doubled_move_new(grid, pos, direction)
        if moved_boxes is not None:
            grid = [list(row) for row in grid]
            for b in moved_boxes:
                grid[b[0]][b[1]] = "."
                grid[b[0]][b[1]+1] = "."
            for b in moved_boxes:
                grid[b[0]+direction[0]][b[1]+direction[1]] = "["
                grid[b[0]+direction[0]][b[1]+direction[1]+1] = "]"
            pos = pos[0] + direction[0], pos[1] + direction[1]
        return grid, pos


    def double_run(self):
        grid, pos = self.grid_without_robot()
        self.set(grid, pos, ".")
        for cmd in self._instructions:
            grid, pos = self.run_step_doubled(grid, pos, cmd)
        return grid



def main(second_flag):
    with open("input15.txt") as f:
        warehouse = Parse(f)
    if not second_flag:
        return warehouse.GPS_score(warehouse.run())
    warehouse.double()
    grid = warehouse.double_run()
    return warehouse.GPS_score(grid)
