def load_data(filename):
    with open(filename, 'r') as f:
        data = [[int(d) for d in i.strip()] for i in f.readlines()]
    return data

def non_minima_suppression(data):
    m, n = len(data), len(data[0])
    indices = []
    for j in range(m):
        for i in range(n):
            if is_local_minima(j, i, data):
                indices.append((j, i))

    return indices

def is_local_minima(j, i, data):
    m, n = len(data), len(data[0])
    checks = [
        (j+dj, i+di)
        for dj, di
        in [
            (-1, 0), (0, -1), (1, 0), (0, 1),
        ]
        if 0 <= i+di < n and 0 <= j+dj < m
    ]
    for dj, di in checks:
        if data[j][i] >= data[dj][di]:
            return False
    return True

def pt_1(data):
    indices = non_minima_suppression(data)

    sum_risk = 0
    for j, i in indices:
        sum_risk += data[j][i]+1
    return sum_risk

def pt_2(data):
    indices = non_minima_suppression(data)

    grown_regions = []
    for local_min in indices:
        expanded = expand(data, [local_min])
        grown_regions.append(expanded)

    sizes = sorted([len(region) for region in grown_regions])[-3:]
    return sizes[0] * sizes[1] * sizes[2]

def expand(data, indices):
    m, n = len(data), len(data[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    new_indices = set() #note: adding duplicates isnt a problem since it's a set
    for j, i in indices:
        for dj, di in directions:
            if 0 <= j+dj < m and 0 <= i+di < n:
                if all([
                    data[j+dj][i+di] > data[j][i], #larger than current
                    data[j+dj][i+di] < 9, #not 9 which is limit
                ]):
                    new_indices.add((j+dj, i+di))

    if new_indices:
        return set(indices).union(expand(data, new_indices))
    return set(indices)

if __name__ == '__main__':
    data = load_data('input.txt')
    print(pt_1(data))
    print(pt_2(data))