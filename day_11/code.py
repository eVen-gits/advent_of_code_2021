from copy import deepcopy

CHECK_DIRECTION = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1)
]

DEBUG = False

def load_data(filename):
    with open(filename, 'r') as f:
        data = [[int(i) for i in line.strip()] for line in f.readlines()]
    return data

def print_data(data):
    for j in range(10):
        print(''.join(map(str, data[j])).replace('0', '*'))

def check_flashes(data):
    indices = []
    for j in range(10):
        for i in range(10):
            if data[j][i] > 9:
                data[j][i] = 0
                indices.append((j, i))
    return indices

def step1(data):
    for j in range(10):
        for i in range(10):
            data[j][i] += 1

def step2(data, indices):
    for j, i in indices:
        for dj, di in CHECK_DIRECTION:
            if all([
                -1 < j+dj < len(data),
                -1 < i+di < len(data[0]),
            ]):
                if data[j+dj][i+di] != 0:
                    data[j+dj][i+di] += 1

def pt_1(data):
    flashes = 0
    if DEBUG: print_data(data)
    for i in range(100):
        step1(data)
        indices = check_flashes(data)
        while indices:
            flashes += len(indices)
            step2(data, indices)
            indices = check_flashes(data)
        if DEBUG:
            print('\nAfter step {}:'.format(i+1))
            print_data(data)

    return flashes

def pt_2(data):
    day = 0
    if DEBUG: print_data(data)
    while True:
        flashes = 0
        step1(data)
        indices = check_flashes(data)
        while indices:
            flashes += len(indices)
            step2(data, indices)
            indices = check_flashes(data)
        day += 1
        if DEBUG:
            print('\nAfter step {}:'.format(day))
            print_data(data)
        if flashes == 100:
            return day

if __name__ == '__main__':
    data = load_data('input.txt')
    print(pt_1(deepcopy(data)))
    print(pt_2(deepcopy(data)))