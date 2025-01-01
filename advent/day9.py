import enum


class Parse:
    def __init__(self, rows):
        self._data = next(rows).strip()
        self._disk = []
        self._file_positions = []
        self._gap_positions = []
        is_space = False
        file_id = 0
        for n in self._data:
            n = int(n)
            if is_space:
                self._gap_positions.append((len(self._disk),n))
                for _ in range(n):
                    self._disk.append(None)
                is_space = False
            else:
                self._file_positions.append((len(self._disk),n))
                for _ in range(n):
                    self._disk.append(file_id)
                file_id += 1
                is_space = True

    @property
    def disk(self):
        return self._disk

    @property
    def gap_positions(self):
        return self._gap_positions

    @property
    def file_positions(self):
        return self._file_positions

    def defrag(self):
        disk = list(self._disk)
        insert_index = 0
        while True:
            while insert_index < len(disk) and disk[insert_index] is not None:
                insert_index += 1
            if insert_index == len(disk):
                return disk
            num = disk.pop()
            disk[insert_index] = num

    def checksum(self):
        disk = self.defrag()
        return sum(n*num for n,num in enumerate(disk))
    
    @staticmethod
    def find_gap(gaps, length, minimal_pos):
        for index, (pos, gap_len) in enumerate(gaps):
            if pos >= minimal_pos:
                return None
            if gap_len == length:
                gaps.pop(index)
                return pos
            if gap_len > length:
                gaps[index] = (pos + length, gap_len - length)
                return pos
        return None

    def defrag_files(self):
        files = dict()
        gaps = list(self.gap_positions)
        index = len(self.file_positions) - 1
        while index >= 0:
            pos, length = self.file_positions[index]
            new_pos = self.find_gap(gaps, length, pos)
            if new_pos is None:
                files[index] = (pos, length)
            else:
                files[index] = (new_pos, length)
            index -= 1
        return files

    def files_checksum(self):
        files = self.defrag_files()
        checksum = 0
        for num in files:
            pos, length = files[num]
            checksum += num * sum( pos+p for p in range(length) )
        return checksum
    
    
def main(second_flag):
    with open("input9.txt") as f:
        disk = Parse(f)
    if not second_flag:
        return disk.checksum()
    return disk.files_checksum()
