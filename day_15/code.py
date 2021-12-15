import sys
from math import inf

DEBUG = False

MOVE_DIRS = ((0,1), (1,0), (0,-1), (-1,0))

def load_data(filename):
    with open(filename, 'r') as f:
        data = [[int(i) for i in line.strip()] for line in f.readlines()]
    return data

def find_path(data):
    m, n = len(data), len(data[0])
    costs = [[inf for _ in range(n)] for _ in range(m)]
    costs[0][0] = 0
    q = {0: [(0,0)]}
    while q:
        cost = min(q.keys())
        (cy, cx) = q[cost].pop()
        if len(q[cost]) == 0:
            del q[cost]
        if DEBUG:
            sys.stdout.write('({})Queue size: {}\r'.format(
                costs[-1][-1]
                if costs[-1][-1] is not inf
                else '/',
                sum(len(q)for q in q.values())
            ))
            sys.stdout.flush()
        for (dy, dx) in MOVE_DIRS:
            y = cy + dy
            x = cx + dx
            if all([
                0 <= y < m,
                0 <= x < n,
            ]):
                if cost+data[y][x] < costs[y][x]:
                    costs[y][x] = cost + data[y][x]
                    if costs[y][x] not in q:
                        q[costs[y][x]] = [(y, x)]
                    else:
                        q[costs[y][x]].append((y, x))

    if DEBUG: print()
    return costs

def extend_data(data, reps=5):
    m, n = len(data), len(data[0])
    new_data = [[0 for _ in range(n*reps)] for _ in range(m*reps)]
    for mul_x in range(reps):
        for mul_y in range(reps):
            for x, y in [(x, y) for x in range(n) for y in range(m)]:
                my, mx = mul_y*m+y, mul_x*n+x
                new_val = (data[y][x] + mul_x + mul_y)
                if new_val > 9:
                    new_val = new_val % 10 + 1

                new_data[my][mx] = new_val

    return new_data

def pt_1(data: list) -> int:
    costs = find_path(data)
    return costs[-1][-1]

def pt_2(data: list) -> int:
    data5 = extend_data(data, 5)
    costs = find_path(data5)
    return costs[-1][-1]

if __name__ == '__main__':
    data = load_data('input.txt')
    print(pt_1(data))
    print(pt_2(data))