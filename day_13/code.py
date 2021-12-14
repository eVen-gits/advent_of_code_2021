from enum import Enum
from copy import deepcopy

DEBUG = False

class Fold(Enum):
    Y = 0
    X = 1

def load_data(filename):
    with open(filename, 'r') as f:
        data = [line.strip() for line in f.readlines()]
        dots = set()
        folds = []
        for line in data:
            coords = line.split(',')
            if len(coords) == 2:
                dots.add((int(coords[0]), int(coords[1])))
            elif 'fold along' in line:
                split = line.split('=')
                position = int(split[-1])
                folds.append((
                    int(split[-1]),
                    Fold[split[0][-1].upper()]
                ))
        data = dots, folds
    return data

def print_grid(dots, m, n):
    for y in range(m+1):
        for x in range(n+1):
            if (x, y) in dots:
                print('#', end='')
            else:
                print('.', end='')
        print()

def fold(dots, action):
    fpos, faxis = action

    Xs = [dot[0] for dot in dots]
    Ys = [dot[1] for dot in dots]

    m, n = max(Ys), max(Xs)
    if DEBUG:
        print()
        print_grid(dots, m, n)

    if faxis == Fold.X:
        m2, n2 = m, min(fpos-1, n-fpos-1)
    else:
        m2, n2 = max(fpos-1, m-fpos-1), n

    new_dots = set()
    for dot in dots:
        if faxis == Fold.X:
            if n2 > fpos: #TODO: Extending fold
                new_dots.add((dot[0]-fpos-1, dot[1]))
            else:
                if dot[0] < fpos:
                    new_dots.add((fpos-dot[0]-1, dot[1]))
                else:
                    new_dots.add((dot[0]-fpos-1, dot[1]))
        elif faxis == Fold.Y:
            if dot[1] > fpos:
                new_dots.add((dot[0], m2 - (dot[1] - fpos-1)))
            elif m2 > fpos: #TODO: extending fold
                new_dots.add((dot[0], dot[1] + m2 - fpos))
            else:
                new_dots.add(dot)

    if DEBUG:
        print('Folding along {}={}'.format(faxis.name, fpos))
        print_grid(new_dots, m2, n2)
    return new_dots


def pt_1(dots, folds):
    for action in [folds[0]]:
        dots = fold(dots, action)
    return len(dots)

def pt_2(dots, folds):
    for action in folds:
        dots = fold(dots, action)

    Xs = [dot[0] for dot in dots]
    Ys = [dot[1] for dot in dots]

    m, n = max(Ys), max(Xs)

    print()
    print_grid(dots, m, n)
    return None

if __name__ == '__main__':
    dots, folds = load_data('input.txt')
    print(pt_1(deepcopy(dots), folds))
    print(pt_2(deepcopy(dots), folds))