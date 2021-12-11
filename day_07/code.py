def load_data(filename):
    with open(filename, 'r') as f:
        data = [int(i) for i in f.readline().strip().split(',')]
    return data

cache = {}

def move(positions, cost_function):
    #calculate the distance from the mean
    pmin, pmax = min(positions), max(positions)
    move_sums = min([
        sum([cost_function(x, target) for x in positions])
        for i, target in enumerate(range(pmin, pmax+1))
    ])

    return move_sums

def pt_1(data):
    return move(data, pt_1_move)

def pt_2(data):
    return move(data, pt_2_move)

def pt_1_move(x, target):
    return abs(x-target)

def pt_2_move(x, target):
    d = abs(x-target)
    if d not in cache:
        cache[d] = sum(range(abs(x-target)+1))
    return cache[d]



if __name__ == '__main__':
    data = load_data('input.txt')

    print(pt_1(data))
    print(pt_2(data))

