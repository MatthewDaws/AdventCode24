class Parse:
    def __init__(self, rows):
        self._reports = []
        for row in rows:
            self._reports.append([int(_) for _ in row.strip().split()])

    def __getitem__(self, report):
        return self._reports[report]

    def __len__(self):
        return len(self._reports)

    def safe(self, report):
        row = self._reports[report]
        return self.is_safe(row)

    @staticmethod
    def is_safe(row):
        d = row[1] - row[0]
        if d == 0 or abs(d) > 3:
            return False
        index = 2
        while index < len(row):
            dd = row[index] - row[index-1]
            if d*dd <= 0:
                return False
            if abs(dd) > 3:
                return False
            index += 1
        return True

    def count_safe(self):
        return sum(self.safe(i) for i in range(len(self)))
    
    def find_bad_levels(self, report):
        row = self._reports[report]
        diffs = [a-b for a,b in zip(row, row[1:])]
        ups = sum(d>0 for d in diffs)
        downs = sum(d<0 for d in diffs)
        if ups > downs:
            expect = 1
        else:
            expect = -1
        problems = []
        for i,d in enumerate(diffs):
            if d==0 or abs(d)>=4 or expect*d < 0:
                problems.append(i)
        return problems

    def check_single_removal(self, report):
        bads = self.find_bad_levels(report)
        if len(bads) == 0:
            return True
        if len(bads) > 1:
            return False
        row = list(self._reports[report])
        row.pop(bads[0])
        return self.is_safe(row)

    def brute_force_check_single_removal(self, report):
        row = self._reports[report]
        if self.is_safe(row):
            return True
        for i in range(len(row)):
            row_copy = list(row)
            row_copy.pop(i)
            if self.is_safe(row_copy):
                return True
        return False

    def count_safe_single_removal(self):
        return sum(self.brute_force_check_single_removal(i) for i in range(len(self)))


def main(second_flag):
    with open("input2.txt") as f:
        reports = Parse(f)
    if not second_flag:
        return reports.count_safe()
    return reports.count_safe_single_removal()
