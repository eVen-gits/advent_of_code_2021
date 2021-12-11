import sys
import time

def load_data(filename):
    with open(filename, 'r') as f:
        data = [i for i in f.readlines()]
        blen = len(data[0].strip())
        data = [int(i, 2) for i in data]
    return data, blen

def get_most_common_bit(data, blen, bit_pos, reverse=False):
    # number of binary inputs
    n_inputs = len(data)
    # count the number set bits in position bit_pos
    ones = sum([
        1 for d in data if d & (1 << bit_pos)
    ])
    # reverse logic for counting (look for less common bit value)
    if reverse:
        return 0 if ones >= n_inputs / 2 else 1
    return 1 if ones >= n_inputs / 2 else 0

def pt_1(data, blen):
    # max integer value for blen bits
    maxint = int('1' * blen, 2)

    # initialize array for result
    gamma = [0] * blen
    for b in range(blen):
        gamma[blen-b-1] = get_most_common_bit(data, blen, b)
    # convert bit string to integer
    gamma = int(''.join(map(str, gamma)), 2)
    # bitwise flip
    epsilon = ~gamma & maxint

    return gamma, epsilon

def pt_2(data, blen):
    # number of binary inputs
    maxint = int('1' * blen, 2)

    # initialize results array and use it for flipping of logic too
    results = [False, True]
    for r, b in enumerate(results):
        # hard copy data to prevent modification
        consider = data.copy()
        for i in range(blen-1, -1, -1):
            bit_val = get_most_common_bit(consider, blen, i, reverse=b)
            # filter rows that don't match bit_val on bit i
            consider = [
                d for d in consider
                if bool(d & (1 << i)) == bit_val
            ]
            if(len(consider) < 2):
                try:
                    results[r] = consider[0]
                except IndexError:
                    # error in input data
                    results[r] = None
                break

    oxy, co2 = results
    return oxy, co2

if __name__ == '__main__':
    data, blen = load_data('input.txt')

    gamma, epsilon = pt_1(data, blen)
    print(gamma * epsilon)
    oxy, co2 = pt_2(data, blen)
    print(oxy * co2)