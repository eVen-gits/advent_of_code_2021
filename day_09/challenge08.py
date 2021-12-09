
def non_minima_suppression(data):
    m, n = len(data), len(data[0])
    data_aug = [[0]*n for i in range(m)]
    indices = []
    for j in range(m):
        for i in range(n):
            is_maxima = is_local_minima(j, i, data)
            data_aug[j][i] = 1 if is_maxima else 0
            if is_maxima:
                indices.append((j, i))

    return data_aug, indices

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
    _, indices = non_minima_suppression(data)

    sum_risk = 0
    for j, i in indices:
        sum_risk += data[j][i]+1
    return sum_risk

def pt_2(data):
    _, indices = non_minima_suppression(data)

    grown_regions = []
    for local_min in indices:
        expanded = expand(data, [local_min])
        grown_regions.append(expanded)

    sizes = sorted([len(region) for region in grown_regions])[-3:]
    mul = sizes[0] * sizes[1] * sizes[2]
    return mul

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
    with open('input.txt', 'r') as f:
        data = [[int(d) for d in i.strip()] for i in f.readlines()]
    print(pt_1(data))
    print(pt_2(data))