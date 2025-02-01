class Parse:
    def __init__(self, rows):
        self._secrets = [int(r.strip()) for r in rows]
    
    @property
    def secrets(self):
        return self._secrets

    # 16777216 = 2**24
    # x*64 is the same as x<<6
    # so if secret has lower 24 bits   b23 b22 ... b1 b0
    # then the 1st move is      b17 ... b1 b0  0  0  0  0  0  0
    #                       XOR b23 ... b7 b6 b5 b4 b3 b2 b1 b0
    #
    # the second move is        0   0 ...   0 b23 b22 ... b8 b7 b6 b5
    #                     XOR b23 b22 ... b19 b18 b17 ... b3 b2 b1 b0

    # 3rd move is           b12 ...  b1  b0   0 ...  0  0  0
    #                   XOR b23 ... b12 b11 b10 ... b2 b1 b0
    @staticmethod
    def next_secret(secret):
        num = secret * 64
        secret = (secret ^ num) % 16777216
        num = secret // 32
        secret = (secret ^ num) % 16777216
        num = secret * 2048
        return (secret ^ num) % 16777216

    def sum_iterations(self, iters=2000):
        count = 0
        for s in self._secrets:
            for _ in range(iters):
                s = self.next_secret(s)
            count += s
        return count
    
    @staticmethod
    def prices_changes(secret, iters=2000):
        values = [secret % 10]
        for _ in range(iters):
            secret = Parse.next_secret(secret)
            values.append(secret%10)
        return [(b, b-a) for a,b in zip(values, values[1:])]

    @staticmethod
    def to_quads(value_delta_list):
        three = [x for _,x in value_delta_list[:3]]
        quads = []
        values = []
        for value, delta in value_delta_list[3:]:
            quad = tuple(three) + (delta, )
            quads.append(quad)
            values.append(value)
            three = quad[1:]
        return quads, values

    @staticmethod
    def quad_values_to_initial_pattern_lookup(quads, values):
        lookup = dict()
        for q,v in zip(quads, values):
            if q not in lookup:
                lookup[q] = v
        return lookup

    def compute_lookups(self):
        lookups = []
        for secret in self._secrets:
            qs, vs = self.to_quads(self.prices_changes(secret))
            lookups.append( self.quad_values_to_initial_pattern_lookup(qs, vs) )
        return lookups
    
    @staticmethod
    def bananas_from(instruction, lookups):
        count = 0
        for lookup in lookups:
            if instruction in lookup:
                count += lookup[instruction]
        return count
    
    def best_instruction(self):
        lookups = self.compute_lookups()
        possible_instructions = set(lookups[0].keys())
        for ls in lookups[1:]:
            possible_instructions |= ls.keys()

        return max( self.bananas_from(instr, lookups) for instr in possible_instructions )
    

def main(second_flag):
    with open("input22.txt") as f:
        secrets = Parse(f)
    if not second_flag:
        return secrets.sum_iterations()
    return secrets.best_instruction()
