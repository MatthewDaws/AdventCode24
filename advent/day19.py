from collections import defaultdict

class Parse:
    def __init__(self, rows):
        row = next(rows)
        self._towels = row.strip().split(", ")
        next(rows)
        self._designs = [row.strip() for row in rows]

    @property
    def towels(self):
        return self._towels
    
    @property
    def designs(self):
        return self._designs
        
    def count_ways2(self, design):
        suffixes = { design : 1 }
        lookup = defaultdict(list)
        for t in self._towels:
            lookup[t[0]].append(t)
        while True:
            next_suffixes = defaultdict(int)
            for des, count in suffixes.items():
                if des == "":
                    next_suffixes[des] += count
                    continue
                for t in lookup[des[0]]:
                    if des.startswith(t):
                        next_suffixes[des[len(t):]] += count
            suffixes = next_suffixes
            if len(suffixes) == 1:
                for key, value in suffixes.items():
                    if key == "":
                        return value
            if len(suffixes) == 0:
                return 0
            
    def number_designs_possible2(self):
        return sum(self.count_ways2(d) > 0 for d in self._designs)


def main(second_flag):
    with open("input19.txt") as f:
        towels = Parse(f)
    if not second_flag:
        return towels.number_designs_possible2()
    return sum(towels.count_ways2(d) for d in towels.designs)
