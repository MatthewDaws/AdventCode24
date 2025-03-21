import sys, importlib, time

def fullrun(puzzle, secondflag):
    modulename = f".day{puzzle}"
    day = importlib.import_module(modulename, "advent")
    return day.main(secondflag)

def takeone(answer):
    try:
        num, *_ = answer
    except:
        return answer
    return num

def run(puzzle, secondflag):
    answer = fullrun(puzzle, secondflag)
    return takeone(answer)

def runall():
    answers = [(2815556, 23927637), (282, 349), (166630675, 93465710), (2639, 2005), (5747, 5502), (4515, 1309),
               (12553187650171, 96779702119491), (327, 1233), (6356833654075, 6389911791746), (789, 1735),
               (185894, 221632504974231), (1451030 ,859494), (33427, 91649162972270), (208437768, 7492),
               (1514333, 1528453), (88416, 442), (("4,1,7,6,4,1,0,2,7",None), 164279024971453), (326, ((18,62),None)),
               (360, 577474410989846), (1393, 990096), (184180, 231309103124520), (13022553808, 1555),
               (1154, ("aj,ds,gg,id,im,jx,kq,nj,ql,qr,ua,yh,zn", None)),
               (57270694330992, ("gwh,jct,rcb,wbw,wgb,z09,z21,z39", None))]
    for day, (first, second) in enumerate(answers):
        start = time.perf_counter_ns()
        one = fullrun(day+1, False)
        t1 = (time.perf_counter_ns() - start) // 1000000
        start = time.perf_counter_ns()
        two = fullrun(day+1, True)
        t2 = (time.perf_counter_ns() - start) // 1000000
        assert one == first
        assert two == second
        print(f"Day {day+1} : {one} ({t1} ms) and {two} ({t2} ms).")

def parse_args(args):
    """return `(mode, puzzlenumber, secondflag)`
    
    or raises `SyntaxError`
    """
    if len(args) <= 1:
        raise SyntaxError()
    if len(args) == 2:
        if args[1] == "all":
            return ("all", None, None)
        try:
            return ("run", int(args[1]), False)
        except:
            raise SyntaxError()
    if len(args) > 3 or args[2] != "2nd":
        raise SyntaxError()
    try:
        return ("run", int(args[1]), True)
    except:
        raise SyntaxError()

def main():
    try:
        mode, puzzle, secondflag = parse_args(sys.argv)
    except:
        print("Usage: [{puzzle number} [2nd]] / [all]")
        print()
        print("python -m advent 5       : Solve the first part of puzzle 5")
        print("python -m advent 7 2nd   : Solve the second part of puzzle 7")
        print("python -m all            : Solve all the puzzles")
        exit(-1)
    if mode == "all":
        runall()
        exit(0)
    print(run(puzzle, secondflag))
          

if __name__ == "__main__":
    main()
