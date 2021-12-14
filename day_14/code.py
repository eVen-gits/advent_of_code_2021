from tqdm import tqdm
DEBUG = False

def load_data(filename):
    with open(filename, 'r') as f:
        data = [line.strip() for line in f.readlines()]
        seq = data[0]
        rules = {key:val for key, val in [d.split(' -> ') for d in data[2:]]}
    return list(seq), rules

def evolve_pt1(seq: list, rules: dict) -> list:
    i = 0
    #alocate array
    new_seq = [''] * (len(seq) * 2 - 1)
    #copy old values
    new_seq[0::2] = seq
    for i in range(len(seq)-1):
        key = '{}{}'.format(seq[i], seq[i+1])
        new_seq[i*2+1]= rules[key]
    return new_seq

def evolve_pt2(poly: dict, rules: dict) -> dict:
    new_poly = {}
    for key, val in poly.items():
        p1, p3 = key
        p2 = rules[key]
        k1 = p1+p2
        k2 = p2+p3
        if k1 not in new_poly:
            new_poly[k1] = 0
        if k2 not in new_poly:
            new_poly[k2] = 0
        new_poly[k1] += val
        new_poly[k2] += val
    return new_poly

def count_poly(poly: dict) -> dict:
    # Note: each character is counted twice
    counts = {}
    for key, val in poly.items():
        if key[0] not in counts:
            counts[key[0]] = 0
        if key[1] not in counts:
            counts[key[1]] = 0
        counts[key[0]] += val
        counts[key[1]] += val
    return counts

def transform(seq: list) -> dict:
    poly = {}
    for i in range(len(seq)-1):
        key = '{}{}'.format(seq[i], seq[i+1])
        if key not in poly:
            poly[key] = 0
        poly[key] += 1
    return poly

def pt_1(seq: list, rules: dict, days=10) -> int:
    for i in range(days):
        seq = evolve_pt1(seq, rules)
        if DEBUG: print('{}: {}'.format(i, len(seq)))

    counts = sorted([(c, seq.count(c)) for c in set(seq)], key=lambda x: x[1])
    return counts[-1][1] - counts[0][1]

def pt_2(seq: list, rules: dict, days=40):
    poly = transform(seq)
    for i in range(days):
        poly = evolve_pt2(poly, rules)
        if DEBUG: print('\n'.join(['{}: {}'.format(k, v) for k, v in poly.items()]))

    counts = sorted([(k, v) for k, v in count_poly(poly).items()], key=lambda x: x[1])
    return (counts[-1][1] - counts[0][1])//2

if __name__ == '__main__':
    seq, rules = load_data('input.txt')
    print(pt_1(seq, rules))
    print(pt_2(seq, rules))