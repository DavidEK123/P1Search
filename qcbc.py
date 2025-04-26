#!/usr/bin/env python3

# lil tests
#   python3 qcbc.py depth-first test1.txt
#   python3 qcbc.py uniform-cost test1.txt

import sys
import heapq
from collections import deque


def load_environment(path):
    with open(path) as f:
        w = int(f.readline())
        h = int(f.readline())



        raw = [list(f.readline().rstrip("\n")) for _ in range(h)]
    
    for idx, line in enumerate(raw):
        if len(line) < w:
            line += [' '] * (w - len(line))



        elif len(line) > w:
            raw[idx] = line[:w]

    print(f"Parsed world: expecting {w} columns, got {h} rows")
    for i, row in enumerate(raw):
        print(f" row {i}: '{''.join(row)}' (len={len(row)})")

    origin = None
    muck   = set()
    walls  = set()
    for y in range(h):
        for x in range(w):
            ch = raw[y][x]
            if   ch == '@': origin = (y, x)
            elif ch == '*': muck.add((y, x))
            elif ch == '#': walls.add((y, x))
    return h, w, origin, muck, walls


# neighbor generator
neighbors = lambda y, x, hh, ww, wl: [
    (y-1, x, 'N'), (y+1, x, 'S'), (y, x+1, 'E'), (y, x-1, 'W')
]


def depth_seeker(h, w, origin, muck, walls):
    start_state = (origin[0], origin[1], frozenset(muck))
    frontier    = deque([(start_state, [])])



    seen        = {start_state: True}
    gen         = 1
    exp         = 0

    while frontier:
        (y, x, d), seq = frontier.pop()
        exp += 1

        if (y, x) in d:
            nd   = set(d)
            nd.remove((y, x))
            st   = (y, x, frozenset(nd))
            seq2 = seq + ['V']
            gen += 1
            if not nd:
                return seq2, gen, exp
            if st not in seen:
                seen[st] = True
                frontier.appendleft((st, seq2))

        for ny, nx, a in neighbors(y, x, h, w, walls):
            nxt = (ny, nx, d)



            seq2 = seq + [a]
            gen += 1
            if nxt not in seen:
                if not d:
                    return seq2, gen, exp
                seen[nxt] = True
                frontier.appendleft((nxt, seq2))

    return None, gen, exp


def cost_traverse(h, w, origin, muck, walls):
    start_state = (origin[0], origin[1], frozenset(muck))
    heap        = [(0, start_state, [])]

    best        = {start_state: 0}
    gen, exp    = 1, 0

    while heap:
        cost, (y, x, d), seq = heapq.heappop(heap)
        if cost > best[(y, x, d)]:
            continue
        exp += 1

        if (y, x) in d:
            nd   = set(d)
            nd.remove((y, x))
            st   = (y, x, frozenset(nd))
            c2   = cost + 1
            seq2 = seq + ['V']
            gen += 1
            if not nd:
                return seq2, gen, exp
            if st not in best or c2 < best[st]:
                best[st] = c2
                heapq.heappush(heap,(c2, st, seq2))

        for ny, nx, a in neighbors(y, x, h, w, walls):
            st2  = (ny, nx, d)
            c2   = cost + 1
            seq2 = seq + [a]
            gen += 1
            if st2 not in best or c2 < best[st2]:
                best[st2] = c2
                heapq.heappush(heap,(c2, st2, seq2)) 

    return None, gen, exp


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 qcbc.py [uniform-cost|depth-first] [world-file]")
        sys.exit(1)

    mode, world_file = sys.argv[1], sys.argv[2]
    h, w, origin, muck, walls = load_environment(world_file)

    if mode == "depth-first":
        plan, gen, exp = depth_seeker(h, w, origin, muck, walls)


    elif mode == "uniform-cost":
        plan, gen, exp = cost_traverse(h, w, origin, muck, walls)
    else:
        print("Unknown algorithm:", mode)
        sys.exit(1)

    if plan is None:
        print("No plan found")
        
    else:
        for a in plan:
            print(a)

    print(f"{gen} our nodes generated...")
    print(f"{exp} our nodes expanded...")

if __name__ == "__main__":
    main()
