cache = {}

def move(positions, cost_function):
    #calculate the distance from the mean
    pmin, pmax = min(positions), max(positions)
    move_sums = min([
        sum([cost_function(x, target) for x in positions])
        for i, target in enumerate(range(pmin, pmax+1))
    ])

    return move_sums

def pt_1(x, target):
    return abs(x-target)

def pt_2(x, target):
    d = abs(x-target)
    if d not in cache:
        cache[d] = sum(range(abs(x-target)+1))
    return cache[d]

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        data = [int(i) for i in f.readline().strip().split(',')]

    print(move(data, pt_1))
    print(move(data, pt_2))

